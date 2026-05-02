import { Button } from "@/components/ui/Button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card";
import { BookOpen, Code, Lightbulb, ArrowRight } from "lucide-react";
import Link from "next/link";

export default function Home() {
  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <section className="text-center space-y-6 py-12">
        <h1 className="text-4xl md:text-6xl font-bold tracking-tight">
          <span className="text-primary">CS知识</span>学习网站
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          通俗易懂、幽默风趣的计算机科学学习平台
          <br />
          让复杂的概念变得生动有趣
        </p>
        <div className="flex gap-4 justify-center">
          <Link href="/courses">
            <Button size="lg" className="gap-2">
              <BookOpen className="w-4 h-4" />
              开始学习
              <ArrowRight className="w-4 h-4" />
            </Button>
          </Link>
        </div>
      </section>

      {/* Features Section */}
      <section className="grid md:grid-cols-3 gap-6">
        <Card>
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

        <Card>
          <CardHeader>
            <Code className="w-8 h-8 text-primary mb-2" />
            <CardTitle>实战代码</CardTitle>
            <CardDescription>
              每节课都配有可运行的代码示例
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              不只是理论，更有动手实践的机会，代码均有详细注释
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <BookOpen className="w-8 h-8 text-primary mb-2" />
            <CardTitle>系统课程</CardTitle>
            <CardDescription>
              从基础到进阶，覆盖10大CS核心模块
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              50节精心设计的课程，循序渐进带你掌握计算机科学
            </p>
          </CardContent>
        </Card>
      </section>

      {/* Course Modules Preview */}
      <section className="space-y-6">
        <h2 className="text-3xl font-bold text-center">课程模块</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-5 gap-4">
          {[
            "计算机基础",
            "数据结构",
            "算法",
            "操作系统",
            "数据库",
            "计算机网络",
            "编程语言",
            "AI/ML基础",
            "Web开发",
            "系统架构",
          ].map((module, index) => (
            <div
              key={module}
              className="p-4 border rounded-lg text-center hover:border-primary transition-colors"
            >
              <span className="text-sm text-muted-foreground">模块{index + 1}</span>
              <p className="font-medium">{module}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
