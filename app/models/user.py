from pydantic import BaseModel

class LoginPayLoad(BaseModel):
    username: str
    password: str

