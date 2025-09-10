from pydantic import BaseModel


class CoinGeckoList(BaseModel):
    """
    Model for Coin Gecko list, example:
    [{"id": "_", "symbol": "gib", "name": "༼ つ ◕_◕ ༽つ"}, {"id": "000-capital", "symbol": "000", "name": "000 Capital"}]
    """

    id: str
    symbol: str
    name: str
