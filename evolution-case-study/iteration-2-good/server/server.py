#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "mcp>=1.1.0",
# ]
# ///
"""Text processing server - Iteration 2: Good documentation"""

from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("TextProcessing-Good")


@mcp.tool()
def to_uppercase(text: str) -> str:
    """Convert all letters in text to uppercase (capital letters).

    Use this tool when you need text in ALL CAPS format. Every lowercase
    letter becomes uppercase, while numbers and symbols remain unchanged.

    Args:
        text: The text to convert to uppercase

    Returns:
        The text with all letters converted to uppercase

    Example:
        to_uppercase("hello world") returns "HELLO WORLD"
        to_uppercase("Hello World 123!") returns "HELLO WORLD 123!"
    """
    return text.upper()


@mcp.tool()
def to_lowercase(text: str) -> str:
    """Convert all letters in text to lowercase (small letters).

    Use this tool when you need text in all lowercase format. Every uppercase
    letter becomes lowercase, while numbers and symbols remain unchanged.

    Args:
        text: The text to convert to lowercase

    Returns:
        The text with all letters converted to lowercase

    Example:
        to_lowercase("HELLO WORLD") returns "hello world"
        to_lowercase("Hello World 123!") returns "hello world 123!"
    """
    return text.lower()


@mcp.tool()
def to_title_case(text: str) -> str:
    """Convert text to title case (first letter of each word capitalized).

    Use this tool when you need proper title formatting where the first
    letter of every word is uppercase and remaining letters are lowercase.
    Also known as "Title Case" or "Proper Case".

    Args:
        text: The text to convert to title case

    Returns:
        The text with the first letter of each word capitalized

    Example:
        to_title_case("hello world") returns "Hello World"
        to_title_case("HELLO WORLD") returns "Hello World"
        to_title_case("the quick brown fox") returns "The Quick Brown Fox"
    """
    return text.title()


@mcp.tool()
def capitalize_first(text: str) -> str:
    """Capitalize only the first letter of the text.

    Use this tool when you need sentence-style capitalization where only
    the very first letter is uppercase and everything else is lowercase.
    Different from title case which capitalizes every word.

    Args:
        text: The text to capitalize

    Returns:
        The text with only the first letter capitalized

    Example:
        capitalize_first("hello world") returns "Hello world"
        capitalize_first("HELLO WORLD") returns "Hello world"
    """
    return text.capitalize()


# Run with streamable HTTP transport
if __name__ == "__main__":
    mcp.run(transport="streamable-http")
