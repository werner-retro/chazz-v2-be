from typing import List, Literal
from pydantic import BaseModel, Field


class RecommendationIn(BaseModel):
    customerName: str
    customerPhone: str

class PreviousPizza(BaseModel):
    pizzaName: str = Field(..., description="Name of the previously ordered pizza")
    size: str
    extras: List[str] = Field(default_factory=List, description="List of extras for this pizza (if any)")

class PreviousOrdersResponse(BaseModel):
    orders: List[PreviousPizza] = Field(
        default_factory=list,
        description="Simplified list of previously ordered pizzas with extras"
    )
    userStatus: Literal["new", "existing"]