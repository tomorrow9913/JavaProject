from datetime import datetime

from pydantic import BaseModel


class Order(BaseModel):
    name: str
    quantity: int


class OrderInfo(BaseModel):
    id: int
    order_time: datetime
    progress: int


class OrderReq(BaseModel):
    order_list: list[Order]


class OrderRes(BaseModel):
    order: OrderInfo
    order_list: list[Order]
    total_price: int


class OrderListRes(BaseModel):
    cnt: int
    page: int
    limit: int
    orders: list[OrderRes]


class OrderUpdateReq(BaseModel):
    state: int
