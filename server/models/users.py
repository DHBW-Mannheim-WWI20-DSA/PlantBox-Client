import uuid
from enum import Enum
from datetime import datetime, date
from typing import Optional, List, Union
from pydantic import BaseModel, EmailStr, Field
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.validators import MaxLengthValidator, MinLengthValidator, RegexValidator


class UserRole(str, Enum):
    """
    User roles for access control
    """
    user = "user"
    admin = "admin"


class User(models.Model):
    """
    User model for the database
    """
    # Index in DB
    uuid = fields.UUIDField(pk=True, default=uuid.uuid4(), index=True, unique=True, null=False, editable=False,
                            description="Unique identifier of the user")
    # Basic info
    username = fields.CharField(max_length=50, null=False, unique=True, description="Username of the user", index=True,
                                validators=[MinLengthValidator(3),
                                            MaxLengthValidator(50)
                                            ])
    email = fields.CharField(max_length=100, null=True, unique=True, description="Email of the user", index=True,
                             validators=[MinLengthValidator(3),
                                         MaxLengthValidator(100)
                                         ])
    first_name = fields.CharField(max_length=50, null=False, description="First title of the user")
    family_name = fields.CharField(max_length=60, null=False, description="Last title of the user")
    hash_password = fields.CharField(max_length=255, null=False, description="Hashed password of the user")
    birth_date = fields.DateField(null=False, description="Birth date of the user")

    # User Roles
    user_role = fields.CharEnumField(UserRole, max_length=255, null=False, default=UserRole.user)
    # Timestamps
    created_at = fields.DatetimeField(auto_now_add=True, description="Creation date of the user")
    updated_at = fields.DatetimeField(auto_now=True, description="Last update date of the user")

    # Status
    is_active = fields.BooleanField(default=True, description="Is the user active", null=False)

    # Relations

    # Methods
    def __str__(self):
        return __dict__()

    def __repr__(self):
        return __dict__()

    # Class methods
    def full_name(self) -> str:
        """
        Returns the best title of the user
        """
        if self.first_name or self.family_name:
            return f"{self.first_name or ''} {self.family_name or ''}".strip()
        return self.username

    def age(self) -> int:
        """
        Returns the age of the user
        """
        today = datetime.today()
        return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    class Meta:
        table = "users"
        table_description = "Users table"

    class PydanticMeta:
        exclude = ["hash_password"]
        computed = ["full_name", "age"]


# Pydantic models
User_Pydantic = pydantic_model_creator(User, name="User")


class UserRegister_Pydantic(BaseModel):
    """
    Pydantic model for user registration
    """

    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=255)
    first_name: str = Field(min_length=1, max_length=50)
    family_name: str = Field(min_length=1, max_length=60)
    birth_date: date
    user_role: UserRole = Field(default=UserRole.user)
    is_active: bool = Field(default=True)

    class Config:
        title = "UserRegister_Pydantic"
        schema_extra = {
            "example": {
                "username": "test",
                "email": "test@test.de",
                "first_name": "Test",
                "family_name": "Test",
                "password": "testtest",
                "birth_date": "1990-01-01",
                "user_role": "user",
                "is_active": True
            }}


class UserLogin_Pydantic(BaseModel):
    """
    Pydantic model for user login
    """
    username: str
    password: str

    class Config:
        title = "UserLogin_Pydantic"
        schema_extra = {
            "example": {
                "username": "test",
                "password": "testtest"
            }}


class UserUpdate_Pydantic(BaseModel):
    """
    Pydantic model for user update
    """
    username: Optional[str]
    email: Optional[EmailStr]
    first_name: Optional[str]
    family_name: Optional[str]
    birth_date: Optional[date]
    user_role: Optional[UserRole]
    is_active: Optional[bool]
    password: Optional[str]

    class config:
        title = "UserUpdate_Pydantic"
        schema_extra = {
            "example": {
                "username": "test",
                "email": "test@test.com",
                "password": "testtest",
                "first_name": "Test",
                "family_name": "Test",
                "birth_date": "1990-01-01",
                "user_role": "user",
                "is_active": True
            }}
