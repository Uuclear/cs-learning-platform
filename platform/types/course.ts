export interface Course {
  id: string;
  title: string;
  slug: string;
  description: string;
  module: string;
  moduleName: string;
  moduleOrder: number;
  lessonOrder: number;
  difficulty: 1 | 2 | 3 | 4 | 5;
  durationMinutes: number;
  prerequisites: string[];
  tags: string[];
  author: string;
  createdAt: string;
  updatedAt: string;
  status: "draft" | "published" | "completed";
}

export interface CourseModule {
  id: string;
  name: string;
  description: string;
  order: number;
  courseCount: number;
  courses: Course[];
}

export interface CourseContent {
  course: Course;
  content: string;
  codeExamples: CodeExample[];
  exercises: Exercise[];
}

export interface CodeExample {
  id: string;
  title: string;
  language: string;
  code: string;
  explanation?: string;
}

export interface Exercise {
  id: string;
  type: "quiz" | "challenge";
  title: string;
  description: string;
  difficulty: 1 | 2 | 3;
}

export interface QuizQuestion {
  id: number;
  question: string;
  options: string[];
  correct: number;
  explanation: string;
}

export interface Quiz {
  questions: QuizQuestion[];
}
