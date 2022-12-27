from pydantic import BaseModel


class SignInSchema(BaseModel):
    email: str
    password: str


class SignUpSchema(BaseModel):
    username: str
    email: str
    password: str
