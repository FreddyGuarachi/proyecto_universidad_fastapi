from fastapi import APIRouter, status

from app.deps.user_deps import UserServiceDep
from app.schemas import user

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=user.UserResponse, status_code=status.HTTP_201_CREATED)
def create(service: UserServiceDep, user_data: user.UserCreate):
    return service.create(user_data)
