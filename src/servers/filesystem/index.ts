#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import fs from "fs/promises";
import path from "path";

const server = new Server(
  {
    name: "filesystem-server",
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
        name: "read_file",
        description: "Read the contents of a file from the filesystem",
        inputSchema: {
          type: "object",
          properties: {
            path: {
              type: "string",
              description: "Path to the file to read",
            },
          },
          required: ["path"],
        },
      },
      {
        name: "write_file",
        description: "Write content to a file on the filesystem",
        inputSchema: {
          type: "object",
          properties: {
            path: {
              type: "string",
              description: "Path to the file to write",
            },
            content: {
              type: "string",
              description: "Content to write to the file",
            },
          },
          required: ["path", "content"],
        },
      },
      {
        name: "list_directory",
        description: "List contents of a directory",
        inputSchema: {
          type: "object",
          properties: {
            path: {
              type: "string",
              description: "Path to the directory to list",
            },
          },
          required: ["path"],
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
      case "read_file": {
        const filePath = args.path as string;
        const content = await fs.readFile(filePath, "utf-8");
        return {
          content: [
            {
              type: "text",
              text: content,
            },
          ],
        };
      }

      case "write_file": {
        const filePath = args.path as string;
        const content = args.content as string;
        await fs.writeFile(filePath, content, "utf-8");
        return {
          content: [
            {
              type: "text",
              text: `Successfully wrote to ${filePath}`,
            },
          ],
        };
      }

      case "list_directory": {
        const dirPath = args.path as string;
        const entries = await fs.readdir(dirPath, { withFileTypes: true });
        const items = entries.map((entry) => ({
          name: entry.name,
          type: entry.isDirectory() ? "directory" : "file",
        }));
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(items, null, 2),
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
  console.error("Filesystem MCP Server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
