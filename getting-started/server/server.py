#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "mcp>=1.1.0",
# ]
# ///
"""FastMCP example with simple add tool."""

from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo")


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Run with streamable HTTP transport
if __name__ == "__main__":
    mcp.run(transport="streamable-http")
