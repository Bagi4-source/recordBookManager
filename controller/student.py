from typing import List, Optional, Union, Literal

from fastapi import APIRouter, HTTPException
from prisma.errors import ForeignKeyViolationError

from db.db import prisma
from pydantic import BaseModel
from datetime import datetime


class StudentCreate(BaseModel):
    name: str
    groupId: int
    status: bool


class StudentUpdate(StudentCreate):
    pass


class Student(StudentCreate):
    id: int
    createdAt: datetime
    updatedAt: datetime


class StudentFilterOrder(BaseModel):
    by: Union[Literal['id'], Literal['name'], Literal['status'], Literal['groupId'], Literal['createdAt']]
    direction: Union[Literal['asc'], Literal['desc']]


class StudentFilter(BaseModel):
    skip: int = 0
    take: int = 20
    name: Optional[str] = None
    groupId: Optional[int] = None
    status: Optional[bool] = None
    order: Optional[StudentFilterOrder]


router = APIRouter()


@router.post("/filter", response_model=List[Student])
async def get_students(filter: StudentFilter):
    where = {}
    order = {"id": "asc"}
    for key, value in filter.dict().items():
        if key in ["skip", "take"]:
            continue
        if value is None:
            continue

        if key == "name":
            where[key] = {"contains": value}
            continue

        if key == "order":
            order = {}
            order.update({value.get("by", "id"): value.get("direction", "asc")})
            continue

        where[key] = value

    return await prisma.student.find_many(
        take=filter.take,
        skip=filter.skip,
        where=where,
        order=order
    )


@router.post("/", response_model=Student)
async def create_student(student: StudentCreate):
    try:
        created_student = await prisma.student.create(
            data={
                "name": student.name,
                "groupId": student.groupId,
                "status": student.status
            }
        )
        return created_student
    except ForeignKeyViolationError as e:
        raise HTTPException(status_code=404, detail="Group not found")


@router.get("/{student_id}", response_model=Student)
async def read_student(student_id: int):
    student = await prisma.student.find_unique(where={"id": student_id})
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.put("/{student_id}", response_model=Student)
async def update_student(student_id: int, student: StudentUpdate):
    updated_student = await prisma.student.update(
        where={"id": student_id},
        data={
            "name": student.name,
            "groupId": student.group_id,
            "status": student.status
        }
    )
    if updated_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated_student


@router.delete("/{student_id}", response_model=Student)
async def delete_student(student_id: int):
    deleted_student = await prisma.student.delete(where={"id": student_id})
    if deleted_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return deleted_student
