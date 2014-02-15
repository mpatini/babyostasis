import os
import re
import random
import hashlib
import hmac
import json
from string import letters
from sendgrid import Sendgrid

import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class MainHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        params['user'] = self.user
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class TestPage(MainHandler):
	def get(self):
		self.write("Hi, I'm serving!")

class SendGrid(MainHandler):
	def get(self):
		sg = sendgrid.Sendgrid.SendGridClient('mpatini', 'footyy612')
		message = sendgrid.Sendgrid.Mail(to='mpatini@me.com', subject='Baby Alert', html="You're baby is too cold!", text="You're baby is too cold!", from_email='mpatini@sas.upenn.edu')
		sg.web.send(message)


app = webapp2.WSGIApplication([('/', TestPage),
							   ('/sendgrid', SendGrid),
                               ],
                              debug=True)
