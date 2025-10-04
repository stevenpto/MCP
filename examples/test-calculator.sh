#!/bin/bash
# Example script to test the calculator MCP server

echo "Testing Calculator MCP Server"
echo "=============================="
echo ""
echo "Starting calculator server and sending a test request..."
echo ""

# Note: This is a demonstration. In actual usage, MCP servers communicate via stdio
# with an MCP client (like Claude Desktop) using the JSON-RPC protocol.

echo "To use this server with Claude Desktop, add this to your claude_desktop_config.json:"
echo ""
echo '{
  "mcpServers": {
    "calculator": {
      "command": "node",
      "args": ["'$(pwd)'/dist/servers/calculator/index.js"]
    }
  }
}'
echo ""
echo "Then you can ask Claude to perform calculations, and it will use this MCP server."
