#https://www.twilio.com/user/account/settings
#https://www.twilio.com/docs/python/install

from twilio.rest import TwilioRestClient
 
# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = "ACa570d940fdc8f1269214ae0745463cec"
auth_token  = "c07986a1538b652730034e19cb90ea6f"
client = TwilioRestClient(account_sid, auth_token)
 
message = client.messages.create(body="What are you doing now?",
    to="+16472904530",    # Replace with your phone number
    from_="+16477228837") # Replace with your Twilio number
print message.sid
