import secrets

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Key:
    """
        Object for Securing an API
    """
    length_int: int
    key_hash: str
    pwd_context: CryptContext

    def __init__(self, length_int: int = 32):
        """
            Constructor
        """
        self.length_int = length_int
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.key_hash = self.hash_key()

    def create_key(self) -> str:
        """
            Create a key
        """
        return secrets.token_urlsafe(self.length_int)

    def hash_key(self) -> str:
        """
            Hash a key
        """
        return self.pwd_context.hash(self.create_key())

    def verify_key(self, key: str) -> bool:
        """
            Verify a key
        """
        return self.pwd_context.verify(key, self.key_hash)

    def __str__(self):
        """
            String representation
        """
        return self.key_hash


if __name__ == "__main__":
    print(Key(
        length_int= int(input("Enter the length of the key: "))
    ))
