import os
import uuid
from datetime import datetime, timedelta
from typing import Union
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from fastapi import APIRouter, Depends, HTTPException, status
from server.models.token import Token, TokenData
from server.models.users import UserRole, User, User_Pydantic, UserRegister_Pydantic, UserLogin_Pydantic
from server.dependencies import verify_password, oauth2_scheme, get_password_hash


# Helper function to create access token
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    # Load the secret key from the environment
    load_dotenv()
    secret_key = os.getenv("JWT_SECRET_KEY")
    algorithm = os.getenv("JWT_ALGORITHM") if os.getenv("JWT_ALGORITHM") else "HS256"

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Load the secret key from the environment
    load_dotenv()
    secret_key = os.getenv("JWT_SECRET_KEY"),
    algorithm = os.getenv("JWT_ALGORITHM") if os.getenv("JWT_ALGORITHM") else "HS256"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        uuid_str: str = payload.get("uuid")
        if uuid_str is None:
            raise credentials_exception
        token_data = TokenData(username=username, uuid=uuid_str)
    except JWTError:
        raise credentials_exception
    user = await User.filter(uuid=uuid.UUID(token_data.uuid)).get_or_none()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.is_active is False:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


# Login user
@router.post("/login", response_model=Token)
async def login_user(user: OAuth2PasswordRequestForm = Depends()):
    user_obj = await User.get(username=user.username)
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(user.password, user_obj.hash_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    load_dotenv()
    access_token_expires = timedelta(hours=int(os.getenv("JWT_EXP_DELTA_HOURS")))
    claims = {"sub": user_obj.username, "uuid": str(user_obj.uuid)}
    access_token = create_access_token(
        data=claims, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Register user
#@router.post("/register", response_model=User_Pydantic)
#async def register_user(user: UserRegister_Pydantic):
#    user_obj = await User.get(username=user.username)
#    if user_obj:
#        raise HTTPException(status_code=400, detail="Username already registered")
#    user_obj = await User.get(email=user.email)
#    if user_obj:
#        raise HTTPException(status_code=400, detail="Email already registered")
#    user_obj = await User.create(**user.dict(exclude_unset=True), hash_password=get_password_hash(user.password))
#    return await User_Pydantic.from_tortoise_orm(user_obj)
