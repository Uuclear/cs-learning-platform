"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { Course, CourseModule } from "@/types/course";
import { BookOpen, ChevronDown, ChevronRight } from "lucide-react";
import { useState } from "react";

interface SidebarProps {
  modules: CourseModule[];
  currentCourse?: Course;
}

export function Sidebar({ modules, currentCourse }: SidebarProps) {
  const pathname = usePathname();
  const [expandedModules, setExpandedModules] = useState<string[]>(() => {
    // 默认展开当前课程所在模块
    if (currentCourse) {
      return [currentCourse.module];
    }
    return [];
  });

  const toggleModule = (moduleId: string) => {
    setExpandedModules((prev) =>
      prev.includes(moduleId)
        ? prev.filter((id) => id !== moduleId)
        : [...prev, moduleId]
    );
  };

  return (
    <aside className="w-64 border-r bg-background h-[calc(100vh-3.5rem)] sticky top-14 overflow-y-auto">
      <div className="p-4">
        <h2 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider mb-4">
          课程模块
        </h2>
        <nav className="space-y-2">
          {modules.map((module) => {
            const isExpanded = expandedModules.includes(module.id);
            const hasCourses = module.courses.length > 0;

            return (
              <div key={module.id} className="space-y-1">
                <button
                  onClick={() => toggleModule(module.id)}
                  className={cn(
                    "flex items-center w-full text-left text-sm font-medium rounded-md px-3 py-2 transition-colors",
                    "hover:bg-accent hover:text-accent-foreground",
                    currentCourse?.module === module.id && "bg-accent"
                  )}
                >
                  {hasCourses ? (
                    isExpanded ? (
                      <ChevronDown className="h-4 w-4 mr-1 shrink-0" />
                    ) : (
                      <ChevronRight className="h-4 w-4 mr-1 shrink-0" />
                    )
                  ) : (
                    <span className="w-4 mr-1" />
                  )}
                  <span className="flex-1">{module.name}</span>
                  <span className="text-xs text-muted-foreground">
                    {module.courseCount}节
                  </span>
                </button>

                {isExpanded && hasCourses && (
                  <div className="ml-4 space-y-1">
                    {module.courses.map((course) => (
                      <Link
                        key={course.id}
                        href={`/courses/${course.slug}`}
                        className={cn(
                          "flex items-center text-sm rounded-md px-3 py-2 transition-colors",
                          "hover:bg-accent hover:text-accent-foreground",
                          currentCourse?.id === course.id
                            ? "bg-primary/10 text-primary font-medium"
                            : "text-muted-foreground"
                        )}
                      >
                        <BookOpen className="h-3 w-3 mr-2 shrink-0" />
                        <span className="truncate">{course.title}</span>
                      </Link>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </nav>
      </div>
    </aside>
  );
}
