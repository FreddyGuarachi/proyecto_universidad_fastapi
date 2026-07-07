from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.user import UserRepository
from app.schemas import user
from app.auth.password import get_password_hash, verify_password


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)

    def create(self, user_data: user.UserCreate):

        if self.repo.find_by_username(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario ya existe"
            )

        hashed_password = get_password_hash(user_data.password)

        user = self.repo.create(
            username=user_data.username,
            password_hash=hashed_password,
        )

        self.db.commit()
        self.db.refresh(user)

        return user

    def authenticate(self, username: str, password: str):
        user = self.repo.find_by_username(username)

        if not user or not verify_password(password, user.password_hash):
            return None

        return user
