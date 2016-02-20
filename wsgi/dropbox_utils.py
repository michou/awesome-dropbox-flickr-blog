import dropbox
import StringIO
from hashlib import sha256
import hmac


def get_dropbox_oauth_flow(request, client_id, client_secret, cookie_name, finishing=False):
    redirect_uri = '%s://%s/admin/oauth/done' % (request.urlparts.scheme, request.urlparts.netloc)
    if finishing:
        session = request.cookies
    else:
        session = {}

    return session, dropbox.oauth.DropboxOAuth2Flow(
        client_id,
        client_secret,
        redirect_uri,
        session,
        cookie_name)


def get_user_credentials_from_oauth_flow(request, oauth_flow):
    access_token, user_id_v1, state = oauth_flow.finish(request.query)

    dbx = dropbox.Dropbox(access_token)
    account_info = dbx.users_get_current_account()

    return (account_info.account_id, access_token)


def check_dropbox_webhook_signature(request, client_secret):
    if isinstance(request.body, StringIO.StringIO):
        own_signature = hmac.new(client_secret, request.body.getvalue(), sha256)
    else:
        own_signature = hmac.new(client_secret, request.body, sha256)

    signature = request.headers.get('X-Dropbox-Signature')

    return hmac.compare_digest(signature, own_signature.hexdigest())
