import firebase_admin
from firebase_admin import credentials, db
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def initialize_firebase():
    try:
        # Try to get Firebase credentials from environment variable
        firebase_credentials = os.getenv("FIREBASE_CREDENTIALS")
        
        if firebase_credentials:
            # Parse JSON credentials from environment variable
            cred_dict = json.loads(firebase_credentials)
            cred = credentials.Certificate(cred_dict)
        else:
            # Fallback to local file for development
            KEY_PATH = os.path.join(os.path.dirname(__file__), 'key.json')
            if os.path.exists(KEY_PATH):
                cred = credentials.Certificate(KEY_PATH)
            else:
                print("Firebase credentials not found in environment or local file")
                return None
        
        # Get database URL from environment or use default
        database_url = os.getenv("FIREBASE_DATABASE_URL", 
                                "https://ac-with-multitank-default-rtdb.asia-southeast1.firebasedatabase.app/")
        
        firebase_admin.initialize_app(cred, {
            'databaseURL': database_url
        })
        
        return db
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        return None

firebase_db = initialize_firebase()