from deta import Deta
DETA_KEY="c0qxqchn_L5nmo4TjJEw2ZEvfFsN5M1PeDbhDNCuY"

#This is how to create/connect a database
deta = Deta(DETA_KEY)
db = deta.Base("users_db")
dd = deta.Base("data_db")

def insert_user(username, name, password):
    """Return the user on a successful user creation, otherwise raises and error"""
    return db.put({"key": username, "name": name, "password": password})

def fetch_all_users():
    """Returns a dict of all users"""
    res = db.fetch()
    return res.items

def fetch_users(usern):
    """Returns a dict of all users"""
    res = dd.fetch("username" == usern)
    return res.items

def get_user(username):
    """If not found, the function will return None"""
    return db.get(username)

def update_user(username, updates):
    """If the item is updated, returns None. Otherwise, an exception is raised"""
    return db.update(updates, username)

def delete_user(username):
    """Always returns None, even if the key does not exist"""
    return db.delete(username)

def insert_data(key, username, title, quartile, characters):
    """Return the user on a successful user creation, otherwise raises and error"""
    return dd.put({"key": key,"username":username,"title": title,"quartile": quartile, "characters": characters})

def get_data(data):
    """If not found, the function will return None"""
    return dd.get(data)


insert_user("adminq","adminq","123")