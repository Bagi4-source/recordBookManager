from typing import List

from fastapi import APIRouter, HTTPException
from db.db import prisma
from pydantic import BaseModel


class GroupCreate(BaseModel):
    groupNumber: str
    courseNumber: int


class GroupUpdate(GroupCreate):
    pass


class Group(GroupCreate):
    id: int


router = APIRouter()


@router.post("/", response_model=Group)
async def create_group(group: GroupCreate):
    created_group = await prisma.group.create(
        data={
            "groupNumber": group.groupNumber.upper(),
            "courseNumber": group.courseNumber
        }
    )
    return created_group


@router.get("/", response_model=List[Group])
async def get_groups():
    return await prisma.group.find_many(order={"groupNumber": "asc"})


@router.get("/{group_id}", response_model=Group)
async def read_group(group_id: int):
    group = await prisma.group.find_unique(where={"id": group_id})
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return group


@router.put("/{group_id}", response_model=Group)
async def update_group(group_id: int, group: GroupUpdate):
    updated_group = await prisma.group.update(
        where={"id": group_id},
        data={
            "groupNumber": group.groupNumber.upper(),
            "courseNumber": group.courseNumber
        }
    )
    if updated_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return updated_group


@router.delete("/{group_id}", response_model=Group)
async def delete_group(group_id: int):
    deleted_group = await prisma.group.delete(where={"id": group_id})
    if deleted_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return deleted_group
