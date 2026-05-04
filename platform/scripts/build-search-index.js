#!/usr/bin/env node
/**
 * Build static search index for GitHub Pages deployment.
 * Outputs a JSON file that the client-side SearchBar can fetch.
 */
const path = require("path");
const fs = require("fs");

const COURSES_DIR = path.resolve(__dirname, "../../courses");
const OUTPUT_DIR = path.resolve(__dirname, "../public");
const OUTPUT_FILE = path.join(OUTPUT_DIR, "search-index.json");

function stripMarkdown(text) {
  return text
    .replace(/```[\s\S]*?```/g, "")
    .replace(/`[^`]*`/g, "")
    .replace(/#{1,6}\s?/g, "")
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
    .replace(/!\[([^\]]*)\]\([^)]+\)/g, "$1")
    .replace(/[*_~`>|-]/g, "")
    .replace(/\n+/g, " ")
    .trim();
}

function loadCourseMetadata(metaPath) {
  const raw = fs.readFileSync(metaPath, "utf-8");
  return JSON.parse(raw);
}

function buildIndex() {
  if (!fs.existsSync(COURSES_DIR)) {
    console.log("No courses directory found");
    return [];
  }

  const index = [];
  const modules = fs.readdirSync(COURSES_DIR, { withFileTypes: true })
    .filter(d => d.isDirectory())
    .map(d => d.name)
    .sort();

  for (const mod of modules) {
    const modPath = path.join(COURSES_DIR, mod);
    const lessons = fs.readdirSync(modPath, { withFileTypes: true })
      .filter(d => d.isDirectory())
      .map(d => d.name)
      .sort();

    for (const lesson of lessons) {
      const metaPath = path.join(modPath, lesson, "metadata.json");
      if (!fs.existsSync(metaPath)) continue;

      const meta = loadCourseMetadata(metaPath);
      const indexPath = path.join(modPath, lesson, "index.mdx");
      let content = "";
      if (fs.existsSync(indexPath)) {
        content = stripMarkdown(fs.readFileSync(indexPath, "utf-8"));
      }

      index.push({
        courseId: meta.id,
        title: meta.title,
        moduleName: meta.module_name || mod.replace(/^\d+-/, "").replace(/-/g, " "),
        slug: meta.slug,
        excerpt: content.substring(0, 200),
        matchType: "content",
      });
    }
  }

  return index;
}

// Ensure output directory exists
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

const index = buildIndex();
fs.writeFileSync(OUTPUT_FILE, JSON.stringify(index, null, 2));
console.log(`✓ Search index built: ${index.length} courses → ${OUTPUT_FILE}`);
