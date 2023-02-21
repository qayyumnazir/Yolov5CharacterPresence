import database as db
import streamlit_authenticator as stauth

names = ["Peter Parker"]
usernames = ["pparker"]
passwords = ["abc"]

hashed_passwords = stauth.Hasher(passwords).generate()

for (username, name, hash_password) in zip(usernames, names, hashed_passwords):
    db.insert_user(username, name, hash_password)