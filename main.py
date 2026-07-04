# This imports the FastAPI class from the FastAPI package.
from fastapi import FastAPI
# Imports the BaseModel class from the Pydantic library.
# Pydantic is responsible for data validation and data parsing in FastAPI.
from pydantic import BaseModel,EmailStr
# This imports the MySQL Connector library.
import mysql.connector

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