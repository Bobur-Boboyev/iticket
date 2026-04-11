import random
from datetime import datetime, timedelta
import uuid

from sqlalchemy.orm import Session

from app.models import (
    Category, Event, Venue,
    TicketType, Ticket,
    User, Order, OrderItem,
    OrderStatus, PaymentMethod,
    TIcketTypeEnum, TicketStatus, RoleEnum
)
from app.core.security import hash_password
from app.db.session import get_db
from app.db.init_db import init_db


def seed_db(db: Session):
    init_db()

    categories = [
        Category(name="Concert"),
        Category(name="Conference"),
        Category(name="Sport"),
        Category(name="Theatre"),
    ]
    db.add_all(categories)
    db.flush()


    venues = [
        Venue(name="Humo Arena", location="Tashkent"),
        Venue(name="UzExpo Center", location="Tashkent"),
        Venue(name="Bunyodkor Stadium", location="Tashkent"),
    ]
    db.add_all(venues)
    db.flush()


    events = []
    for i in range(5):
        event = Event(
            title=f"Event {i+1}",
            date=datetime.now() + timedelta(days=random.randint(1, 30)),
            category_id=random.choice(categories).id,
            venue_id=random.choice(venues).id
        )
        events.append(event)

    db.add_all(events)
    db.flush()

    ticket_types = []
    for event in events:
        for t_type in [TIcketTypeEnum.STANDART, TIcketTypeEnum.VIP]:
            tt = TicketType(
                name=t_type,
                price=random.uniform(10, 100),
                quantity=50,
                event_id=event.id
            )
            ticket_types.append(tt)

    db.add_all(ticket_types)
    db.flush()

    tickets = []
    for tt in ticket_types:
        for _ in range(tt.quantity):
            ticket = Ticket(
                status=TicketStatus.AVAILABLE
            )
            tickets.append(ticket)

    db.add_all(tickets)
    db.flush()

    users = [
        User(
            role=RoleEnum.ADMIN,
            first_name="Admin",
            last_name="User",
            username="admin",
            email="admin@example.com",
            password_hash=hash_password("11111111")
        ),
        User(
            role=RoleEnum.USER,
            first_name="John",
            last_name="Doe",
            username="johndoe",
            email="john@example.com",
            password_hash=hash_password("11111111")
        ),
    ]
    db.add_all(users)
    db.flush()

    orders = []
    for user in users:
        order = Order(
            user_id=user.id,
            status=OrderStatus.PENDING,
            payment_method=None
        )
        orders.append(order)

    db.add_all(orders)
    db.flush()

    order_items = []
    for order in orders:
        tt = random.choice(ticket_types)

        selected_tickets = random.sample(tickets, 2)

        for t in selected_tickets:
            item = OrderItem(
            order_id=order.id,
            ticket_type_id=tt.id,
            ticket_id=t.id
        )
            
            db.add(item)
            db.flush()

            t.status = TicketStatus.RESERVED

        order_items.append(item)

    db.add_all(order_items)
    db.commit()


seed_db(next(get_db()))