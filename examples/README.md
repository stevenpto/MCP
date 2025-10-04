# Examples

This directory contains example scripts and configuration for using the MCP servers.

## Usage with Claude Desktop

To use these MCP servers with Claude Desktop, you need to configure them in your Claude Desktop configuration file.

### Configuration Location

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

### Example Configuration

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "node",
      "args": ["/absolute/path/to/MCP/dist/servers/filesystem/index.js"]
    },
    "calculator": {
      "command": "node",
      "args": ["/absolute/path/to/MCP/dist/servers/calculator/index.js"]
    },
    "weather": {
      "command": "node",
      "args": ["/absolute/path/to/MCP/dist/servers/weather/index.js"]
    }
  }
}
```

Replace `/absolute/path/to/MCP` with the actual path to your MCP repository.

## Testing the Servers

After adding the servers to your configuration:

1. Restart Claude Desktop
2. Open a new conversation
3. Try asking questions that would use the tools:
   - "Can you add 15 and 27?" (uses calculator)
   - "What's the weather like in Tokyo?" (uses weather server)
   - "List the files in my home directory" (uses filesystem server)

Claude will automatically use the appropriate MCP server tools to answer your questions.
