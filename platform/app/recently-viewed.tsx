"use client";

import Link from "next/link";
import { Clock } from "lucide-react";
import { useEffect, useState } from "react";
import { getAllCourses } from "@/lib/courses";
import { getRecentlyViewed } from "@/lib/progress";

interface CourseInfo {
  id: string;
  title: string;
  slug: string;
  moduleName: string;
}

export function RecentlyViewedSection() {
  const [recent, setRecent] = useState<CourseInfo[]>([]);

  useEffect(() => {
    const allCourses = getAllCourses();
    const recentlyViewed = getRecentlyViewed();
    const viewed: CourseInfo[] = recentlyViewed
      .map((rv: { courseId: string; timestamp: number }) => {
        const course = allCourses.find(c => c.id === rv.courseId);
        if (!course) return null;
        return {
          id: course.id,
          title: course.title,
          slug: course.slug,
          moduleName: course.moduleName,
        };
      })
      .filter(Boolean) as CourseInfo[];
    setRecent(viewed.slice(0, 5));
  }, []);

  if (recent.length === 0) return null;

  return (
    <section className="space-y-4">
      <h2 className="text-2xl font-bold flex items-center gap-2">
        <Clock className="h-5 w-5 text-muted-foreground" />
        最近浏览
      </h2>
      <div className="grid sm:grid-cols-2 lg:grid-cols-5 gap-3">
        {recent.map((course) => (
          <Link key={course.id} href={`/courses/${course.slug}`}>
            <div className="p-3 border rounded-lg hover:border-primary hover:shadow-md transition-all cursor-pointer group bg-card">
              <p className="text-sm font-medium group-hover:text-primary transition-colors truncate">
                {course.title}
              </p>
              <p className="text-xs text-muted-foreground mt-1">{course.moduleName}</p>
            </div>
          </Link>
        ))}
      </div>
    </section>
  );
}
