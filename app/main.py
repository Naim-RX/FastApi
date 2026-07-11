# This imports the FastAPI class from the FastAPI package.
from fastapi import FastAPI, HTTPException , status, Depends
# Imports the BaseModel class from the Pydantic library.
# Pydantic is responsible for data validation and data parsing in FastAPI.
from pydantic import BaseModel,EmailStr
# This imports the MySQL Connector library.
import mysql.connector
from . import model,schema
from sqlalchemy.orm import Session
from .database import engine , get_db
from . routers import bbaStudent


# This creates an instance (object) of the FastAPI application.
app = FastAPI()

# This is called a decorator.
@app.get("/students")
# This function contains all the logic needed to retrieve students.
def get_students():
    # This opens a connection to the MySQL database.
    conn = mysql.connector.connect(
        # This tells Python where MySQL is running.
        host="localhost",
        # This is the MySQL username.
        user="root",
        password="naim.123",
        database="college"
    )
    # A cursor is an object that sends SQL statements to MySQL and retrieves the results.
    cursor = conn.cursor(dictionary=True)
    # The cursor sends this SQL command to MySQL.
    cursor.execute("SELECT * FROM cse")
    # fetchall() retrieves every row and stores them in students
    students = cursor.fetchall()

    cursor.close()
    # This closes the connection to MySQL.
    conn.close()
    # FastAPI automatically converts it into JSON.
    return students

# Creates a class named Student that represents the structure of the JSON data your API expects.
class Student(BaseModel):
    id : int
    name : str
    email : EmailStr
    dept : str

# Registers an API endpoint.
@app.post("/students")
# Defines the function that handles the POST request.
# Read the JSON body from the request, validate it using the Student model, then create a Student object and pass it into this function.
def add_student(student : Student):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="naim.123",
        database="college"
    )
    cursor = conn.cursor()
    # This is your SQL command.
    query = """INSERT INTO cse (id,name,email,dept) VALUES (%s,%s,%s,%s)""" 
    # Creates a tuple containing the values to replace the placeholders.
    values= (
        student.id,
        student.name,
        student.email,
        student.dept,
    )
    # This sends the SQL command and its values to MySQL.
    cursor.execute(query,values)
    # This permanently saves the changes to the database.
    conn.commit()
    cursor.close()
    conn.close()
    return {"message" : "Student added successfully"}


# To fetch one student by ID
@app.get("/students/{id}")
def get_student(id:int):
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "naim.123",
        database = "college"
    )
    cursor = conn.cursor(dictionary=True)
    query = """select * from cse where id = %s"""
    # The comma in (id,) makes it a single-element tuple, which cursor.execute() expects for query parameters.
    cursor.execute(query,(id,))
    Student = cursor.fetchone()
    # Checks whether fetchone() returned None
    if not Student:
        # If no matching student exists:
        # FastAPI stops executing the function and returns an HTTP 404 Not Found response:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= f"Course with id {id} was not found"
        )
    cursor.close()
    conn.close()

    return Student


# To delete a record by its id
@app.delete("/students/{id}")
def delete_student(id : int):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="naim.123",
        database="college"
    )
    cursor = conn.cursor(dictionary=True)
    # Check if the student exists
    cursor.execute("SELECT * FROM cse WHERE id = %s", (id,))
    student = cursor.fetchone()
    if not student:
        cursor.close()
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {id} was not found"
        )
    # Delete the student
    cursor.execute("DELETE FROM cse WHERE id = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return {"message": f"Student with id {id} deleted successfully"}


class StudentPut(BaseModel):
    name : str
    email : EmailStr
    dept : str

# To update a record by ID
@app.put("/students/{id}")
def update_student(id:int , student:StudentPut):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="naim.123",
        database="college"
    )
    cursor = conn.cursor(dictionary=True)

    # Check if the student exists
    cursor.execute("SELECT * FROM cse WHERE id = %s", (id,))
    existing_student = cursor.fetchone()

    if not existing_student:
        cursor.close()
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {id} was not found"
        )
    # Update the student
    query = """
    UPDATE cse
    SET name = %s,
        email = %s,
        dept = %s
    WHERE id = %s
    """
    values = (
        student.name,
        student.email,
        student.dept,
        id
    )
    cursor.execute(query, values)

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": f"Student with id {id} updated successfully"
    }




model.Base.metadata.create_all(bind = engine)

@app.get("/bba")
#     This defines the function that handles the request.
# Session is SQLAlchemy's database session. A session lets you communicate with the database.
# Depends(get_db)
# FastAPI automatically calls the get_db() function.
def course(db:Session = Depends(get_db)):
    return {"status" : "sqlalchemy orm working"}



#Fastapi using sql alchemy

app.include_router(bbaStudent.router)