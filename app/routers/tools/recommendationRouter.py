from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.base import getDb

from app.db.services.customerDbService import getCustomerByNameAndPhone
from app.models.recommendationModels import RecommendationIn
from app.services.recommendationService import getOrderPizzasForCustomer

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.post("")
def getRecommendations(body: RecommendationIn, db: Session = Depends(getDb)):
    customer = getCustomerByNameAndPhone(db=db, name=body.customerName, phone=body.customerPhone)
    allOrders = getOrderPizzasForCustomer(db=db, customerId=customer.id)
    print('/////////////////////////////////////////////')
    print(allOrders)
    return allOrders

