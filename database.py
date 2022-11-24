from deta import Deta
import os
from dotenv import load_dotenv

load_dotenv('.env')
DETA_KEY = os.getenv('DETA_KEY')

deta = Deta(DETA_KEY)

db = deta.Base('users_data')

def insert_user(username, name, password):
    return db.put({'key': username, 'name': name, 'password': password})

def fetch_all_users():
    res = db.fetch()
    return res.items

def get_user(username):
    return db.get(username)

def update_user(username, updates):
    return db.update(updates, username)    

def delete_user(username):
    return db.delete(username) 
