def add_function(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


def subtract_function(a: int, b: int) -> int:
    """Subtract two numbers"""
    return a - b


"""
# Query a DynamoDB Table with boto3
def query_dynamodb_table(table_name: str, key: str, value: str) -> dict:
    # Query a DynamoDB table
    return boto3.client("dynamodb").query(
        TableName=table_name, KeyConditionExpression=Key(key).eq(value)
    )
"""
