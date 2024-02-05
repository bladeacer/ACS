import bcrypt


class HashedPassword:
    def __init__(self, plaintext):
        self.salt = bcrypt.gensalt()
        self.hash = bcrypt.hashpw(bytes(plaintext, "utf-8"), self.salt)

