from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.schemas import Token
from app.auth.security import create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    if form_data.username != "admin" or form_data.password != "1234":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales invalidas"
        )

    token = create_access_token({"sub": form_data.username})

    return {"access_token": token, "token_type": "bearer"}


@router.get("/admin")
def admin(user: str = Depends(get_current_user)):
    return {"message": "Acceso permitido", "usuario": user}
