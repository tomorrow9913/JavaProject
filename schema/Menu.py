from pydantic import BaseModel


class Menu(BaseModel):
    name: str
    category: str
    price: float
    thumbnail_url: str
    suggestion: int


class MenuList(BaseModel):
    cnt: int
    page: int
    limit: int
    menu: list[Menu]


