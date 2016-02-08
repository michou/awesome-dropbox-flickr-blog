#!/usr/bin/python

################################################################################
#  ALWAYS RUN FROM PROJECT ROOT, NOT FROM wsgi/ OR FARTHER AWAY
################################################################################
from blogger import app as application
from bottle import run

if __name__ == '__main__':
	run(application, host='0.0.0.0', port=8080, reloader=True, debug=True)