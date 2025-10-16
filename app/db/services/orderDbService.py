from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db.orderDbModels import Order

def createOrder(db: Session, customerId: int | None, grandTotal: float | None = None, mode: str | None = None) -> Order:
    order = Order(customerId=customerId, grandTotal=grandTotal, mode=mode)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def getOrderById(db: Session, orderId: int) -> Order | None:
    return db.query(Order).filter(Order.id == orderId).first()

def getAllOrders(db: Session) -> list[Order]:
    return db.query(Order).order_by(Order.createdAt.desc()).all()

def updateOrder(db: Session, orderId: int, grandTotal: float | None = None, mode: str | None = None) -> Order | None:
    order = db.query(Order).filter(Order.id == orderId).first()
    if not order:
        return None
    if grandTotal is not None:
        order.grandTotal = grandTotal
    if mode is not None:
        order.mode = mode
    db.commit()
    db.refresh(order)
    return order

def deleteOrder(db: Session, orderId: int) -> bool:
    order = db.query(Order).filter(Order.id == orderId).first()
    if not order:
        return False
    db.delete(order)
    db.commit()
    return True

def getOrdersByCustomerId(db: Session, customerId: int | None) -> list[Order]:
    """
    Safely fetch all orders for a given customer ID.
    Returns an empty list if the customerId is None or no orders exist.
    """
    if not customerId:
        return []

    try:
        return (
            db.query(Order)
            .filter(Order.customerId == customerId)
            .order_by(Order.createdAt.desc())
            .all()
        )
    except Exception as e:
        print(f"⚠️ Error fetching orders for customerId={customerId}: {e}")
        return []
    
def getAllTodaysOrders(db: Session) -> list[Order]:
    """
    Fetch all orders placed today (same calendar day), across all customers.
    Returns an empty list if no matching orders exist.
    """
    try:
        return (
            db.query(Order)
            .filter(func.date(Order.createdAt) == func.current_date())
            .order_by(Order.createdAt.desc())
            .all()
        )
    except Exception as e:
        print(f"⚠️ Error fetching today's orders: {e}")
        return []
