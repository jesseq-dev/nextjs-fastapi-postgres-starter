from sqlalchemy import select
from sqlalchemy.orm import Session
from db_engine import sync_engine
from models import User, Thread


def seed_user_if_needed():
    with Session(sync_engine) as session:
        with session.begin():
            if session.execute(select(User)).scalar_one_or_none() is not None:
                print("User already exists, skipping seeding")
                return
            print("Seeding user")
            session.add(User(name="Alice"))
            session.commit()


def seed_threads_if_needed():
    with Session(sync_engine) as session:
        with session.begin():
            user = session.execute(select(User)).scalars().first()
            if user is None:
                print("No user found, seeding user first")
                user = User(name="Alice")
                session.add(user)
                session.commit()
                session.refresh(user)

            if session.execute(select(Thread).filter_by(user_id=user.id)).scalars().first() is not None:
                print("Thread already exists for user, skipping seeding")
                return
            print("Seeding thread")
            session.add(Thread(user_id=user.id))
            session.commit()