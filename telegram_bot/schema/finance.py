from pydantic import BaseModel


class Portfolio(BaseModel):
    ticker: str
    quantity: float
    total_value: float


class Value_Portfolio(BaseModel):
    user_id: int
    total_portfolio_value: float
