from oauth2client import client, crypt

def check_id_token(app, id_token):
    try:
        idinfo = client.verify_id_token(id_token, app.conf.admin.client_id)
        # If multiple clients access the backend server:
        if not idinfo['aud'] == app.conf.admin.client_id:
            raise crypt.AppIdentityError("Unrecognized client.")
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")
    except crypt.AppIdentityError:
        # Invalid token
        return false

    user_email = idinfo['email']
    return user_email == app.conf.admin.admin_email

def check_login_cookie(app, req, res):
    cookie_from_token = req.get_cookie(app.conf.admin.cookie_name)
    if cookie_from_token:
        if check_id_token(app, cookie_from_token):
            return True
        else:
            res.delete_cookie(app.conf.admin.cookie_name, path=app.conf.admin.cookie_path)

    return False

def authorize(app, should_redirect=False):
    def outer(callback):
        from bottle import request, response, redirect, abort

        def wrap_func(*args, **kwargs):
            if not check_login_cookie(app, request, response):
                if should_redirect:
                    redirect('/admin')
                else:
                    abort(403, '{"error": "invalid_credentials"}')
            else:
                return callback(*args, **kwargs)

    return outer
