from sqlalchemy.orm import Session
from app.db.orderDbModels import OrderItem

def createOrderItem(db: Session, orderId: int, pizzaName: str, size: str, quantity: int, subTotal: float) -> OrderItem:
    item = OrderItem(orderId=orderId, pizzaName=pizzaName, size=size, quantity=quantity, subTotal=subTotal)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def getOrderItemById(db: Session, itemId: int) -> OrderItem | None:
    return db.query(OrderItem).filter(OrderItem.id == itemId).first()

def getItemsByOrderId(db: Session, orderId: int) -> list[OrderItem]:
    return db.query(OrderItem).filter(OrderItem.orderId == orderId).all()

def updateOrderItem(db: Session, itemId: int, quantity: int | None = None, subTotal: float | None = None) -> OrderItem | None:
    item = db.query(OrderItem).filter(OrderItem.id == itemId).first()
    if not item:
        return None
    if quantity is not None:
        item.quantity = quantity
    if subTotal is not None:
        item.subTotal = subTotal
    db.commit()
    db.refresh(item)
    return item

def deleteOrderItem(db: Session, itemId: int) -> bool:
    item = db.query(OrderItem).filter(OrderItem.id == itemId).first()
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True
