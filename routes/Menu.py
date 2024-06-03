from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

import crud.Menu as MenuCRUD
from core.database import get_db
from schema.Menu import Menu, MenuList
from schema.Normally import NormallyRes
from utils.oauth import get_current_user

router = APIRouter(
    prefix="/menu",
    tags=["Menu"]
)


# Create
@router.post("/", response_model=NormallyRes)
async def add_new_menu(
        menu: Menu,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)):
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized!"
        )

    return MenuCRUD.add_menu(db, **menu.__dict__)


# Read
@router.get("/category/", response_model=List[str])
async def get_category_list(db: Session = Depends(get_db)):
    return MenuCRUD.get_category_list(db)


@router.get("/category/{category}", response_model=MenuList)
async def get_menu_list(category: str, page: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return MenuCRUD.get_menu_list(db, page, limit, category)


@router.get("/{menu_name}", response_model=Menu)
async def get_menu(menu_name: str, db: Session = Depends(get_db)):
    return MenuCRUD.get_menu(db, menu_name)


# Update
@router.put("/{menu_name}", response_model=NormallyRes)
async def update_product(
        menu_name: str,
        menu: Menu,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)):
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized!"
        )

    return MenuCRUD.update_product(db, menu_name, **menu.__dict__)


# Delete
@router.delete("/{menu_name}", response_model=NormallyRes)
async def delete_product(menu_name: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized!"
        )
    return MenuCRUD.delete_menu(db, menu_name)
