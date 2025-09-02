import asyncio
import argparse
import os
import sys
from fastmcp import Client, FastMCP
import dotenv

dotenv.load_dotenv()

async def main():
    parser = argparse.ArgumentParser(description="Remote MCP Client")
    parser.add_argument(
        "--url",
        "-u",
        default=os.environ.get("AWS_ENDPOINT", "http://localhost:8000/mcp"),
        help="Server URL (default: AWS_ENDPOINT env var or http://localhost:8000/mcp)"
    )
    parser.add_argument(
        "--tool",
        "-t",
        help="Tool to call (e.g., 'add')"
    )
    parser.add_argument(
        "--args",
        "-a",
        help="Tool arguments as JSON string (e.g., '{\"a\": 1, \"b\": 2}')"
    )
    parser.add_argument(
        "--list",
        "-l",
        action="store_true",
        help="List available tools and resources"
    )
    parser.add_argument(
        "--ping",
        "-p",
        action="store_true",
        help="Ping the server"
    )
    
    args = parser.parse_args()
    
    client = Client(args.url)
    
    async with client:
        if args.ping:
            await client.ping()
            print(f"✓ Server at {args.url} is responsive")
            return
            
        if args.list:
            tools = await client.list_tools()
            resources = await client.list_resources()
            print(f"Available tools: {[t.name for t in tools]}")
            print(f"Available resources: {[r.name for r in resources]}")
            return
            
        if args.tool:
            import json
            tool_args = json.loads(args.args) if args.args else {}
            result = await client.call_tool(args.tool, tool_args)
            print(result.content[0].text)
            return
            
        # Default behavior: show server info
        await client.ping()
        tools = await client.list_tools()
        resources = await client.list_resources()
        print(f"Connected to: {args.url}")
        print(f"Tools: {[t.name for t in tools]}")
        print(f"Resources: {[r.name for r in resources]}")

if __name__ == "__main__":
    asyncio.run(main())
