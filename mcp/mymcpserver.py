# server.py
from fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo")

# Add an addition tool
@mcp.tool()
def get_session_username() -> str:
    """return the username of the session"""
    return "Ricardo Borges"


if __name__ == "__main__":
    mcp.run()
