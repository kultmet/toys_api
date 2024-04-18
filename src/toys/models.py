import typing
from datetime import datetime

from sqlalchemy import (
    BOOLEAN,
    CHAR,
    TIMESTAMP,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class IDDateTimeMixin(object):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at = mapped_column(TIMESTAMP, default=datetime.now)


class Toy(IDDateTimeMixin, Base):
    __tablename__ = "toy"

    name: Mapped[str] = mapped_column(String)
    articul: Mapped[str] = mapped_column(String)
    gost: Mapped[str] = mapped_column(String, nullable=True)
    brand: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String)
    nomenclature: Mapped[str] = mapped_column(String)
    category_path: Mapped[str] = mapped_column(String)
    price: Mapped[int] = mapped_column(Integer)
    url: Mapped[str] = mapped_column(String)
    warehouse: Mapped[str] = mapped_column(String, nullable=True)
    count: Mapped[int] = mapped_column(Integer, nullable=True)
    instock: Mapped[int] = mapped_column(Integer, nullable=True)
    city: Mapped[str] = mapped_column(String)
    updated_at = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    discount_price: Mapped[float] = mapped_column(Float, nullable=True)
    razmer: Mapped[str] = mapped_column(String, nullable=True)
