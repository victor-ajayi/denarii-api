import enum

from sqlalchemy import Column, Enum, Float, ForeignKey, Integer
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import TIMESTAMP

from app.database import Base


class TransactionType(str, enum.Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"


class Category(str, enum.Enum):
    HEALTH = "HEALTH"
    FOOD = "FOOD"
    GROCERIES = "GROCERIES"
    TRANSFER = "TRANSFER"
    TRANSPORT = "TRANSPORT"
    TRAVEL = "TRAVEL"
    WITHDRAW = "WITHDRAW"
    OTHERS = "OTHERS"
    SUBSCRIPTIONS = "SUBSCRIPTIONS"


class Transaction(Base):
    __tablename__ = "transactions"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    amount: float = Column(Float, nullable=False)
    transaction_type: bool = Column(
        Enum(TransactionType, name="transaction_type"),
        nullable=False,
        server_default="CREDIT",
    )
    category: str = Column(Enum(Category, name="category"), server_default="OTHERS")
    created_at: TIMESTAMP = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    account_id: int = Column(
        Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False
    )
    user_id: int = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
