import os
import re

import sendgrid
from twilio.rest import TwilioRestClient

import webapp2
import jinja2

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
		self.write("Hit /alert to cause an email/sms send")

class Alert(MainHandler):
	def get(self):
        # SendGrid
		sg = sendgrid.SendGridClient('mpatini', 'footyy612')
		message = sendgrid.Mail(to='mpatini@me.com', subject='Baby Alert', html="You're baby is too cold!", text="You're baby is too cold!", from_email='mpatini@sas.upenn.edu')
		sg.send(message)
        #Twilio
        account_sid = "ACaefb3fc1b4e90f423de6e3695886d4a0"
        auth_token  = "31f62a7a0969c0032095e3a5fe8d0171"
        client = TwilioRestClient(account_sid, auth_token)
        message = client.messages.create(body="ALERT: you're baby is too cold!",
                                         to="19512883162",
                                         from_="19094522970")
        print message.sid
        # redirect to main page
        self.redirect('/')


app = webapp2.WSGIApplication([('/', TestPage),
							                 ('/alert', Alert),
                               ],
                              debug=True)

def main():
  from paste import httpserver
  httpserver.serve(app, host='0.0.0.0', port='8080')

if __name__ == '__main__':
	main()
