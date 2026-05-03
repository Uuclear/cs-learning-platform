import { getAllModules } from "@/lib/courses";
import { CoursesClient } from "./client";

export default function CoursesPage() {
  const modules = getAllModules();

  return <CoursesClient modules={modules} />;
}
