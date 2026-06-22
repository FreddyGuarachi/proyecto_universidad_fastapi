from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas import user


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_data: user.UserCreate):
        user_db = User(**user_data.model_dump())
        self.db.add(user_db)

        return user_db

    def find_by_username(self, username: str):
        stmt = select(User).where(User.username == username)

        return self.db.scalar(stmt)

    def find_by_id(self, user_id: int):
        stmt = select(User).where(User.id == user_id)

        return self.db.scalar(stmt)
