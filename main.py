from fastapi import FastAPI
from db.db import prisma
from controller import student, group

app = FastAPI()


@app.on_event("startup")
async def startup():
    await prisma.connect()


@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()


app.include_router(student.router, prefix="/students", tags=["students"])
app.include_router(group.router, prefix="/groups", tags=["groups"])
