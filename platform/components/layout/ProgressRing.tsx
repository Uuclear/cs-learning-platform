"use client";

import { useProgress } from "@/lib/progress";

interface ProgressRingProps {
  totalCourses: number;
  size?: number;
}

export function ProgressRing({ totalCourses, size = 36 }: ProgressRingProps) {
  const { completedCount } = useProgress();
  const percent = totalCourses > 0 ? (completedCount / totalCourses) * 100 : 0;
  const radius = (size - 4) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (percent / 100) * circumference;

  return (
    <div className="relative inline-flex items-center justify-center" title={`${completedCount}/${totalCourses} 已完成 (${Math.round(percent)}%)`}>
      <svg width={size} height={size} className="-rotate-90">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="currentColor"
          strokeWidth={3}
          className="text-muted/30"
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="currentColor"
          strokeWidth={3}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          className="text-green-500 transition-all duration-500"
        />
      </svg>
      <span className="absolute text-[10px] font-medium leading-none">
        {Math.round(percent)}
      </span>
    </div>
  );
}
