import { marked } from "marked";
import matter from "gray-matter";
import sanitizeHtml from "sanitize-html";

// Configure marked for Chinese-friendly output
marked.setOptions({
  gfm: true,
  breaks: true,
});

// Allowed HTML tags and attributes after sanitization
const SANITIZE_OPTIONS = {
  allowedTags: sanitizeHtml.defaults.allowedTags.concat([
    "div", "span", "table", "thead", "tbody", "tr", "th", "td",
    "h1", "h2", "h3", "h4", "h5", "h6",
    "img", "code", "pre", "blockquote",
    "strong", "em", "del", "sub", "sup",
  ]),
  allowedAttributes: {
    ...sanitizeHtml.defaults.allowedAttributes,
    "*": ["class", "style", "data-*"],
    "a": ["href", "name", "target", "rel"],
    "img": ["src", "srcset", "alt", "title", "width", "height", "loading"],
    "div": ["class", "data-*"],
    "code": ["class", "data-lang"],
  },
  allowedSchemes: ["http", "https", "mailto", "tel"],
};

/**
 * Convert course MDX content to sanitized HTML.
 * Strips YAML frontmatter and converts markdown to HTML.
 */
export function renderMDXContent(mdxContent: string): string {
  // Extract frontmatter
  const { content } = matter(mdxContent);

  // Convert markdown to HTML
  const html = marked.parse(content) as string;

  // Sanitize to prevent XSS
  return sanitizeHtml(html, SANITIZE_OPTIONS);
}
