"use client";

import Link from "next/link";
import { BookOpen, Menu, X, GraduationCap } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/Button";
import { SearchBar } from "@/components/course/SearchBar";
import { Course } from "@/types/course";
import { ThemeToggle } from "./ThemeToggle";

interface HeaderProps {
  courses: Course[];
}

export function Header({ courses }: HeaderProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navItems = [
    { href: "/", label: "首页" },
    { href: "/courses", label: "课程" },
  ];

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto px-4 flex h-14 items-center">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2 mr-6">
          <GraduationCap className="h-6 w-6 text-primary" />
          <span className="font-bold text-lg hidden sm:inline-block">
            CS知识学习
          </span>
        </Link>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex items-center gap-6 text-sm font-medium flex-1">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="transition-colors hover:text-primary text-foreground"
            >
              {item.label}
            </Link>
          ))}
        </nav>

        {/* Search bar - desktop */}
        <div className="hidden md:block mx-4">
          <SearchBar />
        </div>

        {/* Right side actions */}
        <div className="hidden md:flex items-center gap-4 ml-auto">
          <ThemeToggle />
          <Link href="/courses">
            <Button variant="outline" size="sm" className="gap-2">
              <BookOpen className="h-4 w-4" />
              开始学习
            </Button>
          </Link>
        </div>

        {/* Mobile menu button */}
        <button
          className="md:hidden ml-auto p-2"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          aria-label="Toggle menu"
        >
          {mobileMenuOpen ? (
            <X className="h-5 w-5" />
          ) : (
            <Menu className="h-5 w-5" />
          )}
        </button>
      </div>

      {/* Mobile Navigation */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t">
          <div className="container mx-auto px-4 py-4 space-y-4">
            {/* Mobile search */}
            <SearchBar />
            <nav className="flex flex-col gap-4">
              {navItems.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className="text-sm font-medium transition-colors hover:text-primary"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  {item.label}
                </Link>
              ))}
            </nav>
            <div className="flex justify-center">
              <ThemeToggle />
            </div>
            <Link href="/courses" onClick={() => setMobileMenuOpen(false)}>
              <Button variant="outline" size="sm" className="w-full gap-2">
                <BookOpen className="h-4 w-4" />
                开始学习
              </Button>
            </Link>
          </div>
        </div>
      )}
    </header>
  );
}
