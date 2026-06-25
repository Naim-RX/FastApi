from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()

class course(BaseModel):
    name:str
    instructor : str
    duration: float
    website: HttpUrl

@app.post("/post")
def create_post(post : course):
    return {"data":post}
@app.get("/")
def aiquest():
    return {"Django":"API"}

@app.get("/course")
def aiquestcourse():
    return {"CSE101":"Programming and problem solving"}