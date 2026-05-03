import Link from "next/link";

export function Footer() {
  return (
    <footer className="border-t bg-muted/30">
      <div className="container mx-auto px-4 py-8">
        <div className="grid md:grid-cols-3 gap-8">
          {/* Brand */}
          <div>
            <h3 className="font-semibold text-lg mb-2">CS知识学习网站</h3>
            <p className="text-sm text-muted-foreground leading-relaxed">
              一个通俗易懂、幽默风趣的计算机科学学习平台。
              用生活化的比喻解释复杂的计算机概念。
            </p>
          </div>

          {/* Modules */}
          <div>
            <h3 className="font-semibold text-lg mb-2">课程模块</h3>
            <ul className="space-y-1 text-sm text-muted-foreground">
              <li><Link href="/courses" className="hover:text-foreground transition-colors">计算机基础</Link></li>
              <li><Link href="/courses" className="hover:text-foreground transition-colors">数据结构与算法</Link></li>
              <li><Link href="/courses" className="hover:text-foreground transition-colors">操作系统与网络</Link></li>
              <li><Link href="/courses" className="hover:text-foreground transition-colors">数据库与安全</Link></li>
              <li><Link href="/courses" className="hover:text-foreground transition-colors">编程与工程实践</Link></li>
            </ul>
          </div>

          {/* Info */}
          <div>
            <h3 className="font-semibold text-lg mb-2">关于</h3>
            <div className="space-y-2 text-sm text-muted-foreground">
              <p>100门课程，15个核心模块</p>
              <p>覆盖从基础到进阶的完整CS知识体系</p>
              <p>每节课包含代码示例和课后测验</p>
            </div>
          </div>
        </div>

        <div className="mt-8 pt-6 border-t text-center text-sm text-muted-foreground">
          <p>CS知识学习平台 &copy; {new Date().getFullYear()}</p>
        </div>
      </div>
    </footer>
  );
}
