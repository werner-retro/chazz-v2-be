# app/routers/orderToolsRouter.py
import sys
from fastapi import APIRouter

from app.models.orderModels import Order

router = APIRouter(prefix="/order", tags=["order tools"])


@router.post("")
def submit_order(body: Order):
    """
    Accept an Order object, compute grandTotal from item subTotals,
    print the full order, and return an orderNumber + grandTotal.
    """
    # Compute grandTotal (trusting the agent's subTotals)
    grand_total = round(sum(item.subTotal for item in body.pizzas), 2)

    # Log full order (with computed grandTotal if missing)
    order_to_log = body.model_copy(update={"grandTotal": body.grandTotal or grand_total})
    print("\n[ORDER RECEIVED]")
    print(order_to_log.model_dump_json(indent=2), file=sys.stdout, flush=True)

    # Return minimal confirmation payload
    return {
        "orderNumber": 101,
        "grandTotal": grand_total,
    }