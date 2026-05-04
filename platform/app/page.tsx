import { getAllModules } from "@/lib/courses";
import { Button } from "@/components/ui/Button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card";
import { BookOpen, Code, Lightbulb, ArrowRight, GraduationCap, Trophy, Layers } from "lucide-react";
import Link from "next/link";

export default function Home() {
  const modules = getAllModules();
  const totalCourses = modules.reduce((sum, m) => sum + m.courses.length, 0);
  const totalModules = modules.length;

  return (
    <div className="space-y-16">
      {/* Hero Section with gradient background */}
      <section className="relative text-center space-y-6 py-20 px-4 rounded-2xl overflow-hidden bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-blue-950 dark:via-indigo-950 dark:to-purple-950">
        <div className="absolute inset-0 bg-grid-slate-100 dark:bg-grid-slate-800 [mask-image:linear-gradient(0deg,transparent,black)] pointer-events-none" />
        <div className="relative space-y-6">
          <h1 className="text-4xl md:text-6xl font-bold tracking-tight">
            <span className="text-primary">CS知识</span>学习网站
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
            通俗易懂、幽默风趣的计算机科学学习平台
            <br />
            让复杂的概念变得生动有趣
          </p>
          <div className="flex gap-4 justify-center">
            <Link href="/courses">
              <Button size="lg" className="gap-2 shadow-lg hover:shadow-xl transition-shadow">
                <BookOpen className="w-4 h-4" />
                开始学习
                <ArrowRight className="w-4 h-4" />
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: "课程总数", value: totalCourses, icon: BookOpen },
          { label: "核心模块", value: totalModules, icon: Layers },
          { label: "难度等级", value: 5, icon: GraduationCap },
          { label: "全部完成", value: "✅", icon: Trophy },
        ].map((stat) => (
          <Card key={stat.label} className="text-center hover:shadow-md transition-shadow">
            <CardContent className="pt-6">
              <stat.icon className="w-6 h-6 mx-auto mb-2 text-primary" />
              <p className="text-2xl font-bold">{stat.value}</p>
              <p className="text-sm text-muted-foreground">{stat.label}</p>
            </CardContent>
          </Card>
        ))}
      </section>

      {/* Features Section */}
      <section className="grid md:grid-cols-3 gap-6">
        <Card className="hover:shadow-lg transition-shadow border-t-4 border-t-primary/50">
          <CardHeader>
            <Lightbulb className="w-8 h-8 text-primary mb-2" />
            <CardTitle>通俗易懂</CardTitle>
            <CardDescription>
              用生活化的比喻和类比，让抽象的概念变得具体可感
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              避免学术黑话，用你熟悉的场景解释复杂的计算机原理
            </p>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow border-t-4 border-t-green-500/50">
          <CardHeader>
            <Code className="w-8 h-8 text-green-600 mb-2" />
            <CardTitle>实战代码</CardTitle>
            <CardDescription>
              每节课都配有可运行的代码示例
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              不只是理论，更有动手实践的机会，代码均有中文注释
            </p>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow border-t-4 border-t-purple-500/50">
          <CardHeader>
            <BookOpen className="w-8 h-8 text-purple-600 mb-2" />
            <CardTitle>系统课程</CardTitle>
            <CardDescription>
              从基础到进阶，覆盖{totalModules}大CS核心模块
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              {totalCourses}节精心设计的课程，循序渐进带你掌握计算机科学
            </p>
          </CardContent>
        </Card>
      </section>

      {/* Course Modules Preview */}
      <section className="space-y-6">
        <h2 className="text-3xl font-bold text-center">课程模块</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4">
          {modules.map((module) => (
            <Link key={module.id} href="/courses">
              <div className="p-4 border rounded-lg text-center hover:border-primary hover:shadow-md transition-all cursor-pointer group bg-card">
                <span className="text-xs font-medium text-muted-foreground bg-muted px-2 py-1 rounded-full">
                  模块{module.order}
                </span>
                <p className="font-medium mt-2 group-hover:text-primary transition-colors">
                  {module.name}
                </p>
                <p className="text-xs text-muted-foreground mt-1">
                  {module.courseCount}节课
                </p>
              </div>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}
