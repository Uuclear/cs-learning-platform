import { getAllModules } from "@/lib/courses";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { BookOpen, Clock, BarChart3, ArrowRight } from "lucide-react";
import Link from "next/link";

export default function CoursesPage() {
  const modules = getAllModules();

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

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Page Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">全部课程</h1>
        <p className="text-muted-foreground">
          从基础到进阶，系统学习计算机科学知识
        </p>
      </div>

      {/* Modules and Courses */}
      <div className="space-y-8">
        {modules.map((module) => (
          <section key={module.id}>
            <div className="mb-4">
              <h2 className="text-xl font-semibold">{module.name}</h2>
              <p className="text-sm text-muted-foreground">{module.description}</p>
            </div>

            {module.courses.length > 0 ? (
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                {module.courses.map((course) => (
                  <Card key={course.id} className="flex flex-col">
                    <CardHeader className="pb-3">
                      <div className="flex items-start justify-between gap-2">
                        <CardTitle className="text-lg leading-tight">
                          {course.title}
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
                          variant={course.status === "published" ? "default" : "outline"}
                          size="sm"
                          className="w-full gap-2"
                          disabled={course.status !== "published"}
                        >
                          <BookOpen className="h-4 w-4" />
                          {course.status === "published" ? "开始学习" : "即将上线"}
                          {course.status === "published" && (
                            <ArrowRight className="h-4 w-4" />
                          )}
                        </Button>
                      </Link>
                    </CardContent>
                  </Card>
                ))}
              </div>
            ) : (
              <div className="border rounded-lg p-8 text-center text-muted-foreground bg-muted/50">
                <BookOpen className="h-8 w-8 mx-auto mb-2 opacity-50" />
                <p>该模块课程正在开发中，敬请期待...</p>
              </div>
            )}
          </section>
        ))}
      </div>
    </div>
  );
}
