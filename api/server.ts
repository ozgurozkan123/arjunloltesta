import { createMcpHandler } from "mcp-handler";
import { z } from "zod";

const handler = createMcpHandler(
  (server) => {
    server.tool(
      "do-arjun",
      "Run Arjun to discover hidden HTTP parameters.",
      {
        url: z.string(),
        textFile: z.string().optional(),
        wordlist: z.string().optional(),
        method: z.union([z.literal('GET'), z.literal('POST'), z.literal('JSON'), z.literal('HEADERS')]).optional(),
        rateLimit: z.any().optional(),
        chunkSize: z.any().optional()
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
