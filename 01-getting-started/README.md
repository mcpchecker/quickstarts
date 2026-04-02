# Getting Started with MCPChecker

> **Get started with MCPChecker in 5 minutes**

A minimal, batteries-included example showing how to test an HTTP MCP server with MCPChecker.

**What you get:**
- ✅ Working HTTP MCP server (FastMCP official quickstart example)
- ✅ MCPChecker test for the `add` tool
- ✅ One command to run everything
- ✅ Perfect starting point to test your own MCP servers

## Why MCPChecker?

You've built an MCP server with tools. It works. But:
- **Is your tool description clear enough for an LLM to discover it?**
- **Can an AI agent actually use your tool correctly?**
- **Does your tool handle edge cases properly?**

MCPChecker helps you test these questions automatically by:
1. Running real AI agents (like Claude Code) against your tools
2. Verifying agents can discover and use your tools correctly
3. Testing edge cases and error handling
4. Ensuring tool descriptions are clear and actionable

Think of it as integration testing for AI tool use.

## What's Included

- **HTTP MCP Server** (`server/server.py`) - Simple FastMCP server with:
  - `add` tool - Adds two numbers (taken from the official Python-SDK [Quickstart](https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#quickstart))
- **MCPChecker Tests** (`evals/`) - Test task for the `add` tool

The server uses **streamable HTTP transport** with `mcp.run(transport="streamable-http")`.

## Quick Start

### 1. Install Prerequisites

**Install Claude Code** (AI agent):

Claude Code is used as the AI agent that runs the tests.

```bash
# macOS/Linux
curl -fsSL https://claude.ai/install.sh | bash
```

See the [official installation guide](https://github.com/anthropics/claude-code?tab=readme-ov-file#get-started) for Windows and other installation methods.

**Install the Claude ACP agent adapter:**

```bash
npm install -g @agentclientprotocol/claude-agent-acp
```

This provides the `claude-agent-acp` command used by MCPChecker to run Claude Code as an ACP-compatible agent.

**Install uv** (Python package manager):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Install mcpchecker** - Download from [releases](https://github.com/mcpchecker/mcpchecker/releases):

```bash
# Linux (amd64)
curl -L -o mcpchecker https://github.com/mcpchecker/mcpchecker/releases/latest/download/mcpchecker-linux-amd64
chmod +x mcpchecker
sudo mv mcpchecker /usr/local/bin/

# macOS (arm64 - Apple Silicon)
curl -L -o mcpchecker https://github.com/mcpchecker/mcpchecker/releases/latest/download/mcpchecker-darwin-arm64
chmod +x mcpchecker
sudo mv mcpchecker /usr/local/bin/
```

### 2. Start the MCP Server

In one terminal, start the HTTP server:

```bash
cd server
PORT=8000 ./server.py
```

The server will start on `http://localhost:8000/mcp` using streamable HTTP transport.

**Note**: The `PORT` environment variable tells FastMCP which port to use.

### 3. Run the Tests

**Option A: Manual** (two terminals)

In another terminal, run mcpchecker:

```bash
cd evals
mcpchecker check eval.yaml
```

You should see:
```
  Task: add-test
    Path: /../getting-started/evals/tasks/add.yaml
    Difficulty: easy
    Task Status: PASSED
    Assertions: PASSED (3/3)
```

## Understanding the Test Files

This quickstart includes a complete evaluation setup. Let's look at what gets tested and how it's defined:

### The Agent Configuration (`evals/agent.yaml`)

```yaml
kind: Agent
metadata:
  name: "claude-code-acp"
acp:
  cmd: "claude-agent-acp"
```

**What this does:**
- Defines an ACP (Agent Client Protocol) agent that uses Claude Code via the `claude-agent-acp` adapter
- This agent configuration is referenced by both the eval runner and the LLM judge

### The Main Eval Configuration (`evals/eval.yaml`)

```yaml
kind: Eval
metadata:
  name: "demo-server-test"

config:
  # Use Claude Code as the AI agent (via ACP)
  agent:
    type: file
    path: agent.yaml

  # MCP server configuration
  mcpConfigFile: mcp-config.yaml

  # LLM judge configuration (reuses the same agent)
  llmJudge:
    ref:
      type: file
      path: agent.yaml

  # Test tasks
  taskSets:
    - path: tasks/add.yaml
      assertions:
        toolsUsed:
          - server: demo-server
            tool: add
        minToolCalls: 1
        maxToolCalls: 5
```

**What this does:**
- Configures **Claude Code** as the agent via the ACP adapter defined in **agent.yaml**
- Points to **mcp-config.yaml** to connect to your MCP server
- The **LLM judge** also references **agent.yaml**, so no separate judge configuration is needed
- Loads tasks from **tasks/add.yaml** and asserts the `add` tool must be used

### The Task Definition (`evals/tasks/add.yaml`)

```yaml
kind: Task
apiVersion: mcpchecker/v1alpha2
metadata:
  name: "add-test"
  difficulty: easy

spec:
  verify:
    - llmJudge:
        contains: "8"

  prompt:
    inline: |
      I need to know what 5 + 3 equals. Can you help me figure this out?
```

**What this tests:**
- **Natural language prompt**: No mention of tools - agent must discover the `add` tool
- **Verification**: Judge LLM checks that the result contains "8"
- **Tool discovery**: Can the agent find and use the right tool from a simple question?

This tests whether the agent can:
1. **Discover** the `add` tool from its description
2. **Understand** when to use it based on the natural language prompt
3. **Call it correctly** with the right parameters (a=5, b=3)

### The MCP Server Config (`evals/mcp-config.yaml`)

```yaml
mcpServers:
  demo-server:
    type: http
    url: http://localhost:8000/mcp
    enableAllTools: true
```

**What this does:**
- Defines a server named **demo-server**
- Connects via **HTTP** to `http://localhost:8000/mcp`
- **Enables all tools** exposed by the server

## Expected Output

When tests pass, you'll see:

```
✅ add-test: PASSED
  Tool calls:
    - demo-server.add(a=5, b=3) → 8
  Verifications:
    - Result contains "8" ✓
```

The output also generates a JSON file (`demo-server-test-out.json`) with detailed results including:
- Complete agent conversation transcript
- All tool calls made
- Verification results
- Timing information
