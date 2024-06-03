from typing import Optional

from pydantic import BaseModel


class RegisterReq(BaseModel):
    username: str
    password: str
    full_name: str
    address: Optional[str] = None
    payment_info: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str
    username: str
    role: str


class Response(BaseModel):
    message: str
    user: Optional[dict] = None
