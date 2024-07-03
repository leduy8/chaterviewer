import re
from datetime import datetime

from pydantic import BaseModel, EmailStr, constr, field_validator


class AuthBaseRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    def password_length(cls, value, values):
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,128}$"
        if not re.search(pattern, value):
            raise ValueError(
                "Password must contain at least 1 uppercase, 1 lowercase, 1 number, and 1 special character"
            )
        return value


class SignUpRequest(AuthBaseRequest):
    name: str


class SignUpResponse(BaseModel):
    uuid: constr(min_length=32, max_length=32)  # Length 32 due to convert to hex
    email: EmailStr
    name: str
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        from_attributes = True


class LoginRequest(AuthBaseRequest):
    pass


class LoginResponse(BaseModel):
    access_token: str
