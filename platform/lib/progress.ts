"use client";

import { useState, useEffect, useCallback } from "react";

const STORAGE_KEY = "cs-learning-progress";

interface ProgressState {
  completed: string[];  // course IDs
  lastVisited: string | null;
  lastVisitedAt: string | null;
}

function loadProgress(): ProgressState {
  if (typeof window === "undefined") {
    return { completed: [], lastVisited: null, lastVisitedAt: null };
  }
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { completed: [], lastVisited: null, lastVisitedAt: null };
    return JSON.parse(raw);
  } catch {
    return { completed: [], lastVisited: null, lastVisitedAt: null };
  }
}

function saveProgress(state: ProgressState) {
  if (typeof window === "undefined") return;
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch {
    // localStorage full or disabled
  }
}

export function useProgress() {
  const [progress, setProgress] = useState<ProgressState>(loadProgress);

  // Sync across tabs
  useEffect(() => {
    const handler = (e: StorageEvent) => {
      if (e.key === STORAGE_KEY && e.newValue) {
        setProgress(JSON.parse(e.newValue));
      }
    };
    window.addEventListener("storage", handler);
    return () => window.removeEventListener("storage", handler);
  }, []);

  const markComplete = useCallback((courseId: string) => {
    setProgress((prev) => {
      const next = {
        ...prev,
        completed: prev.completed.includes(courseId)
          ? prev.completed
          : [...prev.completed, courseId],
        lastVisited: courseId,
        lastVisitedAt: new Date().toISOString(),
      };
      saveProgress(next);
      return next;
    });
  }, []);

  const markIncomplete = useCallback((courseId: string) => {
    setProgress((prev) => {
      const next = {
        ...prev,
        completed: prev.completed.filter((id) => id !== courseId),
      };
      saveProgress(next);
      return next;
    });
  }, []);

  const isCompleted = useCallback(
    (courseId: string) => progress.completed.includes(courseId),
    [progress.completed]
  );

  const progressPercent = useCallback(
    (total: number) =>
      total > 0 ? Math.round((progress.completed.length / total) * 100) : 0,
    [progress.completed.length]
  );

  return {
    progress,
    markComplete,
    markIncomplete,
    isCompleted,
    progressPercent,
    completedCount: progress.completed.length,
  };
}
