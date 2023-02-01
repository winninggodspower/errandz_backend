# Download the helper library from https://www.twilio.com/docs/python/install
import os
from dotenv import load_dotenv
from twilio.rest import Client

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, ".env"))


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC93847d9bb61fe613344915b6fcfc43a4'
auth_token = '5c354089a06ec4d60d6d54e331103089'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon. this is from errandz",
                     from_='+19063238803',
                     to='+234 818 074 2938'
                 )

print(message.sid)