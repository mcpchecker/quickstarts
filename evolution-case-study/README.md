# Case Study: Evolving from Bad to Good MCP Tooling

> **See how documentation quality affects AI agent success**

This case study demonstrates the power of MCPChecker by showing the same MCP server with **identical functionality** but **different documentation quality**.

## The Experiment

We have **one text processing server** with 4 tools, all text transformation-related:
- `process` / `to_uppercase` - Convert to uppercase
- `transform` / `to_lowercase` - Convert to lowercase
- `convert` / `to_title_case` - Convert to title case
- `format_text` / `capitalize_first` - Capitalize first letter only

**The implementation is identical across both iterations. Only the documentation changes.**

## Why Text Processing Tools?

All 4 tools "transform text" but in different ways. With bad documentation (generic names), the agent can't tell which tool does what. With good documentation, it's crystal clear.

## Two Iterations

### Iteration 1: Bad Documentation
**Location:** `iteration-1-bad/`

Misleading generic names, vague descriptions, no type hints:

```python
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
```

**Problems:**
- ❌ Misleading generic names (`process`, `transform`, `convert`, `format_text`)
- ❌ Names give ZERO hint about what transformation they perform
- ❌ Vague descriptions (doesn't explain what processing/transforming means)
- ❌ No examples
- ❌ No guidance on **when** to use each tool
- ❌ "Process text" could mean anything - uppercase? lowercase? something else?

### Iteration 2: Good Documentation
**Location:** `iteration-2-good/`

Full docstrings with examples, clear names, use case guidance:

```python
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

# ... and so on for to_title_case and capitalize_first
```

**Best practices:**
- ✅ Descriptive names (`to_uppercase`, `to_lowercase`, `to_title_case`)
- ✅ Full docstrings with Args/Returns
- ✅ Examples provided
- ✅ Explains **when** to use each tool
- ✅ Clarifies the differences between similar tools
- ✅ "ALL CAPS format" vs "all lowercase format" - immediately clear

## The Test Tasks

Both iterations are tested with the **same natural language prompts** that don't mention tool names.

> **Note:** The examples below are simplified pseudocode to illustrate the test concepts. The actual test files use the full MCPChecker YAML structure. See `evals/tasks/` directories for complete task definitions.

### Task 1: Uppercase Conversion
```yaml
prompt: |
  I have this text: hello world

  Please convert it to all uppercase letters.
verify: Result contains "HELLO WORLD"
expected_tool: process (bad) / to_uppercase (good)
```

### Task 2: Lowercase Conversion
```yaml
prompt: |
  I have this text: HELLO WORLD

  Please convert it to all lowercase letters.
verify: Result contains "hello world"
expected_tool: transform (bad) / to_lowercase (good)
```

### Task 3: Title Case
```yaml
prompt: |
  I have this text: hello world

  Please format it with title case (first letter of each word capitalized).
verify: Result contains "Hello World"
expected_tool: convert (bad) / to_title_case (good)
```

## Actual Results

Since the **code is identical**, differences in test results prove documentation quality matters:

| Task | Iteration 1 (Bad Docs) | Iteration 2 (Good Docs) |
|------|------------------------|-------------------------|
| Uppercase conversion | ❌ FAILED (assertions) | ✅ PASSED |
| Lowercase conversion | ❌ FAILED (assertions) | ✅ PASSED |
| Title case formatting | ❌ FAILED | ✅ PASSED |

**Actual pass rates:**
- **Iteration 1 (Bad):** 0/3 tests fully passed, 6/9 assertions passed
- **Iteration 2 (Good):** 3/3 tests passed, 9/9 assertions passed

> **About assertions:** Each test checks multiple MCP-specific assertions:
> - **minToolCalls: 1** - Agent must call at least one tool (can't just calculate the answer)
> - **maxToolCalls: 5** - Agent can't try unlimited tools (prevents brute-force guessing)
> - **toolsUsed** - Agent must call the specific expected tool (e.g., `to_uppercase` for uppercase conversion)
>
> In the bad iteration, the agent sometimes got the correct output but failed because it called the wrong tool or tried too many tools trying to figure out which generic name did what.

**What happened in the bad iteration:**
- Agent couldn't discover which generic tool (`process`, `transform`, `convert`) does what
- Even when it got correct answers (by exploring tools), it failed assertions because it didn't call the expected tools
- Generic names like "process text" don't hint at uppercase conversion

**What happened in the good iteration:**
- Clear tool names (`to_uppercase`, `to_lowercase`) made it obvious which to use
- Agent found the correct tools immediately
- All tests passed

## Running the Case Study

### Prerequisites

See [getting-started](../getting-started/) for installation of:
- Claude Code
- mcpchecker
- uv (Python package manager)

Set judge LLM environment variables:
```bash
export JUDGE_BASE_URL="https://api.openai.com/v1"
export JUDGE_API_KEY="sk-your-key-here"
export JUDGE_MODEL_NAME="gpt-4o-mini"
```

### Run Both Iterations

**Iteration 1 - Bad Documentation:**
```bash
cd iteration-1-bad

# Terminal 1: Start server
cd server
PORT=8000 ./server.py

# Terminal 2: Run tests
cd evals
mcpchecker check eval.yaml
```

**Iteration 2 - Good Documentation:**
```bash
cd iteration-2-good

# Terminal 1: Start server (stop previous first)
cd server
PORT=8000 ./server.py

# Terminal 2: Run tests
cd evals
mcpchecker check eval.yaml
```

### Compare Results

After running both, compare the JSON output files:
- `text-processing-bad-test-out.json`
- `text-processing-good-test-out.json`

You'll see the same code producing different test results based purely on documentation quality.

## Key Takeaways

1. **Similar tools need clear differentiation** - When multiple tools do related things (text transformations), documentation is critical
2. **MCPChecker validates discoverability** - Tests pass/fail based on whether agents can find and use the RIGHT tool
3. **Generic names are useless** - `process`, `transform`, `convert` give zero hint about what the tool does, compared to `to_uppercase`, `to_lowercase`, `to_title_case`
4. **Examples clarify usage** - Iteration 2's examples help agents understand exactly what each transformation does
5. **"Use this when..." guidance matters** - Explicitly stating use cases prevents tool confusion
6. **Vague descriptions hurt** - "Process text" could mean anything; "Convert all letters to uppercase" is actionable

## Code Comparison

### Side-by-Side: Uppercase Tool

| Iteration 1 (Bad) | Iteration 2 (Good) |
|-------------------|-------------------|
| `def process(text: str):` | `def to_uppercase(text: str) -> str:` |
| `"""Process text"""` | Full docstring with "Use this when...", Args, Returns, Examples |
| Name gives no hint what processing means | Name clearly indicates uppercase conversion |
| No examples | 2 examples showing exact usage |
| Vague "process" | Specific "ALL CAPS format" description |

The **exact same implementation** (`return text.upper()`) but vastly different discoverability.

## What This Proves

MCPChecker doesn't just test if your tools **work** - it tests if they're **usable by AI agents**.

You can have perfectly functional code that fails MCPChecker tests because:
- Tool names are misleading or generic (`process`, `transform` tell you nothing)
- Descriptions don't explain differences between similar tools
- No examples to learn from
- Unclear when to use this tool vs alternatives
- No guidance on what "processing" or "transforming" actually means

**Good documentation = passing tests = agents can actually use your tools.**

## Next Steps

- Check out the [main documentation](https://github.com/mcpchecker/mcpchecker) for advanced features
