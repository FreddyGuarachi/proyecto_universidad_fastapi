from fastapi import APIRouter, status

from app.deps.user_deps import UserRepositoryDep
from app.schemas import user

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=user.UserCreate, status_code=status.HTTP_201_CREATED)
def create(service: UserRepositoryDep, user_data: user.UserCreate):
    return service.create(user_data)
