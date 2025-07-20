from sqlalchemy import BigInteger, String

from sqlalchemy.orm import mapped_column, Mapped
from .base import Base


class User(Base):
    __tablename__ = "Users"

    Id: Mapped[int] = mapped_column(primary_key=True)
    Telegram_id = mapped_column(BigInteger)
    First_name: Mapped[str] = mapped_column(String(255), nullable=False)
    Username: Mapped[str] = mapped_column(String(255))


class Channal(Base):
    __tablename__ = "Channals"

    Id: Mapped[int] = mapped_column(primary_key=True)
    Channal_id = mapped_column(BigInteger)
    Channal_name: Mapped[str] = mapped_column(String(255), nullable=False)
