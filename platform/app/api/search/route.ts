import { NextRequest, NextResponse } from "next/server";
import { fullTextSearch } from "@/lib/courses";

export async function GET(request: NextRequest) {
  const q = request.nextUrl.searchParams.get("q") || "";
  if (q.length < 2) {
    return NextResponse.json({ results: [] });
  }
  const results = fullTextSearch(q);
  return NextResponse.json({ results });
}
