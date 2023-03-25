import firebase_admin
from firebase_admin import credentials, messaging
from errandz_backend import settings
import json


class FCMNotification():
    def __init__(self):
        firebase_cred = credentials.Certificate(
            settings.FIREBASE_SETTINGS.get("CERTIFICATE"))
        firebase_app = firebase_admin.initialize_app(firebase_cred)

    def send_notification(self, tokens: list, notification: dict):
        print(notification)
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=notification['title'],
                body=notification['body']
            ),
            tokens=tokens
        )
        messaging.send_multicast(message)
