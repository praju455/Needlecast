import { resolve } from "node:path";
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import type { NextConfig } from "next";

const requireFromDashboard = createRequire(resolve(process.cwd(), "package.json"));

function available(name: string) {
  try {
    requireFromDashboard.resolve(name);
    return true;
  } catch {
    return false;
  }
}

const options: NextConfig = {
  output: "standalone",
  outputFileTracingRoot: resolve(process.cwd(), ".."),
  env: {
    NEXT_PUBLIC_APP_VERSION: readFileSync(resolve(process.cwd(), "../VERSION"), "utf8").trim(),
    NEXT_PUBLIC_CHARTS_AVAILABLE: String(available("echarts") && available("echarts-for-react")),
  },
  async rewrites() {
    const server = (process.env.BACKEND_URL ?? "http://127.0.0.1:8000").replace(/\/$/, "");
    return [{ source: "/api/:path*", destination: `${server}/api/:path*` }];
  },
  webpack(config) {
    if (!available("echarts") || !available("echarts-for-react")) {
      config.resolve.alias["echarts-for-react$"] = resolve(
        process.cwd(), "src/components/charts/unavailable.tsx",
      );
    }
    return config;
  },
};

export default options;
