from fastapi import APIRouter, HTTPException

from app.schema.student import StudentCreate

from app.database import students

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

@router.post("/")
async def create_student(student: StudentCreate):
    """
    Create a new student.
    """
    
    new_student = {
        "id": len(students) + 1,
        "name": student.name,
        "age": student.age,
        "branch": student.branch
    }
    student.append(new_student)
    return new_student

@router.get("/")
async def get_student():
    """
    Get all students.
    """
    return students

@router.get("/{student_id}")
async def get_student(student_id: int):
    """
    Get a student by ID.
    """
    
    for student in students:
        if student["id"] == student.id:
            return student
        
    raise HTTPException(
        status_code=404,
        details="Student not found"
    )
    
@router.put("/{student_id}")
async def update_student(
    student_id: int,
    updated:StudentCreate):
    
    """
    Update a student by ID.
    """
    for student in students:
        if student["id"]==student_id:
            student["name"] = updated.name
            student["age"] = updated.age
            student["branch"] = updated.branch
            return student
    
    raise HTTPException(
        status_code=404,
        details="Student not found"
    )
    
@router.delete("/{student_id}")
async def delete_student(
    student_id: int
):
    """
    Delete a student by ID.
    """
    
    for student in students:
        if student["id"]==student_id:
            students.remove(student)
            return {
                "message": "Deleted successfully"
            }
    raise HTTPException(
        status_code=404,
        details="Student not found"
    )

@router.get("")
async def filter_students(branch: str | None = None):
    """
    Filter students by branch.
    """
    if branch is None:
        return students
    
    return [
        student
        for student in students
        if student["branch"].lower() == branch.lower()
    ]


