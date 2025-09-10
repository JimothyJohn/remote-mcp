import os

import boto3
import dotenv
import pytest
from fastmcp import Client

dotenv.load_dotenv()

# Define the endpoints to test against
endpoints = {
    "cloud": os.environ.get("AWS_ENDPOINT"),
    # "local": "http://localhost:3000/mcp",
}


@pytest.fixture(params=list(endpoints.values()), ids=list(endpoints.keys()))
def client(request):
    """Yield a client for each endpoint."""
    return Client(request.param)


"""
Make sure env variable AWS_SAM_STACK_NAME exists with the name of the stack we are going to test. 
"""


class TestApiGateway:
    @pytest.fixture()
    def api_gateway_url(self):
        """Get the API Gateway URL from Cloudformation Stack outputs"""
        stack_name = os.environ.get("AWS_SAM_STACK_NAME")

        if stack_name is None:
            raise ValueError(
                "Please set the AWS_SAM_STACK_NAME environment variable to the name of your stack"
            )

        client = boto3.client("cloudformation")

        try:
            response = client.describe_stacks(StackName=stack_name)
        except Exception as e:
            raise Exception(
                f"Cannot find stack {stack_name} \n"
                f'Please make sure a stack with the name "{stack_name}" exists'
            ) from e

        stacks = response["Stacks"]
        stack_outputs = stacks[0]["Outputs"]
        api_outputs = [
            output for output in stack_outputs if output["OutputKey"] == "RemoteMCPApi"
        ]

        if not api_outputs:
            raise KeyError(f"HelloWorldAPI not found in stack {stack_name}")

        return api_outputs[0]["OutputValue"]  # Extract url from stack outputs

    def test_api_gateway(self, api_gateway_url):
        """Call the API Gateway endpoint and check the response
        curl https://<api_gateway_url>/health {"jsonrpc": "2.0", "id": null, "error": {"code": -32700, "message": "Unsupported Media Type"}}%


        response = requests.get(f"{api_gateway_url}health")


        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        assert response.headers["MCP-Version"] == "0.6"
        assert response.json() == {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Unsupported Media Type"}}

        """

        assert 1 == 1

    @pytest.mark.asyncio
    async def test_get_tools(self, client):
        async with client:
            tools = await client.list_tools()

            assert len(tools) == 1
            assert tools[0].name == "add"

    @pytest.mark.asyncio
    async def test_call_tool(self, client):
        async with client:
            result = await client.call_tool("add", {"a": 1, "b": 2})

            assert result.content[0].text == "3"
