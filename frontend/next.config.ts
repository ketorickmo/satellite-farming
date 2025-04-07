/** @type {import('next').NextConfig} */
const nextConfig = {
  webpack: (config: any) => {
    // Resolve mapbox-gl issues with Next.js
    config.resolve.alias = {
      ...config.resolve.alias,
      'mapbox-gl': 'mapbox-gl'
    };
    return config;
  },
  // Add transpilePackages to avoid issues with mapbox-gl
  transpilePackages: ['mapbox-gl'],
  // Ensure environment variables are properly loaded
  env: {
    NEXT_PUBLIC_MAPBOX_ACCESS_TOKEN: process.env.NEXT_PUBLIC_MAPBOX_ACCESS_TOKEN
  }
};

export default nextConfig;
