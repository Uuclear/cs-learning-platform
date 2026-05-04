"use client";

import { useState } from "react";
import { Course, CourseModule } from "@/types/course";
import { useProgress } from "@/lib/progress";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { BookOpen, Clock, BarChart3, ArrowRight, Search, CheckCircle2 } from "lucide-react";
import Link from "next/link";

interface CoursesClientProps {
  modules: CourseModule[];
}

export function CoursesClient({ modules }: CoursesClientProps) {
  const [filter, setFilter] = useState("");
  const [activeModule, setActiveModule] = useState<string | null>(null);
  const { isCompleted, completedCount, progressPercent } = useProgress();

  const totalCourses = modules.reduce((sum, m) => sum + m.courses.length, 0);
  const totalModules = modules.length;

  const getDifficultyLabel = (level: number) => {
    const labels = ["入门", "简单", "中等", "困难", "专家"];
    return labels[level - 1] || "未知";
  };

  const getDifficultyColor = (level: number) => {
    const colors = [
      "bg-green-100 text-green-800",
      "bg-blue-100 text-blue-800",
      "bg-yellow-100 text-yellow-800",
      "bg-orange-100 text-orange-800",
      "bg-red-100 text-red-800",
    ];
    return colors[level - 1] || "bg-gray-100 text-gray-800";
  };

  const filteredModules = modules
    .map((mod) => {
      const courses = mod.courses.filter((c) => {
        const q = filter.toLowerCase();
        const matchesFilter = !filter ||
          c.title.toLowerCase().includes(q) ||
          c.description.toLowerCase().includes(q) ||
          c.moduleName.toLowerCase().includes(q) ||
          c.tags.some((t) => t.toLowerCase().includes(q));
        const matchesModule = !activeModule || mod.id === activeModule;
        return matchesFilter && matchesModule;
      });
      return { ...mod, courses };
    })
    .filter((mod) => mod.courses.length > 0 || !activeModule);

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Page Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">全部课程</h1>
        <p className="text-muted-foreground mb-4">
          {totalModules}个模块，{totalCourses}门课程，从基础到进阶，系统学习计算机科学知识
        </p>

        {/* Search and Filter Bar */}
        <div className="flex flex-col gap-4 mb-6">
          <div className="flex flex-col sm:flex-row gap-3">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <input
                type="text"
                placeholder="在课程中搜索..."
                value={filter}
                onChange={(e) => setFilter(e.target.value)}
                className="w-full h-10 pl-10 pr-4 rounded-lg border border-input bg-background text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
              />
            </div>
            {/* Progress indicator */}
            <div className="flex items-center gap-2 px-4 py-2 bg-muted rounded-lg self-center">
              <CheckCircle2 className="h-4 w-4 text-green-600" />
              <span className="text-sm font-medium">{completedCount}/{totalCourses}</span>
              <span className="text-sm text-muted-foreground">({progressPercent(totalCourses)}%)</span>
            </div>
          </div>
          <div className="flex gap-2 flex-wrap">
            <Button
              variant={!activeModule ? "default" : "outline"}
              size="sm"
              onClick={() => setActiveModule(null)}
            >
              全部
            </Button>
            {modules.map((mod) => (
              <Button
                key={mod.id}
                variant={activeModule === mod.id ? "default" : "outline"}
                size="sm"
                onClick={() => setActiveModule(activeModule === mod.id ? null : mod.id)}
                className="whitespace-nowrap"
              >
                {mod.name}
              </Button>
            ))}
          </div>
        </div>
      </div>

      {/* Modules and Courses */}
      <div className="space-y-8">
        {filteredModules.map((module) => (
          <section key={module.id}>
            <div className="mb-4 flex items-baseline gap-3">
              <h2 className="text-xl font-semibold">{module.name}</h2>
              <Badge variant="secondary" className="text-xs">{module.courses.length}节</Badge>
              <span className="text-sm text-muted-foreground">{module.description}</span>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              {module.courses.map((course) => (
                <Card key={course.id} className={`flex flex-col ${isCompleted(course.id) ? "border-green-300 bg-green-50/50 dark:bg-green-950/20" : ""}`}>
                  <CardHeader className="pb-3">
                    <div className="flex items-start justify-between gap-2">
                      <CardTitle className="text-lg leading-tight">
                        <span className="flex items-center gap-2">
                          {course.title}
                          {isCompleted(course.id) && (
                            <CheckCircle2 className="w-4 h-4 text-green-600 shrink-0" />
                          )}
                        </span>
                      </CardTitle>
                      <Badge
                        variant="secondary"
                        className={getDifficultyColor(course.difficulty)}
                      >
                        {getDifficultyLabel(course.difficulty)}
                      </Badge>
                    </div>
                    <CardDescription className="line-clamp-2">
                      {course.description}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="flex-1 flex flex-col justify-end pt-0">
                    <div className="flex items-center gap-4 text-sm text-muted-foreground mb-4">
                      <div className="flex items-center gap-1">
                        <Clock className="h-4 w-4" />
                        <span>{course.durationMinutes}分钟</span>
                      </div>
                      <div className="flex items-center gap-1">
                        <BarChart3 className="h-4 w-4" />
                        <span>第{course.lessonOrder}课</span>
                      </div>
                    </div>
                    <Link href={`/courses/${course.slug}`}>
                      <Button
                        variant="default"
                        size="sm"
                        className="w-full gap-2"
                      >
                        <BookOpen className="h-4 w-4" />
                        开始学习
                        <ArrowRight className="h-4 w-4" />
                      </Button>
                    </Link>
                  </CardContent>
                </Card>
              ))}
            </div>
          </section>
        ))}

        {filteredModules.length === 0 && (
          <div className="text-center py-12 text-muted-foreground">
            <BookOpen className="h-12 w-12 mx-auto mb-3 opacity-30" />
            <p className="text-lg">没有找到匹配的课程</p>
            <p className="text-sm mt-1">尝试调整搜索关键词</p>
            <Button variant="outline" className="mt-4" onClick={() => { setFilter(""); setActiveModule(null); }}>
              清除筛选
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}
