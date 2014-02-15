import sendgrid

sg = sendgrid.SendGridClient('mpatini', 'footyy612')
message = sendgrid.Mail(to='mpatini@me.com', subject='Baby Alert', html="You're baby is too cold!", text="You're baby is too cold!", from_email='mpatini@sas.upenn.edu')
sg.send(message)