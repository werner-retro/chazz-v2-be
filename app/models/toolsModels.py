from typing import List, Literal
from pydantic import BaseModel


class AddIn(BaseModel):
    a: float
    b: float

# --- Menu Models ---
class PizzaSize(BaseModel):
    name: Literal["Small", "Medium", "Large"]
    price: float
    currency: Literal["ZAR"] = "ZAR"

class PizzaItem(BaseModel):
    name: str
    sizes: List[PizzaSize]

class ExtraItem(BaseModel):
    name: str
    price: float
    currency: Literal["ZAR"] = "ZAR"

class MenuResponse(BaseModel):
    pizzas: List[PizzaItem]
    extras: List[ExtraItem]