# encoding=utf-8

import os
import sys

import webapp2
import jinja2
import templatetags.filters as filters

jinja_environment = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
jinja_environment.shared=True

def format_datetime(value, format='medium'):
    return value.strftime('%Y-%m-%d %H:%M') 

def get_filters():
    return {
        "parse_page": util.parse_page,
        "pageurl": util.pageurl,
        "pageurl_rel": util.pageurl_rel,
        "uurlencode": util.uurlencode,
        "wikify": util.wikify,
        "breadcrumbs": filters.breadcrumbs,
        "wikify_page": filters.wikify_page,
        "labelurl": filters.labelurl,
        'datetime': format_datetime
    }


for k,v in get_filters().items():
    jinja_environment.filters[k] = v

import handlers
application = webapp2.WSGIApplication(handlers.handlers)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(__file__))
    main()
