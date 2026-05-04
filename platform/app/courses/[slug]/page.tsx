import { notFound } from "next/navigation";
import { getCourseBySlug, getAllModules, getAllCourses, readCourseMDX, readCourseQuiz } from "@/lib/courses";
import { CourseContent } from "@/components/course/CourseContent";
import { Sidebar } from "@/components/layout/Sidebar";
import { QuizClient } from "@/components/course/QuizClient";
import ReadingProgress from "@/components/course/ReadingProgress";
import LessonNavigation from "@/components/course/LessonNavigation";
import { renderMDXContent } from "@/lib/mdx-renderer";

interface CoursePageProps {
  params: {
    slug: string;
  };
}

export function generateStaticParams() {
  const courses = getAllCourses();
  return courses.map((course: any) => ({ slug: course.slug }));
}

export default function CoursePage({ params }: CoursePageProps) {
  const course = getCourseBySlug(params.slug);
  const modules = getAllModules();
  const allCourses = getAllCourses();

  if (!course) {
    notFound();
  }

  const mdxContent = readCourseMDX(course);
  const quiz = readCourseQuiz(course);
  const contentHtml = renderMDXContent(mdxContent);

  return (
    <div className="flex min-h-[calc(100vh-3.5rem)]">
      <Sidebar modules={modules} currentCourse={course} />
      <div className="flex-1 overflow-y-auto">
        <ReadingProgress />
        <div className="p-8">
          <CourseContent course={course} contentHtml={contentHtml} />
          {quiz.length > 0 && (
            <div className="max-w-4xl mx-auto mt-12">
              <QuizClient questions={quiz} courseId={course.id} />
            </div>
          )}
          <div className="max-w-4xl mx-auto">
            <LessonNavigation
              currentModuleOrder={course.moduleOrder}
              currentLessonOrder={course.lessonOrder}
              currentModule={course.module}
              currentSlug={course.slug}
              allCourses={allCourses}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
