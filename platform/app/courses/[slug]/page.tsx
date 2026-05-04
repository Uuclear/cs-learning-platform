import { notFound } from "next/navigation";
import { getCourseBySlug, getAllModules, readCourseMDX, readCourseQuiz } from "@/lib/courses";
import { CourseContent } from "@/components/course/CourseContent";
import { Sidebar } from "@/components/layout/Sidebar";
import { QuizClient } from "@/components/course/QuizClient";
import { renderMDXContent } from "@/lib/mdx-renderer";

interface CoursePageProps {
  params: {
    slug: string;
  };
}

export function generateStaticParams() {
  const { getAllCourses } = require("@/lib/courses");
  const courses = getAllCourses();
  return courses.map((course: any) => ({ slug: course.slug }));
}

export default function CoursePage({ params }: CoursePageProps) {
  const course = getCourseBySlug(params.slug);
  const modules = getAllModules();

  if (!course) {
    notFound();
  }

  const mdxContent = readCourseMDX(course);
  const quiz = readCourseQuiz(course);
  const contentHtml = renderMDXContent(mdxContent);

  return (
    <div className="flex min-h-[calc(100vh-3.5rem)]">
      <Sidebar modules={modules} currentCourse={course} />
      <div className="flex-1 p-8 overflow-y-auto">
        <CourseContent course={course} contentHtml={contentHtml} />
        {quiz.length > 0 && (
          <div className="max-w-4xl mx-auto mt-12">
            <QuizClient questions={quiz} courseId={course.id} />
          </div>
        )}
      </div>
    </div>
  );
}
