import { createMcpHandler } from "mcp-handler";
import { z } from "zod";

const handler = createMcpHandler(
  (server) => {
    server.tool(
      "do-arjun",
      "Run Arjun to discover hidden HTTP parameters.",
      {
        url: z.string().url().describe("Target URL to scan for hidden parameters"),
        textFile: z.string().optional().describe("Path to file containing multiple URLs"),
        wordlist: z.string().optional().describe("Path to custom wordlist file"),
        method: z.enum(["GET", "POST", "JSON", "HEADERS"]).optional().describe("HTTP method to use for scanning (default: GET)"),
        rateLimit: z.number().optional().describe("Maximum requests per second (default: 9999)"),
        chunkSize: z.number().optional().describe("Chunk size. The number of parameters to be sent at once")
      },
      async ({ url, textFile, wordlist, method, rateLimit, chunkSize }) => {
        const args = [];

        if (url) {
          args.push('-u', url);
        }
        if (textFile) {
          args.push('-f', textFile);
        }
        if (wordlist) {
          args.push('-w', wordlist);
        }
        if (method) {
          args.push('-m', method);
        }
        if (rateLimit) {
          args.push('--rate-limit', rateLimit.toString());
        }
        if (chunkSize) {
          args.push('--chunk-size', chunkSize.toString());
        }

        return {
          content: [{
            type: "text",
            text: `Command: arjun ${args.join(" ")}`
          }]
        };
      }
    );
  },
  {
    capabilities: {
      tools: {
        "do-arjun": {
          description: "Run Arjun to discover hidden HTTP parameters."
        }
      }
    }
  },
  {
    basePath: "/api",
    maxDuration: 60,
    verboseLogs: true
  }
);

export default handler;
