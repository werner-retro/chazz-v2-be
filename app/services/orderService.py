from sqlalchemy.orm import Session
from typing import Tuple

from app.models.orderModels import Order as OrderIn
from app.db.services.customerDbService import createCustomer, getCustomerByNameAndPhone
from app.db.services.orderDbService import createOrder
from app.db.services.orderItemDbService import createOrderItem
from app.db.services.orderItemExtraDbService import createOrderItemExtra


def processIncomingOrder(db: Session, orderIn: OrderIn) -> Tuple[int, float]:
    """
    Takes an incoming order from the frontend and writes it to the database
    using the low-level CRUD services.

    Returns:
        (orderId, grandTotal)
    """
    # 1. Calculate grand total if not provided
    grandTotal = (
        float(orderIn.grandTotal)
        if orderIn.grandTotal is not None
        else round(sum(float(p.subTotal) for p in orderIn.pizzas), 2)
    )

    # 2. Get or create customer (by name)
    customerRow = None
    if orderIn.customerName and orderIn.customerPhone:
        customerRow = getCustomerByNameAndPhone(db, orderIn.customerName, orderIn.customerPhone)
        if not customerRow:
            customerRow = createCustomer(db, name=orderIn.customerName, phone=orderIn.customerPhone)

    # 3. Create order
    orderRow = createOrder(
        db=db,
        customerId=customerRow.id if customerRow else None,
        grandTotal=grandTotal,
        mode=None,
    )

    # 4. Create order items
    for pizza in orderIn.pizzas:
        itemRow = createOrderItem(
            db=db,
            orderId=orderRow.id,
            pizzaName=pizza.pizzaName,
            size=pizza.size,
            quantity=pizza.quantity,
            subTotal=pizza.subTotal,
        )

        # 5. Create extras for each item
        for extraName in pizza.extras:
            createOrderItemExtra(db=db, orderItemId=itemRow.id, extraName=extraName)

    return orderRow.id, grandTotal
