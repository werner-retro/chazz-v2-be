# app/routers/orderToolsRouter.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.base import getDb
from app.models.orderModels import Order as OrderIn

from app.services.orderService import processIncomingOrder

router = APIRouter(prefix="/order", tags=["order tools"])


@router.post("")
def submitOrder(body: OrderIn, db: Session = Depends(getDb)):
    orderId, grandTotal = processIncomingOrder(db, body)
    return {"orderNumber": orderId, "grandTotal": grandTotal}