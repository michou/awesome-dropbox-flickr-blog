import dropbox
import os
import markdown as md
import tempfile

BLOG_PATH = '/blog'
RESOURCES_LOCAL_FOLDER = 'res'

class PostProcessor(object):
    def __init__(self, posts, dbx, local_path):
        super(PostProcessor, self).__init__()
        self.posts = posts
        self.dropbox = dbx
        self.local_path = local_path

    def matches(self, dropbox_entry):
        extension = os.path.splitext(dropbox_entry.name)[1].lower()
        return isinstance(dropbox_entry, dropbox.files.FileMetadata) and extension == ".md"

    def _download_and_convert(self, entry):
        temp_file_handle, temp_file_name = tempfile.mkstemp()

        print "Downloading %s to %s" % (entry.name, temp_file_name)
        self.dropbox.files_download_to_file(temp_file_name, entry.path_lower)

        base_name = os.path.splitext(entry.name)[0]
        html_name = base_name + '.html'
        md.markdownFromFile(input=temp_file_name, output=os.path.join(self.local_path, html_name))

        os.remove(temp_file_name)

        return base_name

    def process(self, dropbox_entry):
        stored_post = self.posts.find_post(os.path.splitext(dropbox_entry.name)[0])
        if stored_post:
            print 'Found post'
            print '%s <-> %s' % (stored_post.checksum, dropbox_entry.rev)

            if not stored_post.checksum == dropbox_entry.rev:
                # We hit an updated post. Better download and convert
                final_name = self._download_and_convert(dropbox_entry)
                self.posts.update_post(final_name, dropbox_entry.rev)
        else:
            print 'NOT Found post'
            final_name = self._download_and_convert(dropbox_entry)
            self.posts.add_post(final_name, dropbox_entry.rev)

    def purge_storage(self):
        self.posts.purge()

class ImageProcessor(object):
    def __init__(self, images, dbx, local_path):
        super(ImageProcessor, self).__init__()
        self.images = images
        self.dropbox = dbx
        self.local_path = local_path

        self.IMAGE_EXTENSIONS = ['.gif', '.png', '.jpg', '.jpeg']

    def matches(self, dropbox_entry):
        extension = os.path.splitext(dropbox_entry.name)[1].lower()
        return isinstance(dropbox_entry, dropbox.files.FileMetadata) and extension in self.IMAGE_EXTENSIONS

    def process(self, dropbox_entry):
        """
        This assumes all resource files come from within the BLOG_PATH/res folder and as such
        they will be served from HOST/posts/res/ folder
        :param dropbox_entry:
        :return:
        """
        asset_revision = self.images.get_resource_revision(dropbox_entry.path_lower)
        if not asset_revision:
            resources_folder = os.path.join(self.local_path, RESOURCES_LOCAL_FOLDER)
            if not os.path.exists(resources_folder):
                os.mkdir(resources_folder)
            local_file_name = os.path.join(resources_folder, dropbox_entry.name)
            self.dropbox.files_download_to_file(local_file_name, dropbox_entry.path_lower)
            self.images.put_resource(dropbox_entry.path_lower, dropbox_entry.rev)

    def purge_storage(self):
        self.images.purge()

class DropboxFetcher(object):
    def __init__(self, dropbox_token, posts_db, post_images_db, download_path):
        super(DropboxFetcher, self).__init__()

        self.dropbox = dropbox.Dropbox(dropbox_token)

        self.processors = []
        self.processors.append(PostProcessor(posts_db, self.dropbox, download_path))
        self.processors.append(ImageProcessor(post_images_db, self.dropbox, download_path))

        self.download_path = download_path

    def get_list(self):
        result = self.dropbox.files_list_folder(BLOG_PATH, recursive=True)
        has_more = True

        while has_more:
            for entry in result.entries:
                # ignore folders, in /blog we never recurse
                for processor in self.processors:
                    if processor.matches(entry):
                        yield (entry, processor)

            if result.has_more:
                result = self.dropbox.files_list_folder_continue(result.cursor)
            else:
                has_more = False

    def fetch_all(self, purge=False):
        if purge:
            for processor in self.processors:
                processor.purge_storage()

        for entry, processor in self.get_list():
            processor.process(entry)
