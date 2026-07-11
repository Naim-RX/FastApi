from fastapi import FastAPI, HTTPException , status, Depends,APIRouter
from .. import model,schema
from sqlalchemy.orm import Session
from ..database import engine , get_db

router = APIRouter(
    prefix="/BBaStudent",
    tags= ['BBA']
    )

@router.post("/", response_model=schema.studentResponse)
# FastAPI expects JSON from the client.
# FastAPI creates a SQLAlchemy database session and passes it to the function.
def get_students(student: schema.Student, db: Session = Depends(get_db)):
#     This creates a new SQLAlchemy model object.
# Nothing has been inserted into MySQL yet.
# It is simply a Python object.
    new_student=model.Student(
        **student.model_dump()
    )
#     Adds the object to the SQLAlchemy session.
# At this point, the data is not yet stored in MySQL.
# Think of it as placing the new record into a queue of pending changes.
    db.add(new_student)
    # Now the record is permanently stored in the database.
    db.commit()
    # Reloads the object from the database
    db.refresh(new_student)

    return new_student

@router.get("/{id}",response_model= schema.studentResponse)
def get_student(id: int, db: Session = Depends(get_db)):
    student = db.query(model.Student).filter(model.Student.id == id).first()

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Student not found"
        )

    return student


# Handles PUT requests to update an existing student using their ID.
@router.put("/{id}",response_model=schema.studentResponse)
def update_student(
    # Receives the student ID from the URL.
    id: int,
    # Receives and validates the JSON request body using the Student schema.
    updated_student: schema.Student,
    # Creates and injects a SQLAlchemy database session.
    db: Session = Depends(get_db)
):
    # Creates a query to find the student with the given ID.
    student = db.query(model.Student).filter(model.Student.id == id)
    # Executes the query and checks whether the student exists.
    if student.first() is None:
        # Raises a 404 error if no matching student is found.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    # Converts the Pydantic model into a dictionary and excludes the ID.
    update_data = updated_student.model_dump(exclude={"id"})
    # Updates the matching database row with the new values.
    student.update(update_data, synchronize_session=False)
    # Saves the changes permanently to the database.
    db.commit()
    # Retrieves and returns the updated student record.
    return student.first()



# Delete student using ID
@router.delete("/{id}")
def delete_student(id: int, db: Session = Depends(get_db)):
    
    # Creates a query to find the student with the given ID.
    student = db.query(model.Student).filter(model.Student.id == id)

    # Executes the query and checks whether the student exists.
    if student.first() is None:
        # Raises a 404 error if no matching student is found.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    # Deletes the matching student record.
    student.delete(synchronize_session=False)

    # Permanently saves the changes to the database.
    db.commit()

    # Returns a success message.
    return {"message": "Student record deleted successfully"}