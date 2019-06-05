#usernames to public key hash table
u2k = {}


def add_user(user):
    u2k[user.username] = user.pKey
