from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from server.models.users import UserRole, User, User_Pydantic, UserRegister_Pydantic, UserLogin_Pydantic
from server.routers.users import create_user
from server.dependencies import verify_password

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


# Login user
@router.post("/login", response_model=User_Pydantic)
async def login_user(user: UserLogin_Pydantic):
    user_obj = await User.get(username=user.username)
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(user.password, user_obj.hash_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    return await User_Pydantic.from_tortoise_orm(user_obj)


# Register user
@router.post("/register", response_model=User_Pydantic)
async def register_user(user: UserRegister_Pydantic):
    user_obj = await User.get(username=user.username)
    if user_obj:
        raise HTTPException(status_code=400, detail="Username already registered")
    return await create_user(user)
