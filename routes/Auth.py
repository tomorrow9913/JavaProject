from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.database import get_db
from crud.Auth import add_user, authenticate_user
from schema.Auth import Response, RegisterReq, Token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register", response_model=Response)
async def register_user(register_req: RegisterReq, db: Session = Depends(get_db)):
    return add_user(db, **register_req.dict())


@router.post("/login", response_model=Token)
async def login(login_req: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return authenticate_user(db, login_req.username, login_req.password)
