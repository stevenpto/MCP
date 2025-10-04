# Contributing to MCP Servers

Thank you for your interest in contributing to this MCP servers collection!

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/MCP.git`
3. Install dependencies: `npm install`
4. Build the project: `npm run build`

## Adding a New MCP Server

To add a new MCP server to this collection:

1. Create a new directory under `src/servers/` with your server name:
   ```bash
   mkdir src/servers/your-server-name
   ```

2. Create an `index.ts` file in that directory with the following structure:

```typescript
#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

const server = new Server(
  {
    name: "your-server-name",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "your_tool_name",
        description: "What your tool does",
        inputSchema: {
          type: "object",
          properties: {
            param1: {
              type: "string",
              description: "Description of parameter",
            },
          },
          required: ["param1"],
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (!args) {
    return {
      content: [{ type: "text", text: "Error: No arguments provided" }],
      isError: true,
    };
  }

  try {
    switch (name) {
      case "your_tool_name": {
        // Implement your tool logic here
        return {
          content: [
            {
              type: "text",
              text: "Your result",
            },
          ],
        };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    return {
      content: [
        {
          type: "text",
          text: `Error: ${errorMessage}`,
        },
      ],
      isError: true,
    };
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Your Server Name MCP Server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
```

3. Add a start script to `package.json`:
   ```json
   "start:your-server-name": "node dist/servers/your-server-name/index.js"
   ```

4. Build and test your server:
   ```bash
   npm run build
   npm run start:your-server-name
   ```

5. Update the README.md to document your new server

## Development Guidelines

- Follow the existing code style
- Add proper TypeScript types
- Include error handling
- Add descriptive comments where necessary
- Test your changes before submitting
- Update documentation

## Testing

Build and test your changes:
```bash
npm run build
```

## Pull Request Process

1. Ensure your code builds without errors
2. Update the README.md with details of your changes
3. Submit a pull request with a clear description of the changes

## Code of Conduct

Be respectful and constructive in all interactions.

## Questions?

Open an issue if you have questions or need help!
