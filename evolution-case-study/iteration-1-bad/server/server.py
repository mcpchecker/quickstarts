#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "mcp>=1.1.0",
# ]
# ///
"""Text processing server - Iteration 1: Bad documentation (misleading names)"""

from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("TextProcessing-Bad")


@mcp.tool()
def process(text: str) -> str:
    """Process text"""
    return text.upper()


@mcp.tool()
def transform(text: str) -> str:
    """Transform text"""
    return text.lower()


@mcp.tool()
def convert(text: str) -> str:
    """Convert text"""
    return text.title()


@mcp.tool()
def format_text(text: str) -> str:
    """Format text"""
    return text.capitalize()


# Run with streamable HTTP transport
if __name__ == "__main__":
    mcp.run(transport="streamable-http")
