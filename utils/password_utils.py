import bcrypt


def hash_password(password: str) -> str:
    """
    Hash plain password and return string (JSON serializable)
    """
    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")


def check_password(password: str, hashed: str) -> bool:
    """
    Verify password with hashed password
    """
    password_bytes = password.encode("utf-8")
    hashed_bytes = hashed.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)
