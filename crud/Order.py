import traceback
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from core.models import Order, OrderMenu
from crud.Menu import get_menu
from schema.Order import Order as OrderDto, OrderInfo
from schema.Order import OrderReq


def create_new_order(db: Session):
    now = datetime.now()
    order = Order(order_time=now)
    db.add(order)
    db.commit()

    return db.query(Order).filter(Order.order_time == now).first()


def add_order(db: Session, orders: list[OrderDto]):
    order_info = create_new_order(db)
    try:
        for order in orders:
            if order.quantity <= 0:
                continue

            new_order = OrderMenu(
                order_id=order_info.id,
                order_menu=order.name,
                order_cnt=order.quantity
            )
            db.add(new_order)
            db.commit()

        return {
            "order": {
                "id": order_info.id,
                "order_time": order_info.order_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
                "progress": order_info.progress
            },
            "order_list": orders,
            "total_price": get_price(db, OrderReq(order_list=orders))
    }
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: insert order failed! {e}"
        )


def get_order_by_id(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found!"
        )

    order_menu = db.query(OrderMenu).filter(OrderMenu.order_id == order_id).all()
    order_menu = [{"name": o.order_menu, "quantity": o.order_cnt} for o in order_menu]

    return {
        "order": {
            "id": order.id,
            "order_time": order.order_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
            "progress": order.progress
        },
        "order_list": order_menu,
        "total_price": get_price(db, OrderReq(order_list=order_menu))
    }


def get_price(db: Session, menu_list: OrderReq) -> int:
    orders = menu_list.order_list

    price = 0
    for order in orders:
        price += order.quantity * get_menu(db, order.name).price

    return price


def order_menu_list(db: Session, order_id: int):
    return db.query(OrderMenu).filter(OrderMenu.order_id == order_id).all()


def get_order_list(db: Session, page: int, limit: int):
    order = db.query(Order)

    cnt = order.count()

    order = order.limit(limit).offset(page * limit).all()
    order = [get_order_by_id(db, o.id) for o in order]

    return {
        "cnt": cnt,
        "page": page,
        "limit": limit,
        "orders": order
    }


def get_order_desc(orders: list[OrderDto]):
    products_desc = f"{orders[0].menu_name}"

    if len(orders) > 1:
        products_desc += f" 외 {len(orders) - 1}개 상품"

    return products_desc


def update_state(db: Session, order_id: int, state: int):
    order_type = {
        -1: "Refund",
        0: "Preparing",
        1: "Completion"
    }

    order = db.query(Order).filter(Order.id == order_id).first()

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found!"
        )

    db.query(Order).filter(Order.id == order_id).update({
        "id": order_id,
        "order_time": order.order_time,
        "progress": state
    })
    db.commit()

    return {"message": f"Order updated '{order_type[state]}' successfully"}
