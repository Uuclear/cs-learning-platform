"use client";

import { useProgress } from "@/lib/progress";
import { Button } from "@/components/ui/Button";
import { CheckCircle2, Circle } from "lucide-react";

interface CourseCompleteButtonProps {
  courseId: string;
  courseTitle: string;
}

export function CourseCompleteButton({ courseId, courseTitle }: CourseCompleteButtonProps) {
  const { isCompleted, markComplete, markIncomplete, completedCount } = useProgress();
  const completed = isCompleted(courseId);

  return (
    <Button
      variant={completed ? "outline" : "default"}
      size="sm"
      className="gap-2"
      onClick={() => {
        if (completed) {
          markIncomplete(courseId);
        } else {
          markComplete(courseId);
        }
      }}
    >
      {completed ? (
        <>
          <CheckCircle2 className="w-4 h-4 text-green-600" />
          已完成 ({completedCount}门)
        </>
      ) : (
        <>
          <Circle className="w-4 h-4" />
          标记为完成
        </>
      )}
    </Button>
  );
}
