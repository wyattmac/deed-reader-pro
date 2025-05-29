# MCP (Model Context Protocol) Installation Guide

## Prerequisites
- Node.js installed (v18+ recommended)
- Claude Desktop application
- npm or npx available

## Top 5 MCPs to Install

### 1. MCP Filesystem
Enhanced file system operations beyond basic read/write.

```bash
npm install -g @modelcontextprotocol/server-filesystem
```

### 2. MCP Git
Full Git version control capabilities.

```bash
npm install -g @modelcontextprotocol/server-git
```

### 3. MCP SQLite
Database operations for SQLite.

```bash
npm install -g @modelcontextprotocol/server-sqlite
```

### 4. MCP Fetch
HTTP requests and API interactions.

```bash
npm install -g @modelcontextprotocol/server-fetch
```

### 5. MCP Memory
Persistent memory/notes across conversations.

```bash
npm install -g @modelcontextprotocol/server-memory
```

## Configuration

After installation, you need to configure Claude Desktop. The configuration file is located at:

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux**: `~/.config/claude/claude_desktop_config.json`

## Sample Configuration

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/"
      ]
    },
    "git": {
      "command": "npx",
      "args": [
        "-y", 
        "@modelcontextprotocol/server-git"
      ]
    },
    "sqlite": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-sqlite",
        "--db-path",
        "~/databases/mydata.db"
      ]
    },
    "fetch": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-fetch"
      ]
    },
    "memory": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory",
        "--notes-path", 
        "~/Documents/claude-memory"
      ]
    }
  }
}
```

## Installation Steps

1. **Open Command Prompt/Terminal as Administrator**
2. **Install the MCPs globally**:
   ```bash
   npm install -g @modelcontextprotocol/server-filesystem @modelcontextprotocol/server-git @modelcontextprotocol/server-sqlite @modelcontextprotocol/server-fetch @modelcontextprotocol/server-memory
   ```

3. **Create/Edit the configuration file**
4. **Restart Claude Desktop**

## Verify Installation

After restarting Claude Desktop, you should see the MCP servers listed in the bottom right corner of the Claude interface.

## Usage Examples

### Filesystem MCP
- Better file navigation
- Directory operations
- File search capabilities

### Git MCP
- `git status`, `git add`, `git commit`
- Branch operations
- History viewing

### SQLite MCP
- Create and query databases
- Execute SQL commands
- Data analysis

### Fetch MCP
- Make HTTP requests
- Interact with APIs
- Download content

### Memory MCP
- Store persistent notes
- Remember context across conversations
- Create knowledge base