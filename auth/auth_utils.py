import json
import hashlib
import os

USER_DB_PATH = "auth/users_db.json"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists(USER_DB_PATH):
        return {}
    with open(USER_DB_PATH, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USER_DB_PATH, 'w') as f:
        json.dump(users, f)

def register_user(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = hash_password(password)
    save_users(users)
    return True

def login_user(username, password):
    users = load_users()
    hashed = hash_password(password)
    return username in users and users[username] == hashed
