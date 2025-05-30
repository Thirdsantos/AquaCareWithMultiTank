import firebase_admin
from firebase_admin import credentials, db
import os

# Get the path to the key in the same folder as this file
KEY_PATH = os.path.join(os.path.dirname(__file__), 'key.json')
cred = credentials.Certificate(KEY_PATH)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ac-with-multitank-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

firebase_db = db