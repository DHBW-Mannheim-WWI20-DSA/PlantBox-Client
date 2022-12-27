import uuid
from pydantic import BaseModel
from typing import Union


class Token(BaseModel):
    """
    Pydantic model for token
    """
    access_token: str
    token_type: str

    class Config:
        title = "Token"
        schema_extra = {
            "example": {
                "access_token": "string",
                "token_type": "bearer"
            }}


class TokenData(BaseModel):
    """
    Pydantic model for token data
    """
    username: Union[str, None] = None
    uuid: Union[str, None] = None

    class Config:
        title = "TokenData"
        schema_extra = {
            "example": {
                "username": "string",
                "uuid": "8049afd0-35f7-4537-a069-d343188c9b6a"
            }}
