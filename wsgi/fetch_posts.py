import dropbox
import os
import markdown as md
import tempfile
import db

BLOG_PATH = '/blog'

class PostFetcher(object):
	def __init__(self, config, database, download_path):
		super(PostFetcher, self).__init__()
		self.config = config
		self.database = database
		self.download_path = download_path
		self.dropbox = dropbox.Dropbox(self.config.dropbox.token)

	def get_list(self):
		result = self.dropbox.files_list_folder(BLOG_PATH)
		has_more = True

		while has_more:
			for entry in result.entries:
				# ignore folders, in /blog we never recurse
				extension = os.path.splitext(entry.name)[1].lower()
				if isinstance(entry, dropbox.files.FileMetadata) and extension == '.md':
					yield entry

			if result.has_more:
				result = self.dropbox.files_list_folder_continue(result.cursor)
			else:
				has_more = False

	def fetch_all(self, purge=False):
		if purge:
			self.database.purge()
		for post in self.get_list():
			stored_post = self.database.find_post(post.name)
			print post.name
			if stored_post:
				print 'Found post'
				print '%s <-> %s' % (stored_post.checksum, post.rev)

				if stored_post.checksum == post.rev:
					continue
				else:
					final_name = self.download_and_convert(post)
					self.database.update_post(final_name, post.rev)
			else:
				print 'NOT Found post'
				final_name = self.download_and_convert(post)
				self.database.add_post(final_name, post.rev)

			
	def download_and_convert(self, post):
		temp_file_handle, temp_file_name = tempfile.mkstemp()

		print "Downloading %s to %s" % (post.name, temp_file_name)
		self.dropbox.files_download_to_file(temp_file_name, post.path_lower)

		base_name = os.path.splitext(post.name)[0]
		html_name = base_name + '.html'
		md.markdownFromFile(input=temp_file_name, output=os.path.join(self.download_path, html_name))

		os.remove(temp_file_name)

		return base_name
