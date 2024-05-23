from google.cloud import firestore
from firebase_admin import credentials
from firebase_admin import firestore

class Connection:
    
    def fire_store(self,key):
        db = firestore.Client()
        db.collection(key).add()