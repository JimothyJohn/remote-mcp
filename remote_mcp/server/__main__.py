import argparse
from fastmcp import FastMCP
from tools import add_function

mcp = FastMCP("Demo 🚀")

@mcp.tool
def add(a: int, b: int) -> int:
    return add_function(a, b)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remote MCP Server")
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        "-p",
        type=int,
        default=8000,
        help="Port to bind to (default: 8000)"
    )
    parser.add_argument(
        "--transport",
        "-t",
        default="http",
        choices=["http", "stdio", "sse"],
        help="Transport type (default: http)"
    )
    
    args = parser.parse_args()
    
    print(f"Starting MCP server on {args.host}:{args.port} using {args.transport} transport")
    mcp.run(transport=args.transport, host=args.host, port=args.port)
