from typing import List, Optional
from pydantic import BaseModel, Field


class OrderItemExtra(BaseModel):
    extraName: str = Field(...)


class OrderItem(BaseModel):
    pizzaName: str = Field(..., description="Name of the pizza")
    size: str = Field(..., description="Small | Medium | Large")
    quantity: int = Field(1, ge=1)
    subTotal: float = Field(...)
    extras: List[str] = Field(default_factory=list)


class Order(BaseModel):
    customerName: Optional[str] = None
    pizzas: List[OrderItem] = Field(default_factory=list)
    grandTotal: Optional[float] = None
