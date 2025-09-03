# Remote MCP API Documentation

## Overview

Remote MCP is a deployment template for hosting remote MCP (Model Context Protocol) servers and generating clients to test against them. This documentation covers the main modules and classes in the Remote MCP library.

## Table of Contents

- [Server Components](#server-components)
  - [MCPLambdaHandler](#mcplambdahandler)
  - [Tools](#tools)
  - [Session Management](#session-management)
- [Client Components](#client-components)
- [Types](#types)
- [Examples](#examples)

## Server Components

### MCPLambdaHandler

The main handler class for MCP (Model Context Protocol) HTTP events in AWS Lambda.

#### Constructor

```python
MCPLambdaHandler(
    name: str,
    version: str = "1.0.0",
    session_store: Optional[Union[SessionStore, str]] = None
)
```

**Parameters:**
- `name` (str): Handler name
- `version` (str, optional): Handler version. Defaults to "1.0.0"
- `session_store` (Optional[Union[SessionStore, str]], optional): Session storage configuration
  - `None`: No sessions
  - `SessionStore` instance: Custom session storage
  - `str`: DynamoDB table name for backwards compatibility

#### Methods

##### `tool()`

Decorator to register a function as an MCP tool. Automatically generates MCP tool schema from function signature and docstring.

```python
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        The sum of a and b
    """
    return a + b
```

##### `resource(uri, name, description=None, mime_type=None)`

Decorator to register a function as a resource provider.

```python
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"
```

**Parameters:**
- `uri` (str): Resource URI pattern (supports parameters like `{name}`)
- `name` (str): Resource display name
- `description` (str, optional): Resource description
- `mime_type` (str, optional): MIME type, defaults to "text/plain"

##### `get_session()`

Get the current session data wrapper.

```python
def get_session(self) -> Optional[SessionData]:
    """Get the current session data wrapper.
    
    Returns:
        SessionData object or None if no session exists
    """
```

##### `set_session(data)`

Set the entire session data.

```python
def set_session(self, data: Dict[str, Any]) -> bool:
    """Set the entire session data.
    
    Args:
        data: New session data
    
    Returns:
        True if successful, False if no session exists
    """
```

##### `update_session(updater_func)`

Update session data using a function.

```python
def update_session(self, updater_func: Callable[[SessionData], None]) -> bool:
    """Update session data using a function.
    
    Args:
        updater_func: Function that takes SessionData and updates it in place
    
    Returns:
        True if successful, False if no session exists
    """
```

##### `handle_request(event, context)`

Handle an incoming Lambda request. This is the main entry point for AWS Lambda functions.

```python
def handle_request(self, event: Dict, context: Any) -> Dict:
    """Handle an incoming Lambda request."""
```

#### Supported Methods

The handler automatically supports these MCP methods:

- **`initialize`**: Initialize MCP session
- **`tools/list`**: List available tools
- **`tools/call`**: Execute a tool
- **`resources/list`**: List available resources
- **`resources/read`**: Read a resource
- **`ping`**: Health check

### Tools

Built-in tool implementations in `remote_mcp.server.tools`:

#### `add_function(a: int, b: int) -> int`

Add two numbers together.

**Parameters:**
- `a` (int): First number
- `b` (int): Second number

**Returns:**
- `int`: Sum of the two numbers

#### `subtract_function(a: int, b: int) -> int`

Subtract two numbers.

**Parameters:**
- `a` (int): First number  
- `b` (int): Second number

**Returns:**
- `int`: Difference of the two numbers

### Session Management

#### SessionData

Type-safe session data access wrapper.

```python
class SessionData(Generic[T]):
    """Helper class for type-safe session data access."""
    
    def get(self, key: str, default: Optional[T] = None) -> Optional[T]:
        """Get a value from session data with type safety."""
        
    def set(self, key: str, value: T) -> None:
        """Set a value in session data."""
        
    def raw(self) -> Dict[str, Any]:
        """Get the raw dictionary data."""
```

#### Session Stores

##### NoOpSessionStore

Default session store that doesn't persist sessions.

##### DynamoDBSessionStore

Session store that persists sessions in DynamoDB.

```python
DynamoDBSessionStore(table_name: str)
```

## Client Components

### Client Usage

The client is implemented in `remote_mcp.client` and provides a command-line interface for testing MCP servers.

#### Command Line Interface

```bash
# List available tools and resources
python -m remote_mcp.client --list

# Ping the server
python -m remote_mcp.client --ping

# Call a tool
python -m remote_mcp.client --tool add --args '{"a": 5, "b": 3}'

# Use custom server URL
python -m remote_mcp.client --url https://your-server.com/mcp --list
```

#### Environment Variables

- `AWS_ENDPOINT`: Default server URL if not specified via `--url`

## Types

The `remote_mcp.server.mcp_lambda_handler.types` module defines all the MCP protocol types:

### Core Types

- **`JSONRPCRequest`**: JSON-RPC request structure
- **`JSONRPCResponse`**: JSON-RPC response structure  
- **`JSONRPCError`**: JSON-RPC error structure

### Content Types

- **`TextContent`**: Text content with `text` field
- **`ImageContent`**: Image content with `data` (base64) and `mimeType` fields
- **`ErrorContent`**: Error content with `text` field

### Resource Types

- **`Resource`**: Base resource interface
- **`StaticResource`**: Static resource with fixed content
- **`ResourceContent`**: Resource content wrapper

### MCP Protocol Types

- **`ServerInfo`**: Server information (name, version)
- **`Capabilities`**: Server capabilities (tools, resources)
- **`InitializeResult`**: Initialization response

## Examples

### Basic Server Setup

```python
from remote_mcp.server.mcp_lambda_handler import MCPLambdaHandler
from remote_mcp.server.tools import add_function

# Create handler
mcp = MCPLambdaHandler(name="my-mcp-server", version="1.0.0")

# Register a tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return add_function(a, b)

# Register a resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

# Lambda handler
def lambda_handler(event, context):
    return mcp.handle_request(event, context)
```

### Advanced Server with Sessions

```python
from remote_mcp.server.mcp_lambda_handler import MCPLambdaHandler
from remote_mcp.server.mcp_lambda_handler.session import DynamoDBSessionStore

# Create handler with DynamoDB sessions
session_store = DynamoDBSessionStore(table_name="mcp-sessions")
mcp = MCPLambdaHandler(
    name="stateful-server", 
    version="1.0.0", 
    session_store=session_store
)

@mcp.tool()
def increment_counter() -> int:
    """Increment a session counter"""
    session = mcp.get_session()
    if session:
        current = session.get("counter", 0)
        new_value = current + 1
        session.set("counter", new_value)
        return new_value
    return 0

def lambda_handler(event, context):
    return mcp.handle_request(event, context)
```

### Tool with Complex Types

```python
from typing import List, Dict
from enum import Enum

class Color(Enum):
    RED = "red"
    GREEN = "green" 
    BLUE = "blue"

@mcp.tool()
def process_items(
    items: List[str], 
    metadata: Dict[str, str],
    color: Color
) -> str:
    """Process a list of items with metadata and color
    
    Args:
        items: List of item names to process
        metadata: Additional metadata as key-value pairs
        color: Color preference for processing
        
    Returns:
        Processing result summary
    """
    return f"Processed {len(items)} items with color {color.value}"
```

### Client Usage

```python
import asyncio
from fastmcp import Client

async def test_server():
    client = Client("https://your-server.com/mcp")
    
    async with client:
        # List available tools
        tools = await client.list_tools()
        print(f"Available tools: {[t.name for t in tools]}")
        
        # Call a tool
        result = await client.call_tool("add", {"a": 5, "b": 3})
        print(f"Result: {result.content[0].text}")

asyncio.run(test_server())
```

## Error Handling

The handler automatically converts Python exceptions to MCP error responses:

- **Parse errors (-32700)**: Invalid JSON or malformed requests
- **Invalid request (-32600)**: Missing required fields
- **Method not found (-32601)**: Unknown MCP method or tool
- **Invalid params (-32602)**: Missing or invalid parameters  
- **Internal error (-32603)**: Tool execution errors

## Deployment

### AWS Lambda

The handler is designed for AWS Lambda deployment:

1. Package your code with dependencies
2. Set the Lambda handler to `your_module.lambda_handler`
3. Configure API Gateway to route requests to the Lambda function
4. Set appropriate IAM permissions for DynamoDB (if using sessions)

### Environment Variables

- **`AWS_REGION`**: AWS region for DynamoDB sessions
- **`LOG_LEVEL`**: Logging level (DEBUG, INFO, WARNING, ERROR)

## Security Considerations

- Always validate input parameters in your tools
- Use session management for stateful operations
- Implement appropriate authentication/authorization
- Follow AWS security best practices for Lambda deployment
- Regularly update dependencies for security patches

## Performance Tips

- Use DynamoDB sessions only when state persistence is required
- Implement connection pooling for external services
- Cache frequently accessed data
- Monitor Lambda cold starts and optimize initialization
- Use appropriate memory/timeout settings for Lambda functions

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for development setup and contribution guidelines.