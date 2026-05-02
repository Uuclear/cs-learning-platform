"use client";

import { Course } from "@/types/course";
import { Badge } from "@/components/ui/Badge";
import { Card, CardContent } from "@/components/ui/Card";
import { Clock, BarChart3, Calendar, User } from "lucide-react";

interface CourseContentProps {
  course: Course;
  content: React.ReactNode;
}

export function CourseContent({ course, content }: CourseContentProps) {
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
    <div className="max-w-4xl mx-auto">
      {/* Course Header */}
      <div className="mb-8">
        <div className="flex items-center gap-2 mb-4">
          <Badge variant="outline">{course.moduleName}</Badge>
          <Badge className={getDifficultyColor(course.difficulty)}>
            {getDifficultyLabel(course.difficulty)}
          </Badge>
        </div>
        <h1 className="text-3xl md:text-4xl font-bold mb-4">{course.title}</h1>
        <p className="text-lg text-muted-foreground mb-6">
          {course.description}
        </p>

        {/* Course Meta */}
        <Card>
          <CardContent className="p-4">
            <div className="flex flex-wrap gap-6 text-sm">
              <div className="flex items-center gap-2">
                <Clock className="h-4 w-4 text-muted-foreground" />
                <span>{course.durationMinutes}分钟</span>
              </div>
              <div className="flex items-center gap-2">
                <BarChart3 className="h-4 w-4 text-muted-foreground" />
                <span>难度等级 {course.difficulty}/5</span>
              </div>
              <div className="flex items-center gap-2">
                <Calendar className="h-4 w-4 text-muted-foreground" />
                <span>更新于 {course.updatedAt}</span>
              </div>
              <div className="flex items-center gap-2">
                <User className="h-4 w-4 text-muted-foreground" />
                <span>{course.author}</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Course Content */}
      <article className="prose prose-slate max-w-none">
        {content}
      </article>

      {/* Tags */}
      {course.tags.length > 0 && (
        <div className="mt-12 pt-6 border-t">
          <h3 className="text-sm font-semibold text-muted-foreground mb-3">
            相关标签
          </h3>
          <div className="flex flex-wrap gap-2">
            {course.tags.map((tag) => (
              <Badge key={tag} variant="secondary">
                {tag}
              </Badge>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
