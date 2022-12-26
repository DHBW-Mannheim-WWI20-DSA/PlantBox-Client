from fastapi import APIRouter, Depends, HTTPException, status


router = APIRouter(
    tags=["root"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def welcome_PlantBox():
    return {"message": "Welcome to the PlantBox API!"}
