from remote_mcp.server.handler import mcp


def lambda_handler(event, context):
    return mcp.handle_request(event, context)
