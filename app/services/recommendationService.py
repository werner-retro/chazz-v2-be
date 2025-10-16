from __future__ import annotations
from typing import Any, Dict, List
from sqlalchemy.orm import Session

from app.db.services.orderDbService import getOrdersByCustomerId
from app.db.services.orderItemDbService import getItemsByOrderId
from app.db.services.orderItemExtraDbService import getExtrasByItemId
from app.models.recommendationModels import PreviousOrdersResponse, PreviousPizza

def getOrderPizzasForCustomer(db: Session, customerId: int) -> PreviousOrdersResponse:
    """
    Return a PreviousOrdersResponse with a simplified list of pizzas (name + extras)
    from all orders of a given customer.
    """
    orders = getOrdersByCustomerId(db, customerId)
    pizzas: List[PreviousPizza] = []

    for order in orders:
        items = getItemsByOrderId(db, order.id)
        for item in items:
            extras = getExtrasByItemId(db, item.id)
            pizzas.append(
                PreviousPizza(
                    pizzaName=item.pizzaName,
                    size=item.size,
                    extras=[ex.extraName for ex in extras] if extras else [],
                )
            )

    return PreviousOrdersResponse(orders=pizzas)
