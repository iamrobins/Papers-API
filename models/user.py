from pydantic import BaseModel, EmailStr


class UserModel(BaseModel):
    email: EmailStr
    username: str
    password: str
    class Config:
        schema_extra = {
            "example": {
                "username": "alex",
                "email": "alex@gmail.com",
                "password": "1234"
            }
        }

class UserLoginModel(BaseModel):
    email: EmailStr
    password: str