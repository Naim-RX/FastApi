from pydantic import BaseModel, EmailStr,ConfigDict

class Student(BaseModel):
    id: int
    name: str
    email: EmailStr
    dept: str

class studentResponse(Student):
    id : int
    class Config:
        model_config = ConfigDict(from_attributes=True)