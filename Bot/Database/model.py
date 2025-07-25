from sqlalchemy import BigInteger, String, ForeignKey, Integer
from sqlalchemy.orm import mapped_column, Mapped

from .base import Base


class User(Base):
    __tablename__ = "Users"

    Id: Mapped[int] = mapped_column(primary_key=True)
    Telegram_id = mapped_column(BigInteger)
    First_name: Mapped[str] = mapped_column(String(255), nullable=False)
    Username: Mapped[str] = mapped_column(String(255))


class Channel(Base):
    __tablename__ = "Channels"

    Id: Mapped[int] = mapped_column(primary_key=True)
    Channel_id = mapped_column(BigInteger)
    Channel_name: Mapped[str] = mapped_column(String(255), nullable=False)

    Adder: Mapped[int] = mapped_column(
        Integer, ForeignKey("Users.Id", ondelete="CASCADE"), nullable=False
    )
