from pydantic import BaseModel, EmailStr,ConfigDict
from typing import Optional
class Student(BaseModel):
    id: int
    name: str
    email: EmailStr
    dept: str

class studentResponse(Student):
    id : int
    class Config:
        model_config = ConfigDict(from_attributes=True)

#this is for verifying hashed password
class UserLogin(BaseModel):
    email : EmailStr
    password : str


#verifying access token
class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[int] = None