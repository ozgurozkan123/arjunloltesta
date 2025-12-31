import { createMcpHandler } from "mcp-handler";
import { z } from "zod";
import { spawn } from "child_process";

const handler = createMcpHandler(
  async (server) => {
    server.tool(
      "amass",
      "Advanced subdomain enumeration and reconnaissance tool (runs amass inside the container)",
      {
        subcommand: z
          .enum(["enum", "intel"])
          .describe(
            "Amass operation mode: 'intel' gathers intelligence, 'enum' performs subdomain enumeration"
          ),
        domain: z
          .string()
          .optional()
          .describe("Target domain (e.g., example.com)"),
        intel_whois: z
          .boolean()
          .optional()
          .describe("Include WHOIS data when gathering intelligence"),
        intel_organization: z
          .string()
          .optional()
          .describe("Organization name to search during intelligence gathering"),
        enum_type: z
          .enum(["active", "passive"])
          .optional()
          .describe("Enumeration approach; passive avoids direct interaction"),
        enum_brute: z
          .boolean()
          .optional()
          .describe("Enable brute force subdomain discovery"),
        enum_brute_wordlist: z
          .string()
          .optional()
          .describe("Path to custom wordlist for brute force")
      },
      async ({
        subcommand,
        domain,
        intel_whois,
        intel_organization,
        enum_type,
        enum_brute,
        enum_brute_wordlist
      }) => {
        const amassArgs: string[] = [subcommand];

        if (subcommand === "enum") {
          if (!domain) {
            throw new Error("domain is required for 'enum'");
          }
          amassArgs.push("-d", domain);
          if (enum_type === "passive") {
            amassArgs.push("-passive");
          }
          if (enum_brute === true) {
            amassArgs.push("-brute");
            if (enum_brute_wordlist) {
              amassArgs.push("-w", enum_brute_wordlist);
            }
          }
        }

        if (subcommand === "intel") {
          if (!domain && !intel_organization) {
            throw new Error("Provide domain or intel_organization for 'intel'");
          }
          if (domain) {
            amassArgs.push("-d", domain);
            if (intel_whois === true) {
              amassArgs.push("-whois");
            }
          }
          if (intel_organization) {
            amassArgs.push("-org", intel_organization);
          }
          if (intel_whois === true && !amassArgs.includes("-whois")) {
            amassArgs.push("-whois");
          }
        }

        const commandString = `amass ${amassArgs.join(" ")}`;
        console.log(`Executing: ${commandString}`);

        const child = spawn("amass", amassArgs);
        let output = "";

        child.stdout.on("data", (data) => {
          output += data.toString();
        });
        child.stderr.on("data", (data) => {
          output += data.toString();
        });

        const result = await new Promise<string>((resolve, reject) => {
          child.on("close", (code) => {
            if (code === 0) {
              resolve(output || "(no output)");
            } else {
              reject(new Error(`amass exited with code ${code}. Output: ${output}`));
            }
          });
          child.on("error", (err) => reject(err));
        });

        return {
          content: [
            {
              type: "text",
              text: result
            }
          ]
        };
      }
    );
  },
  {
    capabilities: {
      tools: {
        amass: {
          description: "Advanced subdomain enumeration and reconnaissance tool (runs amass inside the container)"
        }
      }
    }
  } as Parameters<typeof createMcpHandler>[1],
  {
    basePath: "",
    verboseLogs: true,
    maxDuration: 60,
    disableSse: true
  }
);

export { handler as GET, handler as POST, handler as DELETE };
