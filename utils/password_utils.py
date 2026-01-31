import bcrypt


def hash_password(password):
    
    if isinstance(password, str):
        password = password.encode("utf-8")

    return bcrypt.hashpw(password, bcrypt.gensalt())


def check_password(password, hashed):
    if isinstance(password, str):
        password = password.encode("utf-8")

    if isinstance(hashed, str):
        hashed = hashed.encode("utf-8")

    return bcrypt.checkpw(password, hashed)
