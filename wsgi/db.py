import tinydb
import os
import re

POSTS_TABLE = 'posts'
TOKENS_TABLE = 'tokens'

class BlogPost(object):
	def __init__(self, base_path, checksum):
		super(BlogPost, self).__init__()

		self.base_path = base_path
		self.checksum = checksum

		base_name = os.path.splitext(base_path)[0]
		title_splitter = re.compile(r"(\d{4}-\d{2}-\d{2}) (.*)")
		self.date, self.title = title_splitter.search(base_name).groups()

class DropboxToken(object):
	def __init__(self, user_id, token, cursor = None):
		super(DropboxToken, self).__init__()
		self.user_id = user_id
		self.token = token
		self.cursor = cursor

class TokensDatabase(object):
	def __init__(self, local_path):
		super(TokensDatabase, self).__init__()
		self._db = tinydb.TinyDB(local_path)
		self.tokens = self._db.table(TOKENS_TABLE)

	def get_token(self, user_id):
		user = tinydb.Query()
		result = self.tokens.search(user['user_id'] == user_id)

		if result:
			return DropboxToken(result[0]['user_id'],
				result[0]['token'],
				result[0]['cursor'] if 'cursor' in result[0] else None)
		else:
			return None

	def put_token(self, user_id, token, cursor = None):
		print 'Saving token for ' + user_id
		existing_token = self.get_token(user_id)
		query = tinydb.Query()
		if existing_token:
			print '    update existing'
			self.tokens.update({
				'token': token,
				'cursor': cursor
			}, query['user_id'] == user_id)
		else:
			print '    new token'
			self.tokens.insert({
				'user_id': user_id,
				'token': token,
				'cursor': cursor
			})

class PostsDatabase(object):
	def __init__(self, local_path):
		super(PostsDatabase, self).__init__()
		self.local_path = local_path
		self.__init_db__()

	def __init_db__(self):
		self._db = tinydb.TinyDB(self.local_path)
		self.posts = self._db.table(POSTS_TABLE)

	def find_post(self, base_path):
		post_query = tinydb.Query()

		result = self.posts.search(post_query['base_path'] == base_path)

		if result:
			return BlogPost(result[0]['base_path'], result[0]['checksum'])
		else:
			return None

	def add_post(self, local_path, post_hash):
		print 'In add'
		post = BlogPost(local_path, post_hash)

		self.posts.insert({
			'title': post.title,
			'date': post.date,
			'checksum': post.checksum,
			'base_path': post.base_path
			})

	def update_post(self, base_path, post_hash):
		print 'In update'
		post_query = tinydb.Query()

		self.posts.update({
			'checksum': post_hash
			}, post_query['base_path'] == base_path)

	def __get_sorted_entries(self):
		return sorted(self.posts.all(), key = lambda p: p['date'], reverse = True)

	def __get_blog_post_for_entry(self, db_entry):
		return BlogPost(db_entry['base_path'],db_entry['checksum'])

	def get_all_posts(self):
		return [ BlogPost(i['base_path'], i['checksum']) for i in self.__get_sorted_entries() ]

	def get_next_prev(self, base_path):
		sorted_posts = self.__get_sorted_entries()
		total_posts = len(sorted_posts)
		for i in range(0, total_posts):
			if sorted_posts[i]['base_path'] == base_path:
				return (
					self.__get_blog_post_for_entry(sorted_posts[i-1]) if i > 0 else None,
					self.__get_blog_post_for_entry(sorted_posts[i+1]) if i < total_posts - 1 else None
					)
		return (None, None)

	def purge(self):
		self.posts.purge()
