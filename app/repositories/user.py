from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, username: str, password_hash: str) -> User:
        user = User(username=username, password_hash=password_hash)

        self.db.add(user)

        return user

    def find_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)

        return self.db.scalar(stmt)
