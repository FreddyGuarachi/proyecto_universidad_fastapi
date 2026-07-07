from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from .schemas import Token
from .jwt import create_access_token
from .auth_dependencies import credentials_exception

from app.deps.user_deps import UserServiceDep

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
def login(service: UserServiceDep, form_data: OAuth2PasswordRequestForm = Depends()):
    user = service.authenticate(form_data.username, form_data.password)

    if not user:
        raise credentials_exception

    token = create_access_token({"sub": user.username})

    return {"access_token": token, "token_type": "bearer"}
