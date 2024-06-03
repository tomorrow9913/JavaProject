from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from core.models import User


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_list(db: Session, limit: int, page: int) -> dict:
    users = db.query(User)
    cnt = users.count()

    users = users.limit(limit).offset(page * limit).all()
    users = [user.__dict__ for user in users]
    for user in users:
        user.pop('password')

    return {
        "cnt": cnt,
        "page": page,
        "limit": limit,
        "users": users
    }


def update_user_info(
        db: Session,
        username: str,
        role: str,
        ) -> dict:

    current_user = get_user_by_username(db, username)

    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!"
        )

    db.query(User).filter(current_user.username == username).update({
        "role": role,
    })
    db.commit()

    return {"message": "User information updated successfully!"}


def delete_user(db: Session, username: str) -> dict:
    user = get_user_by_username(db, username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!"
        )

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully!"}