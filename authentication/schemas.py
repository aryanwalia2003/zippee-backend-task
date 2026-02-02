from pydantic import BaseModel, EmailStr, constr

class RegisterSchema(BaseModel):
    username: constr(min_length=3, max_length=150)
    email: EmailStr
    password: constr(min_length=6)

class LoginSchema(BaseModel):
    username: str
    password: str
