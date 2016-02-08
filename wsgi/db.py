import tinydb
import os
import re

POSTS_TABLE = 'posts'

class BlogPost(object):
	def __init__(self, path, checksum):
		super(BlogPost, self).__init__()

		self.path = path
		self.checksum = checksum

		base_name = os.path.splitext(path)[0]
		title_splitter = re.compile(r"(\d{4}-\d{2}-\d{2}) (.*)")
		self.date, self.title = title_splitter.search(base_name).groups()

class PostsDatabase(object):
	def __init__(self, local_path):
		super(PostsDatabase, self).__init__()
		self.local_path = local_path
		self.__init_db__()

	def __init_db__(self):
		self._db = tinydb.TinyDB(self.local_path)
		self.posts = self._db.table(POSTS_TABLE)

	def find_post(self, post_path):
		post_query = tinydb.Query()

		result = self.posts.search(post_query['path'] == post_path)

		if result:
			return BlogPost(result[0]['path'], result[0]['checksum'])
		else:
			return None

	def add_post(self, post_path, post_hash):
		post = BlogPost(post_path, post_hash)

		self.posts.insert({
			'title': post.title,
			'date': post.date,
			'checksum': post.checksum,
			'path': post.path
			})

	def update_post(self, post_path, post_hash):
		post = BlogPost(post_path, post_hash)
		post_query = tinydb.Query()

		self.posts.update({
			'title': post.title,
			'date': post.date,
			'checksum': post.checksum,
			'path': post.path
			}, post_query['path'] == post_path)

	def __get_sorted_entries(self):
		return sorted(self.posts.all(), key = lambda p: p['date'], reverse = True)

	def __get_blog_post_for_entry(self, entry):
		return BlogPost(entry['path'], entry['checksum'])

	def get_all_posts(self):
		return [ BlogPost(i['path'], i['checksum']) for i in self.__get_sorted_entries() ]

	def get_next_prev(self, post_path):
		sorted_posts = self.__get_sorted_entries()
		total_posts = len(sorted_posts)
		for i in range(0, total_posts):
			if sorted_posts[i]['path'] == post_path:
				return (
					self.__get_blog_post_for_entry(sorted_posts[i-1]) if i > 0 else None,
					self.__get_blog_post_for_entry(sorted_posts[i+1]) if i < total_posts - 1 else None
					)
		return (None, None)


	def flush(self):
		self.posts.purge_tables()