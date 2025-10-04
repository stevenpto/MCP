# MCP Servers Collection

A collection of Model Context Protocol (MCP) server implementations demonstrating various use cases and capabilities.

## Overview

This repository contains multiple MCP server implementations that can be used with AI assistants that support the Model Context Protocol. Each server provides different tools and capabilities.

## Available Servers

### 1. Filesystem Server
Provides tools for file system operations:
- **read_file**: Read contents of a file
- **write_file**: Write content to a file
- **list_directory**: List contents of a directory

### 2. Calculator Server
Provides basic mathematical operations:
- **add**: Add two numbers
- **subtract**: Subtract two numbers
- **multiply**: Multiply two numbers
- **divide**: Divide two numbers

### 3. Weather Server
Provides weather information (mock data):
- **get_weather**: Get current weather for a city
- **get_forecast**: Get 3-day weather forecast

Supported cities: New York, London, Tokyo, Paris, Sydney

## Installation

1. Clone the repository:
```bash
git clone https://github.com/stevenpto/MCP.git
cd MCP
```

2. Install dependencies:
```bash
npm install
```

3. Build the TypeScript code:
```bash
npm run build
```

## Usage

Each server can be run independently using npm scripts:

```bash
# Run the filesystem server
npm run start:filesystem

# Run the calculator server
npm run start:calculator

# Run the weather server
npm run start:weather
```

## Configuration with Claude Desktop

To use these servers with Claude Desktop, add them to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "node",
      "args": ["/path/to/MCP/dist/servers/filesystem/index.js"]
    },
    "calculator": {
      "command": "node",
      "args": ["/path/to/MCP/dist/servers/calculator/index.js"]
    },
    "weather": {
      "command": "node",
      "args": ["/path/to/MCP/dist/servers/weather/index.js"]
    }
  }
}
```

## Development

### Project Structure

```
MCP/
├── src/
│   └── servers/
│       ├── filesystem/
│       │   └── index.ts
│       ├── calculator/
│       │   └── index.ts
│       └── weather/
│           └── index.ts
├── dist/                 # Compiled JavaScript (generated)
├── package.json
├── tsconfig.json
└── README.md
```

### Building

```bash
npm run build
```

This compiles the TypeScript code to JavaScript in the `dist/` directory.

## Requirements

- Node.js 18 or higher
- npm or yarn

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.