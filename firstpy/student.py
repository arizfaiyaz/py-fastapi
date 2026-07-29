from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException

app = FastAPI()

students =  []

class Student(BaseModel):
    name: str
    age: int
    branch: str
  

@app.post("/students")
def create_student(student: Student):
    
    new_student = {
        "id": len(students) + 1,
        "name": student.name,
        "age": student.age,
        "branch": student.branch
    }
    
    students.append(new_student)
    
    return new_student


@app.get("/students") # get all the students
def get_students():
    return students

@app.get("/students/{student_id}")  # get a specific student by ID
def get_student(student_id: int):
   
    for student in students:
        
        if student["id"] == student_id:
            return student
        
    return {
        "message": "Student not found"
    }


@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    
    for student in students:
        
        if student["id"] == student_id:
            student["name"] = student.name
            student["age"] = student.age
            student["branch"] = student.branch
            
            return student
        
    return {
        "message": "Student not found"
    }


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    
    for student in students:
        
        if student["id"] == student_id:
            
            students.remove(student)
            return {
                "message": "Student deleted successfully"
            }
    raise  HTTPException(
        status_code =  404,
        detail = "Student not found"
    )


#mini challenge: create a new endpoint that returns the total number of students in the list.
@app.get("/students/count")
def get_student_count():
    return {"total_students": len(students)}

# 2  mini  challenge: create a new endpoint that returns  query parameters for filtering students by branch. 

@app.get("/students")
def get_students_branch(branch: str | None =  None):
    
    if  branch is None:
        return students
    
    filtered_students =[]
    
    for student in  students:
        if student["branch"].lower() == branch.lower():
            filtered_students.append(student)
    
    return filtered_students