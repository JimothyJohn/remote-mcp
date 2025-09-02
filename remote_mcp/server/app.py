from remote_mcp.server.mcp_lambda_handler import MCPLambdaHandler
from remote_mcp.server.tools import add_function

mcp = MCPLambdaHandler(name="mcp-lambda-server", version="0.1.0")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return add_function(a, b)


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


def lambda_handler(event, context):
    return mcp.handle_request(event, context)
