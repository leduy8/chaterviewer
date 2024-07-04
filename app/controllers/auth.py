from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm.session import Session

from app.database import get_db
from app.schemas.auth import LoginRequest, LoginResponse, SignUpRequest, SignUpResponse
from app.services import auth as auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=SignUpResponse)
async def signup(data: SignUpRequest = Body(...), db: Session = Depends(get_db)):
    return auth_service.signup(db, data)


@router.post("/login", response_model=LoginResponse)
async def login(data: LoginRequest = Body(...), db: Session = Depends(get_db)):
    return auth_service.login(db, data)
