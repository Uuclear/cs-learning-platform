"use client";

import { useState, useCallback, useEffect } from "react";
import { SearchIndexItem } from "@/lib/courses";
import { Search, X, BookOpen, Hash, Folder } from "lucide-react";
import Link from "next/link";

interface SearchBarProps {
  mode?: "header" | "page";
}

export function SearchBar({ mode = "header" }: SearchBarProps) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchIndexItem[]>([]);
  const [isFocused, setIsFocused] = useState(false);
  const [loading, setLoading] = useState(false);

  const doSearch = useCallback(async (q: string) => {
    if (q.length < 2) {
      setResults([]);
      return;
    }
    setLoading(true);
    try {
      const res = await fetch(`/api/search?q=${encodeURIComponent(q)}`);
      const data = await res.json();
      setResults(data.results || []);
    } catch {
      setResults([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => doSearch(query), 300);
    return () => clearTimeout(timer);
  }, [query, doSearch]);

  const clearSearch = () => {
    setQuery("");
    setResults([]);
  };

  const getMatchIcon = (type: string) => {
    switch (type) {
      case "title": return <BookOpen className="h-3.5 w-3.5 text-primary shrink-0" />;
      case "module": return <Folder className="h-3.5 w-3.5 text-blue-500 shrink-0" />;
      default: return <Hash className="h-3.5 w-3.5 text-green-500 shrink-0" />;
    }
  };

  const isHeader = mode === "header";

  return (
    <div className="relative w-full">
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <input
          type="text"
          placeholder="搜索课程..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setTimeout(() => setIsFocused(false), 200)}
          className={`w-full rounded-lg border border-input bg-background text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring ${isHeader ? "h-10 pl-10 pr-10" : "h-12 pl-10 pr-10 text-base"}`}
        />
        {query && (
          <button
            onClick={clearSearch}
            className="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground hover:text-foreground"
          >
            <X className="h-4 w-4" />
          </button>
        )}
      </div>

      {/* Dropdown results */}
      {isFocused && query.length >= 2 && (
        <div className="absolute top-full left-0 right-0 mt-1 bg-background border rounded-lg shadow-lg z-50 max-h-96 overflow-y-auto">
          {loading ? (
            <div className="p-4 text-center text-sm text-muted-foreground animate-pulse">
              搜索中...
            </div>
          ) : results.length > 0 ? (
            results.map((r) => (
              <Link
                key={r.courseId}
                href={`/courses/${r.slug}`}
                className="block p-3 hover:bg-accent border-b last:border-b-0 transition-colors"
                onMouseDown={(e) => e.preventDefault()}
              >
                <div className="flex items-start gap-2">
                  {getMatchIcon(r.matchType)}
                  <div className="min-w-0 flex-1">
                    <p className="text-sm font-medium">{r.title}</p>
                    <p className="text-xs text-muted-foreground truncate">
                      {r.moduleName}
                    </p>
                    {r.matchType === "content" && r.excerpt && (
                      <p className="text-xs text-muted-foreground mt-1 line-clamp-2">
                        {r.excerpt}
                      </p>
                    )}
                  </div>
                </div>
              </Link>
            ))
          ) : (
            <div className="p-4 text-center text-sm text-muted-foreground">
              没有找到匹配的课程
            </div>
          )}
        </div>
      )}
    </div>
  );
}
