import os
import re
from time import sleep
import json, requests

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
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

found = 0
def update_temp():
    global found
    imp_url = "http://agent.electricimp.com/aGOfLf9OoNcW"
    resp = requests.get(url = imp_url)
    data = json.dumps(resp.content)
    m = re.search("(\d+.\d+)", data)
    if m:
        found = m.group(1)

class MainPage(MainHandler):
    def get(self):
        self.write("Again")
        global found

        update_temp()
                
        if found < 32:
            update_temp()
        else:
            self.write(found)
            alert()
        
        self.redirect("/")
    

        



"""
Alert Stuff
"""
def alert():
    # SendGrid
    sg = sendgrid.SendGridClient('mpatini', 'footyy612')
    message = sendgrid.Mail(to='mpatini@me.com', subject="Baby, such heat, much danger!", html="You're baby is uncomfortably warm. Please check on your baby.", text="Please check on your baby", from_email='mpatini@sas.upenn.edu')
    sg.send(message)
    #Twilio
    account_sid = "ACaefb3fc1b4e90f423de6e3695886d4a0"
    auth_token  = "31f62a7a0969c0032095e3a5fe8d0171"
    client = TwilioRestClient(account_sid, auth_token)
    message = client.messages.create(body="You're baby is uncomfortably warm. Please check on your baby.",
                                     to="19512883162",
                                     from_="19094522970")
    print message.sid


class Alert(MainHandler):
    def get(self):
        alert()


app = webapp2.WSGIApplication([('/', MainPage),
							   ('/alert', Alert),
                               ],
                              debug=True)

def main():
    from paste import httpserver
    httpserver.serve(app, host='0.0.0.0', port='8080')

if __name__ == '__main__':
	main()
