import uuid
from pydantic import BaseModel
from server.generate_secrets import Key


# Client Register Model
class ClientRegister(BaseModel):
    """
    Pydantic model for client register
    """
    client_id: uuid.UUID = uuid.uuid4()
    client_secret: str = Key(64).key_hash

    def __str__(self):
        return self.json()

    class Config:
        title = "ClientRegister"
        schema_extra = {
            "example": {
                "client_id": "8049afd0-35f7-4537-a069-d343188c9b6a",
                "client_secret": "string"}}


if __name__ == '__main__':
    pass
