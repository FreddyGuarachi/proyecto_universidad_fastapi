from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from .jwt import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
)


def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = verify_token(token)

    except InvalidTokenError:
        raise credentials_exception

    username = payload.get("sub")

    if username is None:
        raise credentials_exception

    return username
