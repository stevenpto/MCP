#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

// Mock weather data
const mockWeatherData: Record<string, any> = {
  "new york": {
    city: "New York",
    temperature: 72,
    unit: "F",
    conditions: "Partly cloudy",
    humidity: 65,
    windSpeed: 12,
  },
  london: {
    city: "London",
    temperature: 18,
    unit: "C",
    conditions: "Rainy",
    humidity: 80,
    windSpeed: 15,
  },
  tokyo: {
    city: "Tokyo",
    temperature: 25,
    unit: "C",
    conditions: "Sunny",
    humidity: 55,
    windSpeed: 8,
  },
  paris: {
    city: "Paris",
    temperature: 20,
    unit: "C",
    conditions: "Cloudy",
    humidity: 70,
    windSpeed: 10,
  },
  sydney: {
    city: "Sydney",
    temperature: 22,
    unit: "C",
    conditions: "Clear",
    humidity: 60,
    windSpeed: 18,
  },
};

const server = new Server(
  {
    name: "weather-server",
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
        name: "get_weather",
        description:
          "Get current weather information for a city (mock data). Supported cities: New York, London, Tokyo, Paris, Sydney",
        inputSchema: {
          type: "object",
          properties: {
            city: {
              type: "string",
              description: "Name of the city to get weather for",
            },
          },
          required: ["city"],
        },
      },
      {
        name: "get_forecast",
        description: "Get 3-day weather forecast for a city (mock data)",
        inputSchema: {
          type: "object",
          properties: {
            city: {
              type: "string",
              description: "Name of the city to get forecast for",
            },
          },
          required: ["city"],
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
    const city = (args.city as string).toLowerCase();

    switch (name) {
      case "get_weather": {
        const weather = mockWeatherData[city];
        if (!weather) {
          throw new Error(
            `Weather data not available for ${args.city}. Supported cities: New York, London, Tokyo, Paris, Sydney`
          );
        }
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(weather, null, 2),
            },
          ],
        };
      }

      case "get_forecast": {
        const currentWeather = mockWeatherData[city];
        if (!currentWeather) {
          throw new Error(
            `Weather data not available for ${args.city}. Supported cities: New York, London, Tokyo, Paris, Sydney`
          );
        }
        
        // Generate mock 3-day forecast
        const forecast = [
          {
            day: "Today",
            ...currentWeather,
          },
          {
            day: "Tomorrow",
            city: currentWeather.city,
            temperature: currentWeather.temperature + 2,
            unit: currentWeather.unit,
            conditions: "Partly cloudy",
            humidity: currentWeather.humidity - 5,
            windSpeed: currentWeather.windSpeed + 3,
          },
          {
            day: "Day After Tomorrow",
            city: currentWeather.city,
            temperature: currentWeather.temperature - 1,
            unit: currentWeather.unit,
            conditions: "Cloudy",
            humidity: currentWeather.humidity + 10,
            windSpeed: currentWeather.windSpeed - 2,
          },
        ];

        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(forecast, null, 2),
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
  console.error("Weather MCP Server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
