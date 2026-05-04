const withMDX = require('@next/mdx')({
  options: {
    remarkPlugins: [],
    rehypePlugins: [],
  },
});

// Static export mode for GitHub Pages
const isStaticExport = process.env.NEXT_PUBLIC_STATIC_EXPORT === "true";
const basePath = process.env.NEXT_PUBLIC_BASE_PATH || "";

/** @type {import('next').NextConfig} */
const nextConfig = {
  basePath,
  pageExtensions: ['js', 'jsx', 'mdx', 'ts', 'tsx'],
  experimental: {
    mdxRs: false,
  },
  images: {
    unoptimized: true,
  },
  // Static export for GitHub Pages
  ...(isStaticExport && {
    output: "export",
    distDir: "out",
    trailingSlash: true,
  }),
};

module.exports = withMDX(nextConfig);
