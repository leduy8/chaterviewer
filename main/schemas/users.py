from datetime import datetime

from pydantic import BaseModel, EmailStr, constr


class UserRequest(BaseModel):
    name: str


class UserResponse(BaseModel):
    uuid: constr(min_length=32, max_length=32)  # Length 32 due to convert to hex
    email: EmailStr
    name: str
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        from_attributes = True
