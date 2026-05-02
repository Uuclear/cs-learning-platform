"use client";

import { useState } from "react";
import { Copy, Check } from "lucide-react";
import { Button } from "@/components/ui/Button";

interface CodeBlockProps {
  code: string;
  language: string;
  filename?: string;
}

export function CodeBlock({ code, language, filename }: CodeBlockProps) {
  const [copied, setCopied] = useState(false);

  const copyToClipboard = async () => {
    await navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const languageColors: Record<string, string> = {
    python: "bg-blue-500",
    javascript: "bg-yellow-500",
    typescript: "bg-blue-600",
    go: "bg-cyan-500",
    rust: "bg-orange-500",
    java: "bg-red-500",
    cpp: "bg-purple-500",
    c: "bg-gray-600",
    html: "bg-orange-600",
    css: "bg-blue-400",
    bash: "bg-green-600",
    shell: "bg-green-600",
    json: "bg-gray-500",
    yaml: "bg-red-400",
    markdown: "bg-gray-700",
  };

  return (
    <div className="relative group my-6">
      {/* Header with language and filename */}
      <div className="flex items-center justify-between bg-slate-800 text-slate-200 px-4 py-2 rounded-t-lg">
        <div className="flex items-center gap-2">
          <span
            className={`w-3 h-3 rounded-full ${
              languageColors[language] || "bg-gray-500"
            }`}
          />
          <span className="text-sm font-medium">{language}</span>
          {filename && (
            <span className="text-sm text-slate-400">| {filename}</span>
          )}
        </div>
        <Button
          variant="ghost"
          size="sm"
          onClick={copyToClipboard}
          className="h-8 px-2 text-slate-300 hover:text-white hover:bg-slate-700"
        >
          {copied ? (
            <>
              <Check className="h-4 w-4 mr-1" />
              已复制
            </>
          ) : (
            <>
              <Copy className="h-4 w-4 mr-1" />
              复制
            </>
          )}
        </Button>
      </div>

      {/* Code content */}
      <div className="relative">
        <pre className="rounded-t-none rounded-b-lg overflow-x-auto">
          <code className={`language-${language}`}>{code}</code>
        </pre>
      </div>
    </div>
  );
}
