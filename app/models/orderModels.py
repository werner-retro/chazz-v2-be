from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class OrderItemExtra(BaseModel):
    extraName: str = Field(...)


class OrderItem(BaseModel):
    """Single pizza order entry."""
    pizzaName: str = Field(..., description="Name of the pizza, e.g. 'Margherita'")
    size: Literal["Small", "Medium", "Large"] = Field(..., description="Selected pizza size")
    extras: List[str] = Field(default_factory=list, description="List of selected extras (by name)")
    quantity: int = Field(1, ge=1, description="Number of pizzas of this kind")
    subTotal: float = Field(0.0, description="Calculated subtotal for this item (including extras)")


class Order(BaseModel):
    """Full order payload received from the frontend/agent."""
    customerName: Optional[str] = Field(None, description="Customer’s name for the order")
    customerPhone: Optional[str] = Field(None, description="Customer’s phone number")
    mode: Optional[Literal["pickup", "delivery"]] = Field(None, description="Order mode")
    pizzas: List[OrderItem] = Field(default_factory=list, description="List of pizzas in the order")
    grandTotal: Optional[float] = Field(None, description="Final total including all items and extras in ZAR")
