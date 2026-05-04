'use client';

import { ChevronLeft, ChevronRight } from 'lucide-react';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

interface Course {
  slug: string;
  module: string;
  moduleOrder: number;
  lessonOrder: number;
  title: string;
}

interface LessonNavigationProps {
  currentModuleOrder: number;
  currentLessonOrder: number;
  currentModule: string;
  currentSlug: string;
  allCourses: Course[];
}

export default function LessonNavigation({
  currentModuleOrder,
  currentLessonOrder,
  currentModule,
  currentSlug,
  allCourses,
}: LessonNavigationProps) {
  const router = useRouter();

  // Find previous and next lessons
  const currentCourseIndex = allCourses.findIndex(
    course => course.slug === currentSlug && course.module === currentModule
  );

  const previousCourse = currentCourseIndex > 0 ? allCourses[currentCourseIndex - 1] : null;
  const nextCourse = currentCourseIndex < allCourses.length - 1 ? allCourses[currentCourseIndex + 1] : null;

  // Check if we're at the beginning or end of the current module
  const isFirstInModule = !previousCourse || previousCourse.moduleOrder !== currentModuleOrder;
  const isLastInModule = !nextCourse || nextCourse.moduleOrder !== currentModuleOrder;

  const handlePrevious = () => {
    if (previousCourse && !isFirstInModule) {
      router.push(`/courses/${previousCourse.module}-${previousCourse.slug}`);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const handleNext = () => {
    if (nextCourse && !isLastInModule) {
      router.push(`/courses/${nextCourse.module}-${nextCourse.slug}`);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'ArrowLeft' && previousCourse && !isFirstInModule) {
        handlePrevious();
      } else if (event.key === 'ArrowRight' && nextCourse && !isLastInModule) {
        handleNext();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [previousCourse, nextCourse, isFirstInModule, isLastInModule]);

  return (
    <div className="flex justify-between items-center mt-8 mb-4">
      <button
        onClick={handlePrevious}
        disabled={!previousCourse || isFirstInModule}
        className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all ${
          !previousCourse || isFirstInModule
            ? 'opacity-50 cursor-not-allowed'
            : 'hover:bg-gray-100 hover:dark:bg-gray-800'
        }`}
      >
        <ChevronLeft className="w-4 h-4" />
        <span>← 上一课</span>
      </button>

      <button
        onClick={handleNext}
        disabled={!nextCourse || isLastInModule}
        className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all ${
          !nextCourse || isLastInModule
            ? 'opacity-50 cursor-not-allowed'
            : 'hover:bg-gray-100 hover:dark:bg-gray-800'
        }`}
      >
        <span>下一课 →</span>
        <ChevronRight className="w-4 h-4" />
      </button>
    </div>
  );
}