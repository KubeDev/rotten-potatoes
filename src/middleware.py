import re
from werkzeug import datastructures
from werkzeug.wrappers import Request, Response, ResponseStream
from datetime import date, datetime, timedelta


unhealth = False;
unready_until = datetime.now()

def set_unhealth():
    global unhealth
    unhealth = True

def set_unready_for_seconds(seconds):
    global unready_until
    unready_until = datetime.now() + timedelta(0,seconds)

class middleware():
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):

        global unhealth
        global unready_until

        request = Request(environ)

        print(request.path)

        if unhealth:
            res = Response(u'Out', mimetype= 'text/plain', status=500)
        elif unready_until > datetime.now() and '/ready' in request.path:
            res = Response(u'UnReady', mimetype= 'text/plain', status=500)
        else:
            return self.app(environ, start_response)
    