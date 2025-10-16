from sqlalchemy.orm import Session
from app.db.orderDbModels import Customer

def createCustomer(db: Session, name: str, phone: str | None = None, address: str | None = None) -> Customer:
    customer = Customer(name=name, phone=phone, address=address)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

def getCustomerById(db: Session, customerId: int) -> Customer | None:
    return db.query(Customer).filter(Customer.id == customerId).first()

def getCustomerByName(db: Session, name: str) -> Customer | None:
    return db.query(Customer).filter(Customer.name == name).first()

def getAllCustomers(db: Session) -> list[Customer]:
    return db.query(Customer).all()

def updateCustomer(db: Session, customerId: int, name: str | None = None, phone: str | None = None, address: str | None = None) -> Customer | None:
    customer = db.query(Customer).filter(Customer.id == customerId).first()
    if not customer:
        return None
    if name: customer.name = name
    if phone: customer.phone = phone
    if address: customer.address = address
    db.commit()
    db.refresh(customer)
    return customer

def deleteCustomer(db: Session, customerId: int) -> bool:
    customer = db.query(Customer).filter(Customer.id == customerId).first()
    if not customer:
        return False
    db.delete(customer)
    db.commit()
    return True
