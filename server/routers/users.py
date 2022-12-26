import uuid
from typing import List
from server.dependencies import verify_password, get_password_hash
from fastapi import APIRouter, Depends, HTTPException, status
from server.models.users import UserRole, User, User_Pydantic, UserRegister_Pydantic, UserLogin_Pydantic, \
    UserUpdate_Pydantic

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


# Get all users
@router.get("/", response_model=List[User_Pydantic])
async def get_all_users():
    return await User_Pydantic.from_queryset(User.all())


# Get user by uuid
@router.get("/{uuid}", response_model=User_Pydantic)
async def get_user(uuid: uuid.UUID):
    return await User_Pydantic.from_queryset_single(User.get(uuid=uuid))


# Create user
@router.post("/", response_model=User_Pydantic)
async def create_user(user: UserRegister_Pydantic):
    user_obj = await User.create(**user.dict(exclude_unset=True), hash_password=get_password_hash(user.password))
    return await User_Pydantic.from_tortoise_orm(user_obj)


# Update user
@router.put("/{uuid}", response_model=User_Pydantic)
async def update_user(uuid: uuid.UUID, user: UserUpdate_Pydantic):
    hashed_value = get_password_hash(user.password) if user.password else None
    await User.filter(uuid=uuid).update(**user.dict(exclude_unset=True, exclude={"password"}),
                                        hash_password=hashed_value)
    return await User_Pydantic.from_queryset_single(User.get(uuid=uuid))


# Delete user
@router.delete("/{uuid}", response_model=str)
async def delete_user(uuid: uuid.UUID) -> str:
    deleted_count = await User.filter(uuid=uuid).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {uuid} not found")
    return f"Deleted user with uuid: {uuid}"
