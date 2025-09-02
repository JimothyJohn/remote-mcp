import json
from remote_mcp.server.mcp_lambda_handler import MCPLambdaHandler
from remote_mcp.server.tools import add_function

mcp = MCPLambdaHandler(name="mcp-lambda-server", version="0.1.0")


@mcp.tool()
def add(a: int, b: int) -> int:
    return add_function(a, b)


def lambda_handler(event, context):
    return mcp.handle_request(event, context)
