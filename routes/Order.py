from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

import crud.Order as OrderCRUD
from core.database import get_db
from schema.Normally import NormallyRes
from schema.Order import OrderReq, OrderUpdateReq, OrderRes, OrderListRes
from utils.oauth import get_current_user

router = APIRouter(
    prefix="/orders",
    tags=["Order"]
)


# Create
@router.post("/", response_model=OrderRes)
async def create_new_order(
        order: OrderReq,
        db: Session = Depends(get_db)):

    if len(order.order_list) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No order list!"
        )
    return OrderCRUD.add_order(db, order.order_list)


# Read
@router.get("/sales")
def get_sales(date: str, db: Session = Depends(get_db)):
    y, m, d = map(int, date.split('-'))
    return OrderCRUD.get_sales(db, y, m, d)


@router.get("/{order_id}", response_model=OrderRes)
async def read_order_by_id(
        order_id: int,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)):
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized!"
        )

    return OrderCRUD.get_order_by_id(db, order_id)


@router.get("/", response_model=OrderListRes)
async def read_all_order(
        limit: int = 10,
        page: int = 0,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)):
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized!"
        )

    return OrderCRUD.get_order_list(db, page, limit)


# Update
@router.put("/{order_id}", response_model=NormallyRes)
async def order_state_update(
        order_id: int,
        state: OrderUpdateReq,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)):

    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized!"
        )

    return OrderCRUD.update_state(db, order_id, state.state)
