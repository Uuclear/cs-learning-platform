"use client";

import { useState, useEffect, useCallback } from "react";

const STORAGE_KEY = "cs-learning-progress";

interface ProgressState {
  completed: string[];  // course IDs
  lastVisited: string | null;
  lastVisitedAt: string | null;
  bookmarked: string[];
  recentlyViewed: Array<{courseId: string, timestamp: number}>;
  quizHistory: Record<string, Array<{score: number, totalQuestions: number, timestamp: number}>>;
}

function loadProgress(): ProgressState {
  if (typeof window === "undefined") {
    return {
      completed: [],
      lastVisited: null,
      lastVisitedAt: null,
      bookmarked: [],
      recentlyViewed: [],
      quizHistory: {}
    };
  }
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return {
      completed: [],
      lastVisited: null,
      lastVisitedAt: null,
      bookmarked: [],
      recentlyViewed: [],
      quizHistory: {}
    };
    const parsed = JSON.parse(raw);
    // Ensure backward compatibility by providing defaults for new fields
    return {
      completed: parsed.completed || [],
      lastVisited: parsed.lastVisited || null,
      lastVisitedAt: parsed.lastVisitedAt || null,
      bookmarked: parsed.bookmarked || [],
      recentlyViewed: parsed.recentlyViewed || [],
      quizHistory: parsed.quizHistory || {}
    };
  } catch {
    return {
      completed: [],
      lastVisited: null,
      lastVisitedAt: null,
      bookmarked: [],
      recentlyViewed: [],
      quizHistory: {}
    };
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

// New utility functions
export function toggleBookmark(courseId: string): void {
  const progress = loadProgress();
  const isCurrentlyBookmarked = progress.bookmarked.includes(courseId);
  const updatedBookmarks = isCurrentlyBookmarked
    ? progress.bookmarked.filter(id => id !== courseId)
    : [...progress.bookmarked, courseId];

  const newState = { ...progress, bookmarked: updatedBookmarks };
  saveProgress(newState);
}

export function isBookmarked(courseId: string): boolean {
  const progress = loadProgress();
  return progress.bookmarked.includes(courseId);
}

export function addRecentlyViewed(courseId: string): void {
  const progress = loadProgress();
  const now = Date.now();

  // Remove existing entry if it exists
  const filtered = progress.recentlyViewed.filter(item => item.courseId !== courseId);
  // Add new entry at the beginning
  const updated = [{ courseId, timestamp: now }, ...filtered];
  // Keep only last 5 entries
  const limited = updated.slice(0, 5);

  const newState = { ...progress, recentlyViewed: limited };
  saveProgress(newState);
}

export function getRecentlyViewed(): Array<{courseId: string, timestamp: number}> {
  const progress = loadProgress();
  // Return sorted by timestamp descending (most recent first)
  return [...progress.recentlyViewed].sort((a, b) => b.timestamp - a.timestamp);
}

export function addQuizHistory(courseId: string, score: number, totalQuestions: number): void {
  const progress = loadProgress();
  const now = Date.now();

  const newEntry = { score, totalQuestions, timestamp: now };
  const existingHistory = progress.quizHistory[courseId] || [];
  const updatedHistory = [...existingHistory, newEntry];

  const newState = {
    ...progress,
    quizHistory: {
      ...progress.quizHistory,
      [courseId]: updatedHistory
    }
  };
  saveProgress(newState);
}

export function getQuizHistory(courseId: string): Array<{score: number, totalQuestions: number, timestamp: number}> {
  const progress = loadProgress();
  return progress.quizHistory[courseId] || [];
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

  const isBookmarked = useCallback(
    (courseId: string) => progress.bookmarked.includes(courseId),
    [progress.bookmarked]
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
    isBookmarked,
    toggleBookmark: () => {
      // Will be called from component level
    },
    progressPercent,
    completedCount: progress.completed.length,
  };
}
