"use client";

import { useState, useMemo, useCallback } from "react";
import { Course } from "@/types/course";
import { Search, X, BookOpen } from "lucide-react";
import Link from "next/link";
import { Badge } from "@/components/ui/Badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";

interface SearchBarProps {
  courses: Course[];
}

export function SearchBar({ courses }: SearchBarProps) {
  const [query, setQuery] = useState("");
  const [isFocused, setIsFocused] = useState(false);

  const results = useMemo(() => {
    if (query.length < 2) return [];
    const q = query.toLowerCase();
    return courses
      .filter((c) => {
        return (
          c.title.toLowerCase().includes(q) ||
          c.description.toLowerCase().includes(q) ||
          c.moduleName.toLowerCase().includes(q) ||
          c.tags.some((t) => t.toLowerCase().includes(q))
        );
      })
      .slice(0, 10);
  }, [query, courses]);

  const clearSearch = () => setQuery("");

  return (
    <div className="relative w-full max-w-md">
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <input
          type="text"
          placeholder="搜索课程..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setTimeout(() => setIsFocused(false), 200)}
          className="w-full h-10 pl-10 pr-10 rounded-lg border border-input bg-background text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
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
          {results.length > 0 ? (
            results.map((course) => (
              <Link
                key={course.id}
                href={`/courses/${course.slug}`}
                className="block p-3 hover:bg-accent border-b last:border-b-0 transition-colors"
              >
                <div className="flex items-start gap-2">
                  <BookOpen className="h-4 w-4 mt-0.5 text-primary shrink-0" />
                  <div className="min-w-0">
                    <p className="text-sm font-medium truncate">{course.title}</p>
                    <p className="text-xs text-muted-foreground truncate">
                      {course.moduleName}
                    </p>
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

/** Filter courses by query string on the courses page */
export function filterCourses(courses: Course[], query: string): Course[] {
  if (!query || query.length < 2) return courses;
  const q = query.toLowerCase();
  return courses.filter(
    (c) =>
      c.title.toLowerCase().includes(q) ||
      c.description.toLowerCase().includes(q) ||
      c.moduleName.toLowerCase().includes(q) ||
      c.tags.some((t) => t.toLowerCase().includes(q))
  );
}
