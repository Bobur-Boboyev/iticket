from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models import Category, Venue


def seed_categories(session: Session):
    existing = session.execute(select(Category.name)).scalars().all()
    existing_set = set(existing)

    data = [
        "Concert",
        "Sport",
        "Conference",
        "Comedy",
        "E-sports",
    ]

    objects = [Category(name=name) for name in data if name not in existing_set]

    session.add_all(objects)


def seed_venues(session: Session):
    existing = session.execute(select(Venue.name)).scalars().all()
    existing_set = set(existing)

    data = [
        ("Humo Arena", "Tashkent"),
        ("Bunyodkor Stadium", "Tashkent"),
        ("UzExpo Center", "Tashkent"),
    ]

    objects = [
        Venue(name=name, location=location)
        for name, location in data
        if name not in existing_set
    ]

    session.add_all(objects)


def run_seeding(session: Session):
    try:
        seed_categories(session)
        seed_venues(session)

        session.commit()
    except Exception:
        session.rollback()
        raise


if __name__ == "__main__":
    from app.db.session import SessionLocal

    with SessionLocal() as session:
        run_seeding(session)
