import dropbox
import threading
import os
import tempfile

class PostSyncer(threading.Thread):
	def __init__(self, conf, tokens, user):
		super(PostSyncer, self).__init__()
		self.source_users = conf.dropbox.source_users.split(",")
		self.target_user = conf.dropbox.target_user
		self.tokens = tokens
		self.user = user
	
	def run(self):
		# Ignore "master" user for which we already serve resources or any user not listed as a
		# trusted source
		if self.user == self.target_user or not self.user in self.source_users:
			return

		token = self.tokens.get_token(self.user)
		target_user_token = self.tokens.get_token(self.target_user)
		if not token or not target_user_token:
			return

		source_dbx = dropbox.Dropbox(token.token)
		target_dbx = dropbox.Dropbox(target_user_token.token)

		has_more = True

		while has_more:
			if not token.cursor:
				result = source_dbx.files_list_folder('')
			else:
				result = source_dbx.files_list_folder_continue(token.cursor)

			for entry in result.entries:
				if isinstance(entry, dropbox.files.FileMetadata) and entry.path_lower.endswith('.md'):
					_, temp_file_name = tempfile.mkstemp()

					print 'Syncing %s from %s' % (entry.name, self.user)
					print '    downloading to %s' % (temp_file_name, )
					source_dbx.files_download_to_file(temp_file_name, entry.path_lower)

					# TODO implement some sort of file comparison so as not to copy too many files
					print '    uploading'
					target_dbx.files_upload(open(temp_file_name), '/blog/' + entry.name)

					print '    removing %s' % (temp_file_name,)
					os.remove(temp_file_name)

			token.cursor = result.cursor
			has_more = result.has_more

		self.tokens.put_token(self.user, token.token, token.cursor)

