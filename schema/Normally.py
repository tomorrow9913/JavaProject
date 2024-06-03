from pydantic import BaseModel


class NormallyRes(BaseModel):
    message: str
