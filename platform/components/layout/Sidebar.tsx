"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { useProgress } from "@/lib/progress";
import { Course, CourseModule } from "@/types/course";
import { BookOpen, ChevronDown, ChevronRight, CheckCircle2 } from "lucide-react";
import { useState } from "react";

interface SidebarProps {
  modules: CourseModule[];
  currentCourse?: Course;
}

export function Sidebar({ modules, currentCourse }: SidebarProps) {
  const pathname = usePathname();
  const { isCompleted } = useProgress();
  const [expandedModules, setExpandedModules] = useState<string[]>(() => {
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
          课程导航
        </h2>
        <nav className="space-y-2">
          {modules.map((module) => {
            const isExpanded = expandedModules.includes(module.id);
            const completedCount = module.courses.filter((c) => isCompleted(c.id)).length;

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
                  {module.courses.length > 0 ? (
                    isExpanded ? (
                      <ChevronDown className="h-4 w-4 mr-1 shrink-0" />
                    ) : (
                      <ChevronRight className="h-4 w-4 mr-1 shrink-0" />
                    )
                  ) : (
                    <span className="w-4 mr-1" />
                  )}
                  <span className="flex-1 truncate">{module.name}</span>
                  {completedCount > 0 && (
                    <span className="text-xs text-green-600 mr-1">{completedCount}</span>
                  )}
                </button>

                {isExpanded && module.courses.length > 0 && (
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
                        {isCompleted(course.id) ? (
                          <CheckCircle2 className="h-3 w-3 mr-2 shrink-0 text-green-600" />
                        ) : (
                          <BookOpen className="h-3 w-3 mr-2 shrink-0" />
                        )}
                        <span className="truncate">{course.title.split("：")[0]}</span>
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
