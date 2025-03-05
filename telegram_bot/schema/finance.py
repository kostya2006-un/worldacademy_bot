from datetime import datetime

from pydantic import BaseModel


class Portfolio(BaseModel):
    ticker: str
    quantity: float
    total_value: float


class Value_Portfolio(BaseModel):
    user_id: int
    total_portfolio_value: float


class Trade(BaseModel):
    user_id: int
    ticker: str
    trade_type: str  # "buy" или "sell"
    quantity: float

    @classmethod
    def create_trade(cls, user_id: int, ticker: str, trade_type: str, quantity: float):
        return cls(
            user_id=user_id, ticker=ticker, trade_type=trade_type, quantity=quantity
        )


class Trade_History(BaseModel):
    ticker: str
    trade_type: str
    quantity: float
    price: float
    timestamp: datetime
