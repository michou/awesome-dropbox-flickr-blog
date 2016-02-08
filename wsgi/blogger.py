from bottle import TEMPLATE_PATH
from bottle import Bottle
from bottle import static_file, template
from bottle import request, response, redirect

from envutils import set_local_or_prod

import auth_util

VIEWS_PATH = set_local_or_prod('OPENSHIFT_REPO_DIR', 'wsgi/views', 'wsgi/views')
STATIC_PATH = set_local_or_prod('OPENSHIFT_REPO_DIR', 'wsgi/static', 'wsgi/static')
CONTENT_PATH = set_local_or_prod('OPENSHIFT_DATA_DIR', '.', './data')

# This must be added in order to do correct path lookups for the views
if VIEWS_PATH not in TEMPLATE_PATH:
	TEMPLATE_PATH.append(VIEWS_PATH)

app = Bottle()

import os
from localconfig import LocalConfig as Configuration
from db import PostsDatabase

app.conf = Configuration(os.path.join(CONTENT_PATH, 'config.ini'))
app.database = PostsDatabase(os.path.join(CONTENT_PATH, 'posts.json'))

@app.route('/static/<path:path>')
def serve_static(path):
	return static_file(path, STATIC_PATH)

@app.route('/')
def bumper():
	return template('bumper.tpl')

@app.route('/posts')
def posts_index():
	posts = app.database.get_all_posts()
	if not posts:
		# nothing to display, go back to bumper page
		redirect('/')
	else:
		latest_post = posts[0]
		print latest_post
		redirect('/posts/' + latest_post.path)

@app.route('/posts/<post_path>')
def single_post(post_path):
	post = app.database.find_post(post_path)
	previous, next = app.database.get_next_prev(post_path)
	return template('posts/single.tpl',
			body=open(os.path.join(CONTENT_PATH, post_path)),
			previous=previous,
			next=next,
			title=post.title
		)


@app.route('/posts/<which:path>')
def render_post(which):
	composed_path = os.path.realpath(os.path.join(CONTENT_PATH, which))
	print which
	print composed_path
	print CONTENT_PATH
	
	if composed_path.startswith(CONTENT_PATH):
		print "Returning: " + composed_path
		return static_file(composed_path, root = "/")
	else:
		abort(404, "Bad path: " + which)

@app.route('/admin')
def render_admin():
	return template('admin/login.tpl')

@app.post('/admin/check')
def admin_response():
	if auth_util.check_id_token(app, request.forms.idtoken):
		response.set_cookie(app.conf.admin.cookie_name, request.forms.idtoken, max_age=600, path=app.conf.admin.cookie_path, httponly=True)
		redirect('/admin/view')
	else:
		# HACK HACK HACK We redirect to a bad page and display the 404 message
		redirect('/forbidden')

@auth_util.authorize(app, should_redirect=True)
@app.route('/admin/view')
def admin_view():
	if auth_util.check_login_cookie(app, request, response):
		return template('admin/view.tpl')
	else:
		redirect('/admin')

@auth_util.authorize(app, should_redirect=True)
@app.post('/admin/fetch/posts')
def admin_reload_posts():
	from fetch_posts import PostFetcher

	fetcher = PostFetcher(app.conf, app.database, CONTENT_PATH)
	fetcher.fetch_all()
	return "Posts refreshed, check home page"

@app.error(404)
def error_not_found(error):
	return "<h1>Nothing to see here, move along!</h1>"
