# Linux MCP Server Quickstart

> **Test your local system diagnostics MCP server with MCPChecker**

This quickstart demonstrates how to test a **stdio-based MCP server** that runs diagnostics on your local Linux system. Unlike HTTP-based servers, stdio servers communicate over standard input/output.

## What You'll Learn

- How to configure MCPChecker to test stdio/local MCP servers
- How to write evals for system diagnostic tools
- How natural language tasks test tool discoverability
- Best practices for testing read-only diagnostic tools

## Why MCPChecker?

The Linux MCP Server provides many diagnostic tools. MCPChecker helps you verify that:

- **Tool names are discoverable** - Can agents find the right tool from natural language requests?
- **Documentation is clear** - Do descriptions guide agents to use the correct tool?
- **Tools work as expected** - Does the output match what you expect?

This is especially important for diagnostic tools where choosing the wrong tool could waste time or provide incorrect information.

## Prerequisites

### 1. Install Claude Code

Claude Code acts as the AI agent for testing:

```bash
curl -fsSL https://anthropic.com/install-claude-code | sh
```

For more installation options, see the [official installation guide](https://github.com/anthropics/claude-code).

### 2. Install MCPChecker

Download the latest release:

```bash
# For Linux (adjust version as needed)
curl -LO https://github.com/mcpchecker/mcpchecker/releases/download/v0.1.0/mcpchecker-linux-amd64
chmod +x mcpchecker-linux-amd64
sudo mv mcpchecker-linux-amd64 /usr/local/bin/mcpchecker
```

### 3. Install Linux MCP Server

```bash
pip install --user linux-mcp-server
```

This installs the server to `~/.local/bin/linux-mcp-server`. Make sure `~/.local/bin` is in your PATH:

```bash
# Add to your ~/.bashrc or ~/.zshrc if needed
export PATH="$HOME/.local/bin:$PATH"

# Verify installation
which linux-mcp-server
```

For more installation options and documentation, see the [Linux MCP Server documentation](https://rhel-lightspeed.github.io/linux-mcp-server/).

### 4. Configure Judge LLM

MCPChecker uses an LLM to verify test results. Set these environment variables:

```bash
export JUDGE_BASE_URL="https://api.openai.com/v1"
export JUDGE_API_KEY="sk-your-key-here"
export JUDGE_MODEL_NAME="gpt-4o-mini"
```

**Why a judge LLM?** Testing AI agents requires flexible verification. Instead of exact string matching, we use an LLM to verify if the output is semantically correct.

For example, instead of checking for the exact string "Fedora Linux 43", the judge checks if the output "contains information about the operating system". This allows the test to pass even if the formatting varies, as long as the required information is present.

Each verification step includes a `reason` explaining what the judge is checking, which helps with debugging when tests fail.

## What Gets Tested

This quickstart tests two diagnostic tools from the Linux MCP Server:

### Tool 1: get_system_information
```python
@mcp.tool(
    title="Get system information",
    description="Get basic system information such as operating system, distribution, kernel version, uptime, and last boot time.",
    tags={"hardware", "system"},
)
async def get_system_information(host: Host = None) -> SystemInfo:
    """Get basic system information.

    Retrieves hostname, OS name/version, kernel version, architecture,
    system uptime, and last boot time.
    """
```

### Tool 2: get_disk_usage
```python
@mcp.tool(
    title="Get disk usage",
    description="Get detailed disk space information including size, mount points, and utilization.",
    tags={"disk", "filesystem", "storage", "system"},
)
async def get_disk_usage(host: Host = None) -> DiskUsage:
    """Get disk usage information.

    Retrieves filesystem usage for all mounted volumes including size,
    used/available space, utilization percentage, and mount points.
    """
```

## The Test Tasks

Both tools are tested with **natural language prompts** that don't mention specific tool names:

### Task 1: System Information (`evals/tasks/system-info.yaml`)

```yaml
kind: Task
apiVersion: mcpchecker/v1alpha2
metadata:
  name: "system-info-test"
  difficulty: easy
  description: |
    Tests if the agent can discover the get_system_information tool from a natural
    language request for "basic information about this Linux system". The judge
    verifies that the output contains OS and kernel information as requested.
spec:
  verify:
    - llmJudge:
        contains: "operating system"
        reason: "Verify the output identifies the operating system (e.g., 'Fedora Linux 43')"
    - llmJudge:
        contains: "kernel"
        reason: "Verify the output includes the kernel version as requested"
  prompt:
    inline: |
      I need to know basic information about this Linux system.

      Please tell me what operating system it's running and the kernel version.
```

**What this tests:**
- **Tool discovery:** Can the agent find `get_system_information` from "basic information about this Linux system"?
- **Documentation clarity:** Does the tool's description guide the agent correctly?
- **Output verification:** The judge LLM verifies that:
  - The output mentions the operating system (e.g., "Fedora Linux 43")
  - The output includes the kernel version as requested

### Task 2: Disk Usage (`evals/tasks/disk-usage.yaml`)

```yaml
kind: Task
apiVersion: mcpchecker/v1alpha2
metadata:
  name: "disk-usage-test"
  difficulty: easy
  description: |
    Tests if the agent can discover the get_disk_usage tool from a natural language
    request about disk space. The judge verifies that the output contains disk space
    information including available space and filesystem details.
spec:
  verify:
    - llmJudge:
        contains: "disk space"
        reason: "Verify the output discusses disk space (not just 'disk' or 'usage' separately)"
    - llmJudge:
        contains: "available"
        reason: "Verify the output shows available/free space, which was requested"
  prompt:
    inline: |
      I want to check how much disk space is available on this system.

      Please show me the disk usage information.
```

**What this tests:**
- **Tool discovery:** Can the agent find `get_disk_usage` from "disk space available"?
- **Documentation clarity:** Does the description clearly indicate this tool shows disk usage?
- **Output verification:** The judge LLM verifies that:
  - The output discusses disk space (contains "disk space" or similar)
  - The output shows available/free space, since that's what was requested

## Expected Output

When you run the tests, you should see:

```
Task: system-info-test
  Difficulty: easy                                                                                                                                                                                                                                                                                                  
  → Running agent...
  → Verifying results...
  ✓ Task passed
                                                                                                                                                                                                                                                                                                                    
Task: disk-usage-test
  Difficulty: easy                                                                                                                                                                                                                                                                                                  
  → Running agent...
  → Verifying results...
  ✓ Task passed
```

## Running the Tests

### Configure the Server

The MCP configuration (`evals/mcp-config.yaml`) tells MCPChecker how to connect to the stdio server:

```yaml
mcpServers:
  linux-server:
    type: stdio
    command: linux-mcp-server
    args: []
    enableAllTools: true
```

**Key differences from HTTP servers:**
- `type: stdio` - Server communicates via stdin/stdout
- `command` - Executable name (must be on PATH) or absolute path
- `args` - Command-line arguments (empty for this server)
- No need to start a separate server process
- MCPChecker manages the subprocess lifecycle automatically

### Run the Tests

```bash
cd evals
mcpchecker check eval.yaml
```

The command will:
1. Start the linux-mcp-server as a subprocess
2. Connect Claude Code to it
3. Run each test task
4. Verify the results with the judge LLM
5. Report pass/fail for each test

### Review Results

Check the output file:

```bash
cat linux-diagnostic-test-out.json
```

This contains detailed information about:
- Which tools were called
- What arguments were used
- The actual output
- Judge verification results

## What This Demonstrates

**Tool Discoverability:**
- The tasks use natural language ("basic information about this Linux system")
- The agent must find the right tool based on descriptions
- Clear tool names (`get_system_information`, `get_disk_usage`) help discoverability

**Documentation Quality:**
- Good descriptions guide agents to the right tool
- Tags (`hardware`, `system`, `disk`, `filesystem`) provide additional context
- Docstrings explain what information is retrieved

**Stdio Transport:**
- Unlike HTTP servers, no separate server process needed
- MCPChecker manages the subprocess lifecycle
- Simpler setup for local-only servers
