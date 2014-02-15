from twilio.rest import TwilioRestClient

account_sid = "ACaefb3fc1b4e90f423de6e3695886d4a0"
auth_token  = "31f62a7a0969c0032095e3a5fe8d0171"
client = TwilioRestClient(account_sid, auth_token)

message = client.messages.create(body="ALERT: you're baby is too cold!",
    to="19512883162",
    from_="19094522970")
print message.sid