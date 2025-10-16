from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.base import getDb

from app.db.services.customerDbService import getCustomerByNameAndPhone
from app.models.recommendationModels import RecommendationIn
from app.services.recommendationService import generatePizzaRecommendationsForUser, generatePizzaRecommendationsForNewUsers

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.post("")
def getRecommendations(body: RecommendationIn, db: Session = Depends(getDb)):
    """
    Get pizza recommendations:
    - If an existing customer is found, use their past orders.
    - If not, generate recommendations based on today's overall popular orders.
    """
    customer = getCustomerByNameAndPhone(db=db, name=body.customerName, phone=body.customerPhone)
    
    if customer:
        print(f"🔍 Existing customer found: {customer.name} (id={customer.id})")
        recommendations = generatePizzaRecommendationsForUser(db=db, customerId=customer.id)
    else:
        print(f"🆕 No customer found for {body.customerName}, generating recommendations for new users.")
        recommendations = generatePizzaRecommendationsForNewUsers(db=db)

    print("/////////////////////////////////////////////")
    print(recommendations)
    return recommendations

