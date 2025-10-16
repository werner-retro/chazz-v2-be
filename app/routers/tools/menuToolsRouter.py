# app/routers/menuToolsRouter.py
from fastapi import APIRouter
from app.models.toolsModels import ExtraItem, MenuResponse, PizzaItem, PizzaSize

router = APIRouter(prefix="/menu", tags=["menu tools"])

@router.get("", response_model=MenuResponse)
def get_menu():
    """Return Cheesy Chazz Pizza menu with pizzas, sizes, and extras."""
    return MenuResponse(
        pizzas=[
            PizzaItem(
                name="Margherita",
                sizes=[
                    PizzaSize(name="Small", price=69.00),
                    PizzaSize(name="Medium", price=89.00),
                    PizzaSize(name="Large", price=109.00),
                ],
            ),
            PizzaItem(
                name="Pepperoni",
                sizes=[
                    PizzaSize(name="Small", price=89.00),
                    PizzaSize(name="Medium", price=109.00),
                    PizzaSize(name="Large", price=129.00),
                ],
            ),
            PizzaItem(
                name="Hawaiian",
                sizes=[
                    PizzaSize(name="Small", price=85.00),
                    PizzaSize(name="Medium", price=105.00),
                    PizzaSize(name="Large", price=125.00),
                ],
            ),
        ],
        extras=[
            ExtraItem(name="Cheese", price=15.00),
            ExtraItem(name="Mushrooms", price=18.00),
            ExtraItem(name="Bacon", price=22.00),
        ],
    )
