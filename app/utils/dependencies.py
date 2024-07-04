import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm.session import Session

from app.database import get_db
from app.exceptions import InvalidAuthorizationError, MissingAuthorizationError
from app.services.users import find_user_by_uuid
from app.utils.jwt import get_jwt_payload, get_jwt_token


async def authenticate_user(
    request: Request,
    bearer: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
    db: Session = Depends(get_db),
):
    try:
        token = get_jwt_token(auth_header=request.headers.get("Authorization"))
    except (MissingAuthorizationError, InvalidAuthorizationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is either missing or invalid",
        )

    try:
        data = get_jwt_payload(token)
        user = find_user_by_uuid(db, data["uuid"])

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")

        return user
    except jwt.DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
