from fastapi import APIRouter, HTTPException, Depends
from app.dependencies import get_db
from sqlalchemy.orm import Session
from app.models.student import Student
from app.schema.student import StudentCreate


router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

@router.post("/")
async def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new student.
    """
    
    new_student = Student(
        name=student.name,
        age=student.age,
        branch=student.branch
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@router.get("/{student_id}")
async def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a student by ID.
    """
    
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=404,
            details="Student not found"
        )
    return student

    raise HTTPException(
        status_code=404,
        details="Student not found"
    )
    
@router.put("/{student_id}")
async def update_student(
    student_id: int,
    updated:StudentCreate,
    db: Session = Depends(get_db)
):
    
    """
    Update a student by ID.
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=404,
            details="Student not found"
        )
    student.name = updated.name
    student.age = updated.age
    student.branch = updated.branch
    db.commit()
    db.refresh(student)
    return student
    
    raise HTTPException(
        status_code=404,
        details="Student not found"
    )
    
@router.delete("/{student_id}")
async def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a student by ID.
    """
    
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=404,
            details="Student not found"
        )
    db.delete(student)
    db.commit()
    return {
        "message": "Deleted successfully"
            }
    raise HTTPException(
        status_code=404,
        details="Student not found"
    )

@router.get("/")
async def get_students(branch: str | None = None, db: Session = Depends(get_db)):
    """
    Filter students by branch.
    """
    if branch is None:
        return db.query(Student).all()
    
    return db.query(Student).filter(Student.branch == branch).all()



