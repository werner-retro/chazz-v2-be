from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, ForeignKey, DateTime, func
from app.db.base import Base

class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="customer", cascade="all, delete-orphan")

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    customerId: Mapped[int | None] = mapped_column(ForeignKey("customers.id"), nullable=True)
    createdAt: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
    mode: Mapped[str | None] = mapped_column(String(20), nullable=True)   # "pickup" / "delivery" (future)
    grandTotal: Mapped[float | None] = mapped_column(Float, nullable=True)

    customer: Mapped[Customer | None] = relationship("Customer", back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "orderItems"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    orderId: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    pizzaName: Mapped[str] = mapped_column(String(120), nullable=False)
    size: Mapped[str] = mapped_column(String(20), nullable=False)         # Small | Medium | Large
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    subTotal: Mapped[float] = mapped_column(Float, nullable=False)

    order: Mapped[Order] = relationship("Order", back_populates="items")
    extras: Mapped[list["OrderItemExtra"]] = relationship("OrderItemExtra", back_populates="orderItem", cascade="all, delete-orphan")

class OrderItemExtra(Base):
    __tablename__ = "orderItemExtras"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    orderItemId: Mapped[int] = mapped_column(ForeignKey("orderItems.id"), nullable=False)
    extraName: Mapped[str] = mapped_column(String(120), nullable=False)

    orderItem: Mapped[OrderItem] = relationship("OrderItem", back_populates="extras")
