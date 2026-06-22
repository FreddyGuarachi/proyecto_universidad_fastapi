from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.schemas import user


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)

    def create(self, user_data: user.UserCreate):
        user_exists = self.repo.find_by_username(user_data.username)

        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario ya existe"
            )

        user_db = self.repo.create(user_data)

        self.db.commit()
        self.db.refresh(user_db)

        return user_db
