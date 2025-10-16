# app/routers/orderToolsRouter.py
import sys
from fastapi import APIRouter

from app.models.orderModels import Order

router = APIRouter(prefix="/order", tags=["order tools"])


@router.post("")
def submit_order(body: Order):
    """
    Accept an Order object and simply print it to the server terminal.
    No validation, no totals math here — the agent compiles everything.
    """
    print("\n[ORDER RECEIVED]")
    print(body.model_dump_json(indent=2), file=sys.stdout, flush=True)
    return {"ok": True}