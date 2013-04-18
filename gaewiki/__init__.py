# encoding=utf-8

import os
import sys

import webapp2
import handlers

application = webapp2.WSGIApplication(handlers.handlers)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(__file__))
    main()
