from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import TicketType, User, Order, OrderItem, Ticket
from app.models.order import OrderStatus
from app.models.ticket import TicketStatus
from app.schemas.order import CreateOrder, OrderResponse, OrderItemResponse, PaymentData, UserOrdersResponse



class OrderService:
    def __init__(self, db: Session):
        self.db = db

    def create_order(self, data: CreateOrder, user: User) -> OrderItemResponse:
        ticket_type = self.db.query(TicketType).filter(TicketType.id == data.ticket_type_id).first()
        if not ticket_type:
            raise HTTPException(status_code=404, detail="Ticket type not found")


        order = self.db.query(Order).filter(Order.user_id == user.id, Order.status == OrderStatus.PENDING).first()

        if not order:
            order = Order(user_id=user.id)
            self.db.add(order)
            self.db.flush()

        ticket = Ticket(status=TicketStatus.RESERVED)
        self.db.add(ticket)
        self.db.flush()

        if ticket_type.quantity <= 0:
            raise HTTPException(status_code=400, detail="No tickets available for this type")

        order_item = OrderItem(
            order_id=order.id,
            ticket_id=ticket.id,
            ticket_type_id=data.ticket_type_id,
            
        )
        ticket_type.quantity -= 1
        self.db.add(ticket_type)
        self.db.add(order_item)
        self.db.commit()

        return order_item
    
    def get_orders_by_user(self, user: User) -> list[OrderResponse]:
        orders = self.db.query(Order).filter(Order.user_id == user.id).all()

        return [
            OrderResponse(
                id=order.id,
                    status=OrderStatus(order.status),
                    payment_method=order.payment_method,
                    user_id=order.user_id,
                    order_items=[
                        OrderItemResponse(
                            id=item.id,
                            ticket_id=item.ticket_id,
                            ticket_type_id=item.ticket_type_id,
                        )
                        for item in order.items
                    ]
                )
                for order in orders
            ]
    
    def get_all_orders(self) -> list[UserOrdersResponse]:
        users = self.db.query(User).all()

        response = []
        for user in users:
            orders = self.get_orders_by_user(user)
            response.append(UserOrdersResponse(user_id=user.id, orders=orders))
        return response
    
    def get_order_by_id(self, order_id: int, user: User) -> OrderResponse:
        order = self.db.query(Order).filter(Order.id == order_id).first()

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        if order.user_id != user.id and user.role != "admin":
            raise HTTPException(status_code=403, detail="Not authorized to view this order")

        return OrderResponse(
            id=order.id,
            status=OrderStatus(order.status),
            payment_method=order.payment_method,
            user_id=order.user_id,
            order_items=[
                OrderItemResponse(
                    id=item.id,
                    ticket_id=item.ticket_id,
                    ticket_type_id=item.ticket_type_id,
                )
                for item in order.items
            ]
        )
    
    def pay_order(self, order_id: int, user: User, payment_data: PaymentData):
        order = self.db.query(Order).filter(Order.id == order_id).first()

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        if order.user_id != user.id and user.role != "admin":
            raise HTTPException(status_code=403, detail="Not authorized to pay for this order")

        if order.status != OrderStatus.PENDING.value:
            raise HTTPException(status_code=400, detail="Only pending orders can be paid for")
        
        for item in order.items:
            ticket = self.db.query(Ticket).filter(Ticket.id == item.ticket_id).first()
            if ticket:
                ticket.status = TicketStatus.SOLD.value
                self.db.add(ticket)

        order.payment_method = payment_data.payment_method
        order.status = OrderStatus.PAID.value

        self.db.commit()

        return True
    
    def cancel_order(self, order_id: int, user: User):
        order = self.db.query(Order).filter(Order.id == order_id).first()

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        if order.user_id != user.id and user.role != "admin":
            raise HTTPException(status_code=403, detail="Not authorized to cancel this order")
        
        if order.status == OrderStatus.CANCELLED:
            raise HTTPException(status_code=400, detail="Order has been already cancelled")
        
        order.status = OrderStatus.CANCELLED.value

        for item in order.items:
            ticket_type = self.db.query(TicketType).filter(TicketType.id == item.ticket_type_id).first()
            ticket = self.db.query(Ticket).filter(Ticket.id == item.ticket_id).first()
            if ticket:
                ticket.status = TicketStatus.CANCELLED.value
                self.db.add(ticket)

            if ticket_type:
                ticket_type.quantity += 1
                self.db.add(ticket_type)

        self.db.commit()

        return True
    
    def refund_order(self, order_id: int, admin: User):
        order = self.db.query(Order).filter(Order.id == order_id).first()

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        if admin.role != "admin":
            raise HTTPException(status_code=403, detail="Not authorized to refund this order")
        
        if order.status != OrderStatus.PAID.value:
            raise HTTPException(status_code=400, detail="Only paid orders can be refunded")

        order.status = OrderStatus.REFUNDED.value

        for item in order.items:
            ticket_type = self.db.query(TicketType).filter(TicketType.id == item.ticket_type_id).first()
            ticket = self.db.query(Ticket).filter(Ticket.id == item.ticket_id).first()
            if ticket:
                ticket.status = TicketStatus.CANCELLED.value
                self.db.add(ticket)

            if ticket_type:
                ticket_type.quantity += 1
                self.db.add(ticket_type)

        self.db.commit()

        return True