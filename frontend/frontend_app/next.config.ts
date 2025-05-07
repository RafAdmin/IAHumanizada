import { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export", // Add this line for static export
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  // If you have dynamic routes with parameters (e.g., /agents/[id]),
  // you might need to configure generateStaticParams if they are not automatically detected.
  // For MVP, login, register, and dashboard are static paths, so this might not be needed yet.
};

export default nextConfig;

