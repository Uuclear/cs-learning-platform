import { notFound } from "next/navigation";
import { getCourseBySlug, getAllModules } from "@/lib/courses";
import { CourseContent } from "@/components/course/CourseContent";
import { Sidebar } from "@/components/layout/Sidebar";
import { CodeBlock } from "@/components/course/CodeBlock";

interface CoursePageProps {
  params: {
    slug: string;
  };
}

export default function CoursePage({ params }: CoursePageProps) {
  const course = getCourseBySlug(params.slug);
  const modules = getAllModules();

  if (!course) {
    notFound();
  }

  return (
    <div className="flex min-h-[calc(100vh-3.5rem)]">
      <Sidebar modules={modules} currentCourse={course} />
      <div className="flex-1 p-8 overflow-y-auto">
        <CourseContent course={course} content={<CourseLesson />} />
      </div>
    </div>
  );
}

function CourseLesson() {
  const pythonCode = `# 模拟冯诺依曼架构的简单CPU

class SimpleCPU:
    def __init__(self):
        # 寄存器（最快速的存储）
        self.registers = {'A': 0, 'B': 0}
        # 程序计数器，记录当前执行到哪条指令
        self.pc = 0
        
    def execute(self, instruction):
        """执行单条指令"""
        parts = instruction.split()
        opcode = parts[0]
        
        if opcode == 'LOAD':
            # LOAD A 5  -> 把5加载到寄存器A
            reg, value = parts[1], int(parts[2])
            self.registers[reg] = value
            print(f"执行: {instruction} -> 寄存器{reg} = {value}")
            
        elif opcode == 'ADD':
            # ADD A B -> A = A + B
            reg1, reg2 = parts[1], parts[2]
            result = self.registers[reg1] + self.registers[reg2]
            self.registers[reg1] = result
            print(f"执行: {instruction} -> {reg1} = {result}")
            
        elif opcode == 'PRINT':
            # PRINT A -> 输出寄存器A的值
            reg = parts[1]
            print(f"输出: 寄存器{reg} = {self.registers[reg]}")
            
        self.pc += 1

# 测试程序：计算 5 + 3
program = [
    'LOAD A 5',    # 把5加载到寄存器A
    'LOAD B 3',    # 把3加载到寄存器B
    'ADD A B',     # A = A + B (结果是8)
    'PRINT A',     # 输出结果
]

print("=== 开始执行程序 ===")
cpu = SimpleCPU()

for instruction in program:
    cpu.execute(instruction)

print(f"\\n程序计数器最终值: {cpu.pc}")
print(f"寄存器状态: {cpu.registers}")`;

  return (
    <div className="space-y-8">
      {/* 开场白 */}
      <section>
        <h2 className="text-2xl font-semibold text-primary mb-4">开场白</h2>
        <p className="leading-7 mb-4">
          想象一下，你走进一家餐厅，点了一份宫保鸡丁。几分钟后，一盘香喷喷的菜就端上来了。
          但你有没有想过，这短短几分钟背后，厨房里的"大厨们"是如何协作的？
        </p>
        <p className="leading-7 mb-4">
          计算机的工作原理，其实和餐厅厨房非常相似！今天，我们就来揭开计算机"厨房"的神秘面纱。
        </p>
      </section>

      {/* 核心概念 */}
      <section>
        <h2 className="text-2xl font-semibold text-primary mb-4">核心概念：冯诺依曼架构</h2>
        <p className="leading-7 mb-4">
          1945年，数学家冯·诺依曼提出了一种计算机设计架构，至今仍然是现代计算机的基础。
          这个架构把计算机分成了五大组成部分：
        </p>

        <h3 className="text-xl font-semibold mt-6 mb-2">1. 运算器（ALU）- "大厨"</h3>
        <p className="leading-7 mb-4">
          就像厨房里的大厨负责炒菜一样，<strong>运算器</strong>负责执行所有的数学和逻辑运算：
        </p>
        <ul className="list-disc pl-6 mb-4 space-y-2">
          <li>加法、减法、乘法、除法</li>
          <li>比较大小</li>
          <li>逻辑判断（与、或、非）</li>
        </ul>

        <h3 className="text-xl font-semibold mt-6 mb-2">2. 控制器 - "主厨"</h3>
        <p className="leading-7 mb-4">
          <strong>控制器</strong>就像餐厅的主厨，它负责：
        </p>
        <ul className="list-disc pl-6 mb-4 space-y-2">
          <li>指挥运算器什么时候做什么</li>
          <li>协调各个部件的工作</li>
          <li>按照程序指令一步步执行</li>
        </ul>

        <h3 className="text-xl font-semibold mt-6 mb-2">3. 存储器 - "冰箱和货架"</h3>
        <p className="leading-7 mb-4">
          <strong>存储器</strong>用来存放程序指令（菜谱）和数据（食材）。
        </p>

        <div className="overflow-x-auto my-4">
          <table className="w-full border-collapse border border-border">
            <thead className="bg-muted">
              <tr>
                <th className="border border-border px-4 py-2 text-left font-semibold">存储类型</th>
                <th className="border border-border px-4 py-2 text-left font-semibold">速度</th>
                <th className="border border-border px-4 py-2 text-left font-semibold">容量</th>
                <th className="border border-border px-4 py-2 text-left font-semibold">比喻</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="border border-border px-4 py-2">寄存器</td>
                <td className="border border-border px-4 py-2">最快</td>
                <td className="border border-border px-4 py-2">最小</td>
                <td className="border border-border px-4 py-2">厨师手边的调料盒</td>
              </tr>
              <tr>
                <td className="border border-border px-4 py-2">缓存</td>
                <td className="border border-border px-4 py-2">很快</td>
                <td className="border border-border px-4 py-2">很小</td>
                <td className="border border-border px-4 py-2">操作台上的食材</td>
              </tr>
              <tr>
                <td className="border border-border px-4 py-2">内存(RAM)</td>
                <td className="border border-border px-4 py-2">快</td>
                <td className="border border-border px-4 py-2">中等</td>
                <td className="border border-border px-4 py-2">厨房里的冰箱</td>
              </tr>
              <tr>
                <td className="border border-border px-4 py-2">硬盘</td>
                <td className="border border-border px-4 py-2">慢</td>
                <td className="border border-border px-4 py-2">很大</td>
                <td className="border border-border px-4 py-2">仓库</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h3 className="text-xl font-semibold mt-6 mb-2">4. 输入设备 - "点餐系统"</h3>
        <p className="leading-7 mb-4">
          <strong>输入设备</strong>负责把外部信息传给计算机：键盘、鼠标、触摸屏、麦克风、摄像头等。
          就像顾客通过点餐系统把订单传给厨房。
        </p>

        <h3 className="text-xl font-semibold mt-6 mb-2">5. 输出设备 - "上菜窗口"</h3>
        <p className="leading-7 mb-4">
          <strong>输出设备</strong>负责把计算机处理的结果展示出来：显示器、打印机、扬声器等。
          就像厨房通过上菜窗口把做好的菜端给顾客。
        </p>
      </section>

      {/* 深入理解 */}
      <section>
        <h2 className="text-2xl font-semibold text-primary mb-4">深入理解：为什么这样设计？</h2>
        <p className="leading-7 mb-4">
          冯诺依曼架构的核心思想是<strong>"存储程序"</strong>。
        </p>
        <p className="leading-7 mb-4">
          在早期的计算机中，程序是通过物理线路（比如插线板）来"写"的，要改变程序就得重新接线，非常麻烦。
        </p>
        <p className="leading-7 mb-4">
          冯诺依曼的天才之处在于：<strong>把程序也当作数据来存储</strong>。
        </p>
        <p className="leading-7 mb-4">
          这样，计算机就可以按照<strong>"取指-译码-执行"</strong>循环来工作。
        </p>
      </section>

      {/* 实际应用 */}
      <section>
        <h2 className="text-2xl font-semibold text-primary mb-4">实际应用</h2>
        <p className="leading-7 mb-4">
          你现在的手机、电脑、甚至智能手表，都是基于冯诺依曼架构设计的。
        </p>
        <p className="leading-7 mb-4">
          虽然经过了70多年的发展，计算机的速度提升了数百万倍，但基本原理没有变：
        </p>
        <ul className="list-disc pl-6 mb-4 space-y-2">
          <li>CPU（中央处理器）= 运算器 + 控制器</li>
          <li>内存 = 存储器</li>
          <li>各种外设 = 输入/输出设备</li>
        </ul>
      </section>

      {/* 常见误区 */}
      <section>
        <h2 className="text-2xl font-semibold text-primary mb-4">常见误区</h2>
        
        <div className="border-l-4 border-primary pl-4 py-2 my-4 bg-muted/50">
          <p className="font-semibold">误区1：内存越大，电脑越快</p>
          <p className="text-muted-foreground">
            真相：内存影响的是能同时运行多少程序，而不是单个程序的速度。CPU和硬盘速度对性能影响更大。
          </p>
        </div>

        <div className="border-l-4 border-primary pl-4 py-2 my-4 bg-muted/50">
          <p className="font-semibold">误区2：CPU核心越多越好</p>
          <p className="text-muted-foreground">
            真相：对于单线程程序，核心数影响不大。多核心主要对并行任务有帮助。
          </p>
        </div>

        <div className="border-l-4 border-primary pl-4 py-2 my-4 bg-muted/50">
          <p className="font-semibold">误区3：存储器就是硬盘</p>
          <p className="text-muted-foreground">
            真相：在计算机术语中，"存储器"通常指内存(RAM)，而不是硬盘。硬盘属于"外存储器"。
          </p>
        </div>
      </section>

      {/* 动手实践 */}
      <section>
        <h2 className="text-2xl font-semibold text-primary mb-4">动手实践</h2>
        <p className="leading-7 mb-4">
          下面用Python模拟一个简单的CPU执行过程：
        </p>
        <CodeBlock code={pythonCode} language="python" filename="cpu_simulation.py" />
      </section>

      {/* 小结与思考 */}
      <section>
        <h2 className="text-2xl font-semibold text-primary mb-4">小结与思考</h2>
        <p className="leading-7 mb-4">今天我们学习了：</p>
        <ol className="list-decimal pl-6 mb-4 space-y-2">
          <li><strong>冯诺依曼架构的五大组成部分</strong>：运算器、控制器、存储器、输入设备、输出设备</li>
          <li><strong>存储程序思想</strong>：程序和数据都以二进制形式存储在存储器中</li>
          <li><strong>取指-译码-执行循环</strong>：CPU工作的基本流程</li>
        </ol>

        <h3 className="text-xl font-semibold mt-6 mb-2">思考题</h3>
        <ol className="list-decimal pl-6 mb-4 space-y-2">
          <li>如果把计算机比作餐厅，你觉得显卡在这个比喻中相当于什么？</li>
          <li>为什么现代计算机要有缓存(Cache)？它解决了什么问题？</li>
          <li>在Python模拟的CPU中，如果要实现减法操作，你会怎么设计指令？</li>
          <li>思考一下：你的手机是如何协调CPU、内存、屏幕、摄像头等部件协同工作的？</li>
        </ol>
      </section>
    </div>
  );
}
