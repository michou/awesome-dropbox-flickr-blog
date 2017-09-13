#!/usr/bin/python

################################################################################
#  ALWAYS RUN FROM PROJECT ROOT, NOT FROM wsgi/ OR FARTHER AWAY
################################################################################
from blog import app as application
import envutils
from bottle import run

if __name__ == '__main__':
    envutils.PRODUCTION_MODE = False
    run(application, host='0.0.0.0', port=8080, reloader=True, debug=True)
