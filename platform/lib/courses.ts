import { Course, CourseModule, QuizQuestion } from "@/types/course";
import fs from "fs";
import path from "path";

const COURSES_DIR = path.resolve(process.cwd(), "../courses");

/** Extract description from index.mdx frontmatter if present */
function extractDescriptionFromMDX(indexPath: string): string | null {
  if (!fs.existsSync(indexPath)) return null;
  const content = fs.readFileSync(indexPath, "utf-8");
  const match = content.match(/^---\s*\n([\s\S]*?)\n---/);
  if (!match) return null;
  const frontmatter = match[1];
  const descMatch = frontmatter.match(/description:\s*["'](.+?)["']/);
  return descMatch ? descMatch[1] : null;
}

function normalizeMetadata(filePath: string, metadata: Record<string, unknown>): Course {
  const id = String(metadata.id ?? "");
  const title = String(metadata.title ?? "");
  const lessonDirName = path.basename(path.dirname(filePath));
  const slugFromMetadata = metadata.slug;
  let slug: string;
  if (slugFromMetadata) {
    slug = String(slugFromMetadata);
  } else {
    const slugParts = lessonDirName.split("-");
    slug = slugParts.length > 2 ? slugParts.slice(2).join("-") : id.toLowerCase();
  }

  const module = String(metadata.module ?? "");
  const moduleName = String(metadata.module_name ?? "");

  // Try to get description from index.mdx frontmatter
  const indexPath = path.join(path.dirname(filePath), "index.mdx");
  let description = String(metadata.description ?? "");
  if (!description) {
    const mdxDesc = extractDescriptionFromMDX(indexPath);
    if (mdxDesc) {
      description = mdxDesc;
    } else {
      description = title || lessonDirName.replace(/-/g, " ");
    }
  }

  const difficulty = Math.min(5, Math.max(1, Number(metadata.difficulty ?? 1))) as Course["difficulty"];
  const durationMinutes = Number(metadata.duration ?? 30);
  const prerequisites = Array.isArray(metadata.prerequisites)
    ? metadata.prerequisites.map(String)
    : [];
  const tags = Array.isArray(metadata.tags)
    ? metadata.tags.map(String)
    : [module];
  const author = String(metadata.author ?? "CS教授");

  const moduleOrder = parseInt(module.split("-")[0], 10) || 0;
  const idParts = id.split("-");
  const lessonOrder = parseInt(idParts.length >= 2 ? idParts[1] : "0", 10) || 0;

  return {
    id,
    title,
    slug,
    description,
    module,
    moduleName,
    moduleOrder,
    lessonOrder,
    difficulty,
    durationMinutes,
    prerequisites,
    tags,
    author,
    createdAt: String(metadata.created ?? metadata.created_at ?? "2026-05-03"),
    updatedAt: String(metadata.updated ?? metadata.updated_at ?? "2026-05-03"),
    status: "published",
  };
}

function loadCourseMetadata(filePath: string): Course {
  const raw = fs.readFileSync(filePath, "utf-8");
  const metadata = JSON.parse(raw) as Record<string, unknown>;
  return normalizeMetadata(filePath, metadata);
}

let _allCourses: Course[] | null = null;
let _allModules: CourseModule[] | null = null;

function getAllCoursesInternal(): Course[] {
  if (_allCourses) return _allCourses;

  if (!fs.existsSync(COURSES_DIR)) {
    return [];
  }

  const courses: Course[] = [];
  const moduleDirs = fs
    .readdirSync(COURSES_DIR, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => d.name)
    .sort();

  for (const moduleDir of moduleDirs) {
    const modulePath = path.join(COURSES_DIR, moduleDir);
    let moduleMetadata: Record<string, unknown> | null = null;

    // Try to read a module-level metadata file
    const moduleMetaPath = path.join(modulePath, "module.json");
    if (fs.existsSync(moduleMetaPath)) {
      moduleMetadata = JSON.parse(fs.readFileSync(moduleMetaPath, "utf-8"));
    }

    const lessonDirs = fs
      .readdirSync(modulePath, { withFileTypes: true })
      .filter((d) => d.isDirectory())
      .map((d) => d.name)
      .sort();

    for (const lessonDir of lessonDirs) {
      const metaPath = path.join(modulePath, lessonDir, "metadata.json");
      if (fs.existsSync(metaPath)) {
        try {
          const course = loadCourseMetadata(metaPath);
          // Fill in missing module name from directory name
          if (!course.moduleName && moduleMetadata) {
            course.moduleName = String(moduleMetadata.name ?? course.module);
          }
          if (!course.moduleName) {
            const dirParts = moduleDir.split("-");
            course.moduleName = dirParts.slice(1).join(" ") || moduleDir;
          }
          courses.push(course);
        } catch {
          // Skip malformed metadata
        }
      }
    }
  }

  _allCourses = courses;
  return courses;
}

function getAllModulesInternal(): CourseModule[] {
  if (_allModules) return _allModules;

  const courses = getAllCoursesInternal();
  const moduleMap = new Map<string, CourseModule>();

  // Group courses by module
  for (const course of courses) {
    if (!moduleMap.has(course.module)) {
      moduleMap.set(course.module, {
        id: course.module,
        name: course.moduleName,
        description: `${course.moduleName}课程模块`,
        order: course.moduleOrder,
        courseCount: 0,
        courses: [],
      });
    }
    const mod = moduleMap.get(course.module)!;
    mod.courses.push(course);
  }

  // Sort courses within each module and count
  const modules = Array.from(moduleMap.values()).map((mod) => ({
    ...mod,
    courses: mod.courses.sort((a, b) => a.lessonOrder - b.lessonOrder),
    courseCount: mod.courses.length,
  }));

  modules.sort((a, b) => a.order - b.order);
  _allModules = modules;
  return modules;
}

export function getCourseBySlug(slug: string): Course | undefined {
  return getAllCoursesInternal().find((c) => c.slug === slug);
}

export function getCoursesByModule(moduleId: string): Course[] {
  return getAllCoursesInternal().filter((c) => c.module === moduleId);
}

export function getAllCourses(): Course[] {
  return getAllCoursesInternal();
}

export function getAllModules(): CourseModule[] {
  return getAllModulesInternal();
}

export function getPublishedCourses(): Course[] {
  return getAllCoursesInternal().filter((c) => c.status === "published");
}

/** Get the filesystem path to a course directory */
export function findCourseDirBySlug(slug: string): string | null {
  if (!fs.existsSync(COURSES_DIR)) return null;

  for (const moduleDir of fs.readdirSync(COURSES_DIR, { withFileTypes: true }).filter(d => d.isDirectory())) {
    const modulePath = path.join(COURSES_DIR, moduleDir.name);
    for (const lessonDir of fs.readdirSync(modulePath, { withFileTypes: true }).filter(d => d.isDirectory())) {
      const dirName = lessonDir.name;
      const parts = dirName.split("-");
      const dirSlug = parts.length > 2 ? parts.slice(2).join("-") : dirName;
      if (dirSlug === slug) {
        return path.join(modulePath, dirName);
      }
    }
  }
  return null;
}

/** Read the full MDX content of a course */
export function readCourseMDX(course: Course): string {
  const dir = findCourseDirBySlug(course.slug);
  if (!dir) return "";
  const indexPath = path.join(dir, "index.mdx");
  if (!fs.existsSync(indexPath)) return "";
  return fs.readFileSync(indexPath, "utf-8");
}

/** Read quiz questions for a course */
export function readCourseQuiz(course: Course): QuizQuestion[] {
  const dir = findCourseDirBySlug(course.slug);
  if (!dir) return [];
  const quizPath = path.join(dir, "exercises", "quiz.json");
  if (!fs.existsSync(quizPath)) return [];
  try {
    const raw = fs.readFileSync(quizPath, "utf-8");
    return JSON.parse(raw) as QuizQuestion[];
  } catch {
    return [];
  }
}
