from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

import crud.Users as UsersCRUD
from core.database import get_db
from core.models import User
from schema.Normally import NormallyRes
from schema.User import User as UsrDto
from utils.oauth import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# Create is in Auth.py

# Update
@router.put("/", response_model=NormallyRes)
async def update_user_info(
        update_info: UsrDto,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    if current_user.role != 'admin' and current_user.username != update_info.username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized!"
        )

    if current_user.role != 'admin' and current_user.role != update_info.role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized!"
        )

    return UsersCRUD.update_user_info(db, **update_info.dict())


# Delete
@router.delete("/{username}", response_model=NormallyRes)
async def delete_user_endpoint(
        username: str,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    if current_user.role != 'admin' or current_user.username != username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized!"
        )

    return UsersCRUD.delete_user(db, username)
