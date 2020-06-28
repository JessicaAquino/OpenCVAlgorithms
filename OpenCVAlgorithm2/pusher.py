import pyrebase
from pusher_push_notifications import PushNotifications
#pip install pyrebase
#pip install pusher_push_notifications

config = {
    'apiKey' : "AIzaSyBS6npE3_ai-AnK7WUfyWWgf2CkIJZgNjg",
    'authDomain' : "crowdcams.firebaseapp.com",
    'databaseURL' : "https://crowdcams.firebaseio.com",
    'projectId' : "crowdcams",
    'storageBucket' : "crowdcams.appspot.com",
    'messagingSenderId' : "183704478086",
    'appId' : "1:183704478086:web:6ba4504e2f3d4594b28c07",
    'measurementId' : "G-4MR2PK8HQE"
  }

firebase = pyrebase.initialize_app(config)

db=firebase.database()

beams_client = PushNotifications(
    instance_id='2148aa96-a718-456b-b0b3-bbc3ad91e908',
    secret_key='629445A7C2BB84C2342A10BE58B366DEF83CA60A58EBC359E5677A7F49F5419F',
)

def stream_handler(message):
    print(message)
    if(message['data'] is 1):
        response = beams_client.publish_to_interests(
          interests=['hello'],
          publish_body={
            'apns': {
              'aps': {
                'alert': 'Hello!',
              },
            },
            'fcm': {
              'notification': {
                'title': 'Hello',
                'body': 'Hello, world!',
              },
            },
            'web': {
              'notification': {
                'title': 'Hello',
                'body': 'Hello, world!',
              },
            },
          },
        )

        print(response['publishId'])

my_stream = db.child("cAirport/alarm").stream(stream_handler, None) #posible error
