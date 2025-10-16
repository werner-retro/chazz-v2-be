from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class OrderItem(BaseModel):
    """Single pizza order entry."""
    pizzaName: str = Field(..., description="Name of the pizza, e.g. 'Margherita'")
    size: Literal["Small", "Medium", "Large"] = Field(..., description="Selected pizza size")
    extras: List[str] = Field(default_factory=list, description="List of selected extras (by name)")
    quantity: int = Field(1, ge=1, description="Number of pizzas of this kind")
    subTotal: float = Field(0.0, description="Calculated subtotal for this item (including extras)")

class Order(BaseModel):
    """Full order model with all pizzas and grand total."""
    customerName: Optional[str] = Field(None, description="Name of the customer (optional for now)")
    pizzas: List[OrderItem] = Field(..., description="List of pizzas in the order")
    grandTotal: float = Field(..., description="Final total including all items and extras, in ZAR")