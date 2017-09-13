import os

PRODUCTION_MODE = True
OVERRIDES = {
    'OPENSHIFT_REPO_DIR': '.',
    # HACK-HACK-HACK: These should be actually taken from a config file or something
    # Hardcoding these values until I write some proper code to encapsulate these settings
    'OPENSHIFT_DATA_DIR': '/var/www/blog'
}

def set_local_or_prod(env_key, remote_path, local_path):
    if PRODUCTION_MODE:
        if env_key in os.environ:
            return os.path.realpath(os.path.join(os.environ[env_key], remote_path))
        else:
            return os.path.realpath(os.path.join(OVERRIDES[env_key], remote_path))
    else:
        return os.path.realpath(local_path)
