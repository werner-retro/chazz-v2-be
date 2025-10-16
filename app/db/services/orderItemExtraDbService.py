from sqlalchemy.orm import Session
from app.db.orderDbModels import OrderItemExtra

def createOrderItemExtra(db: Session, orderItemId: int, extraName: str) -> OrderItemExtra:
    extra = OrderItemExtra(orderItemId=orderItemId, extraName=extraName)
    db.add(extra)
    db.commit()
    db.refresh(extra)
    return extra

def getExtrasByItemId(db: Session, orderItemId: int) -> list[OrderItemExtra]:
    return db.query(OrderItemExtra).filter(OrderItemExtra.orderItemId == orderItemId).all()

def deleteOrderItemExtra(db: Session, extraId: int) -> bool:
    extra = db.query(OrderItemExtra).filter(OrderItemExtra.id == extraId).first()
    if not extra:
        return False
    db.delete(extra)
    db.commit()
    return True
