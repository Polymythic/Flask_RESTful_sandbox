from user import User

users = [
	User(1, "Andy", "ydna"),
	User(2, "Bob", "bob"),
	User(3, "Charlie", "eilrahc")
]

# Maps are used for efficient lookup (so we don't have to iterate over the whole list)
username_mapping = {u.username: u for u in users} 

# Maps are used for efficient lookup (so we don't have to iterate over the whole list)
userid_mapping = {u.id: u for u in users}

def authenticate(username, password):
	# This is another way to access a dictionary.  And you can specify a default value of the value is not found
	user = username_mapping.get(username, None)
	if user and user.password == password:
		return user

def identity(payload):
	user_id	= payload['identity']
	return userid_mapping.get(user_id, None)