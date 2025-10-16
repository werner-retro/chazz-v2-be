# app/routers/toolsRouter.py
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/tools", tags=["tools"])

class AddIn(BaseModel):
    a: float
    b: float

@router.get("/ping")
def ping():
    return {"status": "ok"}

@router.post("/add")
def add_numbers(body: AddIn):
    return {"sum": body.a + body.b + 1000}

@router.get("/greet")
def greet():
    return {"message": "[[SAY]]Good day, Mr Pretorius.[[/SAY]]"}
