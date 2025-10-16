from __future__ import annotations
from typing import List
from sqlalchemy.orm import Session
import os
from openai import OpenAI

from app.db.services.orderDbService import getAllTodaysOrders, getOrdersByCustomerId
from app.db.services.orderItemDbService import getItemsByOrderId
from app.db.services.orderItemExtraDbService import getExtrasByItemId
from app.models.recommendationModels import PreviousOrdersResponse, PreviousPizza

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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


def generatePizzaRecommendationsForUser(db: Session, customerId: int) -> PreviousOrdersResponse:
    """
    Generate top 3 pizza recommendations for the customer using GPT-4o-mini.
    Returns a PreviousOrdersResponse in the same structure as getOrderPizzasForCustomer().
    """
    orders = getOrdersByCustomerId(db, customerId)
    pizzas: List[PreviousPizza] = []

    # Flatten all previous pizzas
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

    # Prepare GPT input
    if not pizzas:
        return PreviousOrdersResponse(orders=[])

    order_summary = "\n".join(
        [f"- {p.pizzaName} ({p.size}) extras: {', '.join(p.extras) or 'none'}" for p in pizzas]
    )

    prompt = f"""
You are the recommendation system for Cheesy Chazz Pizza.
These are the pizzas this customer has ordered before:

{order_summary}

From these, recommend the top 3 pizzas they are most likely to enjoy again.
Rules:
- Prefer pizzas they ordered multiple times or with recurring extras.
- Suggest similar items (e.g. if they like spicy, suggest others with similar flavor).
- Respond in valid JSON array form like:
[
  {{ "pizzaName": "Margherita", "size": "Large", "extras": ["Extra Cheese"] }},
  {{ "pizzaName": "BBQ Chicken", "size": "Medium", "extras": [] }},
  {{ "pizzaName": "Pepperoni Feast", "size": "Large", "extras": ["Chilli Flakes"] }}
]
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a precise JSON-only pizza recommender."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )

        content = response.choices[0].message.content.strip()

        # Parse JSON safely
        import json
        try:
            data = json.loads(content)
            recs = []
            for item in data:
                recs.append(
                    PreviousPizza(
                        pizzaName=item.get("pizzaName", "Unknown"),
                        size=item.get("size", "Medium"),
                        extras=item.get("extras", []),
                    )
                )
            return PreviousOrdersResponse(orders=recs)

        except json.JSONDecodeError:
            print("⚠️ GPT returned invalid JSON:\n", content)
            return PreviousOrdersResponse(orders=[])

    except Exception as e:
        print("⚠️ Error generating GPT recommendations:", e)
        return PreviousOrdersResponse(orders=[], userStatus='existing')
    
def generatePizzaRecommendationsForNewUsers(db: Session) -> PreviousOrdersResponse:
    """
    Generate top 3 pizza recommendations for a NEW customer using GPT-4o-mini,
    based on ALL orders placed today (across all customers).
    Returns a PreviousOrdersResponse (same structure as other functions).
    """
    orders = getAllTodaysOrders(db)
    pizzas: List[PreviousPizza] = []

    # Flatten today's pizzas across all customers
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

    # No orders today → no signal → empty response
    if not pizzas:
        return PreviousOrdersResponse(orders=[])

    # Summarize today's orders for GPT
    todays_summary = "\n".join(
        [f"- {p.pizzaName} ({p.size}) extras: {', '.join(p.extras) or 'none'}" for p in pizzas]
    )

    prompt = f"""
You are the recommendation system for Cheesy Chazz Pizza.
Below is a list of ALL pizzas ordered today by all customers:

{todays_summary}

Based on today's ordering patterns, recommend the TOP 3 pizzas a NEW customer is most likely to enjoy.
Rules:
- Prefer pizzas that are popular today (higher frequency, common extras).
- If multiple variants exist, suggest the most common size and extras observed today.
- Respond in valid JSON array form like:
[
  {{ "pizzaName": "Margherita", "size": "Large", "extras": ["Extra Cheese"] }},
  {{ "pizzaName": "BBQ Chicken", "size": "Medium", "extras": [] }},
  {{ "pizzaName": "Pepperoni", "size": "Large", "extras": ["Bacon"] }}
]
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a precise JSON-only pizza recommender."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )

        content = response.choices[0].message.content.strip()

        # Parse JSON safely
        import json
        try:
            data = json.loads(content)
            recs: List[PreviousPizza] = []
            for item in data:
                recs.append(
                    PreviousPizza(
                        pizzaName=item.get("pizzaName", "Unknown"),
                        size=item.get("size", "Medium"),
                        extras=item.get("extras", []),
                    )
                )
            return PreviousOrdersResponse(orders=recs, userStatus='new')

        except json.JSONDecodeError:
            print("⚠️ GPT returned invalid JSON:\n", content)
            return PreviousOrdersResponse(orders=[])

    except Exception as e:
        print("⚠️ Error generating GPT recommendations (today):", e)
        return PreviousOrdersResponse(orders=[])
