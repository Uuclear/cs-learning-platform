"use client";

import { Printer } from "lucide-react";

export function PrintButton() {
  const handlePrint = () => {
    window.print();
  };

  return (
    <button
      onClick={handlePrint}
      className="print:hidden flex items-center gap-2 px-3 py-2 text-sm rounded-lg border border-input hover:bg-accent transition-colors"
      title="打印课程内容"
    >
      <Printer className="h-4 w-4" />
      <span className="hidden sm:inline">打印</span>
    </button>
  );
}
