"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { useProgress } from "@/lib/progress";
import { Course, CourseModule } from "@/types/course";
import { BookOpen, ChevronDown, ChevronRight, CheckCircle2, X } from "lucide-react";
import { useState, useEffect } from "react";

interface SidebarProps {
  modules: CourseModule[];
  currentCourse?: Course;
}

function SidebarContent({ modules, currentCourse, onClose }: SidebarProps & { onClose?: () => void }) {
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

  const handleLinkClick = () => {
    onClose?.();
  };

  return (
    <div className="p-4">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider">
          课程导航
        </h2>
        {onClose && (
          <button
            onClick={onClose}
            className="p-1 rounded-md hover:bg-accent md:hidden"
            aria-label="关闭导航"
          >
            <X className="h-4 w-4" />
          </button>
        )}
      </div>
      <nav className="space-y-2">
        {modules.map((module) => {
          const isExpanded = expandedModules.includes(module.id);
          const completedCount = module.courses.filter((c) => isCompleted(c.id)).length;

          return (
            <div key={module.id} className="space-y-1">
              <button
                onClick={() => toggleModule(module.id)}
                className={cn(
                  "flex items-center w-full text-left text-sm font-medium rounded-md px-3 py-2 min-h-[44px] transition-colors",
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
                      onClick={handleLinkClick}
                      className={cn(
                        "flex items-center text-sm rounded-md px-3 py-2 min-h-[44px] transition-colors",
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
  );
}

export function Sidebar({ modules, currentCourse }: SidebarProps) {
  const [mobileOpen, setMobileOpen] = useState(false);

  // Close on Escape key
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") setMobileOpen(false);
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  return (
    <>
      {/* Mobile toggle button */}
      <button
        onClick={() => setMobileOpen(true)}
        className="fixed bottom-4 left-4 z-40 md:hidden p-3 rounded-full bg-primary text-primary-foreground shadow-lg min-h-[44px] min-w-[44px] flex items-center justify-center"
        aria-label="打开导航"
      >
        <BookOpen className="h-5 w-5" />
      </button>

      {/* Desktop sidebar */}
      <aside className="hidden md:block w-64 border-r bg-background h-[calc(100vh-3.5rem)] sticky top-14 overflow-y-auto">
        <SidebarContent modules={modules} currentCourse={currentCourse} />
      </aside>

      {/* Mobile drawer */}
      {mobileOpen && (
        <>
          <div
            className="fixed inset-0 z-40 bg-black/50 md:hidden"
            onClick={() => setMobileOpen(false)}
          />
          <aside className="fixed top-0 left-0 z-50 w-72 max-w-[85vw] h-full bg-background border-r overflow-y-auto md:hidden animate-in slide-in-from-left duration-200">
            <SidebarContent
              modules={modules}
              currentCourse={currentCourse}
              onClose={() => setMobileOpen(false)}
            />
          </aside>
        </>
      )}
    </>
  );
}
