import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { getAllCourses } from "@/lib/courses";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "CS知识学习网站 - 通俗易懂学计算机",
  description: "一个通俗易懂、幽默风趣的CS知识学习平台，让复杂的计算机科学概念变得生动有趣",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const courses = getAllCourses();

  return (
    <html lang="zh-CN">
      <body className={inter.className}>
        <div className="min-h-screen bg-background flex flex-col">
          <Header courses={courses} />
          <main className="flex-1 flex flex-col">
            <div className="container mx-auto px-4 py-6">
              {children}
            </div>
          </main>
          <Footer />
        </div>
      </body>
    </html>
  );
}
