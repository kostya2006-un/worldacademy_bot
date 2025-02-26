from pydantic import BaseModel


class Asset(BaseModel):
    ticker: str
    name: str
    asset_type: str
    price: float
