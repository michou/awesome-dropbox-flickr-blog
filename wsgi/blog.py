from bottle import TEMPLATE_PATH
from bottle import Bottle
from bottle import static_file, template
from bottle import request, response, redirect, abort

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
from db import PostsDatabase, TokensDatabase

import dropbox_utils

app.conf = Configuration(os.path.join(CONTENT_PATH, 'config.ini'))
app.database = PostsDatabase(os.path.join(CONTENT_PATH, 'posts.json'))
app.tokens = TokensDatabase(os.path.join(CONTENT_PATH, 'tokens.json'))

@app.route('/static/<path:path>')
def serve_static(path):
	return static_file(path, STATIC_PATH)

@app.route('/bumper')
def bumper():
	return template('bumper.tpl')

@app.route('/')
def posts_index():
	posts = app.database.get_all_posts()
	if not posts:
		# nothing to display, go back to bumper page
		redirect('/bumper')
	else:
		latest_post = posts[0]
		print latest_post
		redirect('/posts/' + latest_post.base_path)

@app.route('/posts/<post_path>')
def single_post(post_path):
	post = app.database.find_post(post_path)
	if not post:
		abort(404)
	previous, next = app.database.get_next_prev(post_path)
	return template('posts/single.tpl',
			body=open(os.path.join(CONTENT_PATH, post_path + ".html")),
			previous=previous,
			next=next,
			title=post.title
		)

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
	with_cleanup = bool(request.forms.purge_database)
	fetcher.fetch_all(with_cleanup)

	return "Posts refreshed, check home page"

@app.get('/sync')
def dropbox_webhook_echo():
	return request.query.get('challenge')

@app.post('/sync')
def dropbox_webhook_handler():
	import copy_posts

	if dropbox_utils.check_dropbox_webhook_signature(request, app.conf.dropbox.client_secret):
		for account in request.json['list_folder']['accounts']:
			copy_posts.PostSyncer(app.conf, app.tokens, account).start()

		return '{"result": "ok"}'
	else:
		abort(403)


@app.get('/admin/oauth/start')
def dropbox_oauth_start():
	_, oauth_flow = dropbox_utils.get_dropbox_oauth_flow(request, app.conf.dropbox.client_id, app.conf.dropbox.client_secret, app.conf.dropbox.cookie_name)
	authorize_url = oauth_flow.start()

	return '<a href="%s">Login with DropBox</a>' % (authorize_url)

@app.get('/admin/oauth/done')
def drobox_oauth_complete():
	import dropbox
	session, oauth_flow = dropbox_utils.get_dropbox_oauth_flow(request, app.conf.dropbox.client_id, app.conf.dropbox.client_secret, app.conf.dropbox.cookie_name, True)

	access_token, user_id_v1, state = oauth_flow.finish(request.query)

	dbx = dropbox.Dropbox(access_token)
	account_info = dbx.users_get_current_account()

	app.tokens.put_token(account_info.account_id, access_token)

	return 'Hi %s!' % (account_info.account_id)

@app.error(404)
def error_not_found(error):
	return template('errors/404.tpl')
