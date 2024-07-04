from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm.session import Session

from app.database import get_db
from app.models.users import User
from app.schemas.users import UserRequest, UserResponse
from app.services import users as user_service
from app.utils.dependencies import authenticate_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def get_user_info(user: User = Depends(authenticate_user), db: Session = Depends(get_db)):
    return user


@router.put("/info", response_model=UserResponse)
async def update_user_info(
    user: User = Depends(authenticate_user),
    data: UserRequest = Body(...),
    db: Session = Depends(get_db),
):
    return user_service.update_user(db, user.uuid, data)
