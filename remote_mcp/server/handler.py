import requests
from remote_mcp.server.mcp_lambda_handler import MCPLambdaHandler
from remote_mcp.server.models import CoinGeckoList

COIN_GECKO_BASE_URL = "https://api.coingecko.com/api/v3"


mcp = MCPLambdaHandler(name="mcp-lambda-server", version="0.1.0")


@mcp.tool()
def add_function(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


@mcp.tool()
def get_coins() -> list[CoinGeckoList]:
    # Get all available coin IDs from CoinGecko
    url = f"{COIN_GECKO_BASE_URL}/coins/list"
    headers = {"x-cg-pro-api-key": "CG-x9Mn1xPv4v7sKSeY87pL2w7s"}
    response = requests.get(url, headers=headers)
    return [CoinGeckoList(**coin) for coin in response.json()]


"""
# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    # Get a personalized greeting
    return get_greeting_function(name)
"""
