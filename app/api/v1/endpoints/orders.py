from typing import Annotated

from fastapi import APIRouter, Depends, Path, Body
from sqlalchemy.orm import Session

from app.services.order_service import OrderService
from app.schemas.order import CreateOrder, OrderItemResponse, OrderResponse, UserOrdersResponse, PaymentData
from app.core.security import get_admin, get_user
from app.db.session import get_db
from app.models.user import User


router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.post("/", response_model=OrderItemResponse, status_code=201)
async def create_order_view(
    data: Annotated[CreateOrder, Body()],
    user: Annotated[User, Depends(get_user)],
    db: Annotated[Session, Depends(get_db)],
):
    order_service = OrderService(db)
    order = order_service.create_order(data, user)

    return order


@router.get("/my", response_model=list[OrderResponse])
async def my_orders_view(
    user: Annotated[User, Depends(get_user)],
    db: Annotated[Session, Depends(get_db)],
):
    order_service = OrderService(db)
    orders = order_service.get_orders_by_user(user)

    return orders


@router.get("/", response_model=list[UserOrdersResponse])
async def all_orders_view(admin: Annotated[User, Depends(get_admin)], db: Annotated[Session, Depends(get_db)]):
    order_service = OrderService(db)
    orders = order_service.get_all_orders()

    return orders


@router.get("/{id}", response_model=OrderResponse)
async def get_order_view(
    id: Annotated[int, Path()],
    user: Annotated[User, Depends(get_user)],
    db: Annotated[Session, Depends(get_db)],
):
    order_service = OrderService(db)
    order = order_service.get_order_by_id(id, user)

    return order


@router.post("/{id}/pay")
async def pay_order_view(
    id: Annotated[int, Path()],
    data: Annotated[PaymentData, Body()],
    user: Annotated[User, Depends(get_user)],
    db: Annotated[Session, Depends(get_db)],
):
    order_service = OrderService(db)
    order_service.pay_order(id, user, data)

    return {"message": "Order paid successfully"}


@router.post("/{id}/cancel", response_model=None)
async def cancel_order_view(
    id: Annotated[int, Path()],
    user: Annotated[User, Depends(get_user)],
    db: Annotated[Session, Depends(get_db)],
):
    order_service = OrderService(db)
    order_service.cancel_order(id, user)

    return {"message": "Order cancelled successfully"}


@router.post("/{id}/refund", response_model=None)
async def refund_order_view(
    id: Annotated[int, Path()],
    admin: Annotated[User, Depends(get_admin)],
    db: Annotated[Session, Depends(get_db)],
):
    order_service = OrderService(db)
    order_service.refund_order(id, admin)

    return {"message": "Order refunded successfully"}