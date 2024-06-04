from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from core.models import Menu


# Create
def add_menu(db: Session, name: str, category: str, price: float, thumbnail_url: str, suggestion: int):
    menu = db.query(Menu).filter(Menu.name == name).first()
    if menu is not None:
        return {"message": "Menu already exists!"}
    menu = Menu(name=name, category=category, price=price, thumbnail_url=thumbnail_url, suggestion=suggestion)
    db.add(menu)
    db.commit()
    return {"message": "Menu add successfully"}


# Read
def get_menu(db: Session, menu_name: str):
    menu = db.query(Menu).filter(Menu.name == menu_name).first()
    if menu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu not found!"
        )
    return menu


def get_category_list(db: Session):
    product = db.query(Menu).distinct(Menu.category).all()
    product = set([p.category for p in product])
    return product


def get_menu_list(db: Session, page: int, limit: int, category: str = None):
    menu = db.query(Menu)

    if category is not None:
        menu.filter(Menu.category == category)

    cnt = menu.count()

    menu = menu.limit(limit).offset(page * limit).all()
    menu = [p.__dict__ for p in menu]

    return {
        "cnt": cnt,
        "page": page,
        "limit": limit,
        "menu": menu
    }


# Update
def update_menu(db: Session, menu_name:str, name: str, category: str, price: int, thumbnail_url: str, suggestion: int):
    menu = db.query(Menu).filter(Menu.name == menu_name).first()

    if menu is None:
        return {"message": "Menu not found!"}

    db.query(Menu).filter(Menu.name == menu_name).update({
        "name": name,
        "category": category,
        "price": price,
        "thumbnail_url": thumbnail_url,
        "suggestion": suggestion
    })
    db.commit()

    return {"message": "Menu updated successfully"}


# Delete
def delete_menu(db: Session, menu_name):
    product = db.query(Menu).filter(Menu.name == menu_name).first()

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu not found!"
        )

    db.delete(product)
    db.commit()

    return {"message": "Menu deleted successfully!"}
