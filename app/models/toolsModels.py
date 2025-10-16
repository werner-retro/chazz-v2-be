from pydantic import BaseModel


class AddIn(BaseModel):
    a: float
    b: float