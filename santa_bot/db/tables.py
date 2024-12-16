from sqlalchemy import BigInteger, Column, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=False,
    )

    username: Mapped[str] = mapped_column(unique=True, nullable=True)
    name: Mapped[str] = mapped_column(nullable=True)
    wish_price: Mapped[str] = mapped_column(nullable=True)
    wish_list: Mapped[str] = mapped_column(nullable=True)


class Givers(Base):
    __tablename__ = "givers"

    giver_id = Column(BigInteger, ForeignKey("user.id"), primary_key=True)
    receiver_id = Column(BigInteger, ForeignKey("user.id"), nullable=True)
