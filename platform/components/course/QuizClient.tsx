"use client";

import { useState, useCallback } from "react";
import { QuizQuestion } from "@/types/course";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { CheckCircle, XCircle, HelpCircle, Trophy, RotateCcw } from "lucide-react";

interface QuizClientProps {
  questions: QuizQuestion[];
  courseId: string;
}

export function QuizClient({ questions, courseId }: QuizClientProps) {
  const [answers, setAnswers] = useState<Record<number, number>>({});
  const [showResults, setShowResults] = useState(false);
  const [expandedExplanations, setExpandedExplanations] = useState<Set<number>>(new Set());

  const handleAnswer = useCallback((questionIndex: number, answerIndex: number) => {
    if (showResults) return;
    setAnswers((prev) => ({ ...prev, [questionIndex]: answerIndex }));
  }, [showResults]);

  const toggleExplanation = useCallback((questionIndex: number) => {
    setExpandedExplanations((prev) => {
      const next = new Set(prev);
      if (next.has(questionIndex)) {
        next.delete(questionIndex);
      } else {
        next.add(questionIndex);
      }
      return next;
    });
  }, []);

  const handleSubmit = () => setShowResults(true);

  const handleReset = () => {
    setAnswers({});
    setShowResults(false);
    setExpandedExplanations(new Set());
  };

  const score = questions.reduce((acc, q, i) => {
    return acc + (answers[i] === q.answer ? 1 : 0);
  }, 0);

  const answeredCount = Object.keys(answers).length;
  const allAnswered = answeredCount === questions.length;
  const scorePercent = allAnswered ? Math.round((score / questions.length) * 100) : 0;

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="flex items-center gap-2">
              <HelpCircle className="w-5 h-5" />
              课后测验
            </CardTitle>
            <CardDescription>
              共 {questions.length} 道题，检验你的学习成果
            </CardDescription>
          </div>
          {showResults && (
            <Badge
              variant={scorePercent >= 80 ? "default" : scorePercent >= 60 ? "secondary" : "destructive"}
              className="text-lg px-4 py-1"
            >
              <Trophy className="w-4 h-4 mr-1" />
              {score}/{questions.length} ({scorePercent}%)
            </Badge>
          )}
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        {questions.map((q, index) => {
          const isCorrect = answers[index] === q.answer;
          const hasAnswer = answers[index] !== undefined;

          return (
            <div key={q.id} className="space-y-3 pb-4 border-b last:border-b-0">
              <p className="font-medium">
                {index + 1}. {q.question}
              </p>

              <div className="space-y-2">
                {q.options.map((option, optIndex) => {
                  const isSelected = answers[index] === optIndex;
                  const isCorrectOption = optIndex === q.answer;

                  let optionClass = "border-border hover:bg-accent";
                  if (showResults) {
                    if (isCorrectOption) {
                      optionClass = "border-green-500 bg-green-50";
                    } else if (isSelected && !isCorrect) {
                      optionClass = "border-red-500 bg-red-50";
                    }
                  } else if (isSelected) {
                    optionClass = "border-primary bg-primary/10";
                  }

                  return (
                    <button
                      key={optIndex}
                      onClick={() => handleAnswer(index, optIndex)}
                      disabled={showResults}
                      className={`w-full text-left p-3 rounded-lg border transition-colors ${optionClass}`}
                    >
                      <span className="inline-flex items-center gap-2">
                        <span className="w-6 h-6 rounded-full border-2 flex items-center justify-center text-xs font-bold shrink-0
                          ${showResults && isCorrectOption ? 'border-green-500 bg-green-500 text-white' :
                            showResults && isSelected && !isCorrect ? 'border-red-500 bg-red-500 text-white' :
                            isSelected ? 'border-primary bg-primary text-white' :
                            'border-muted-foreground'}">
                          {String.fromCharCode(65 + optIndex)}
                        </span>
                        {option}
                        {showResults && isCorrectOption && (
                          <CheckCircle className="w-4 h-4 text-green-600 ml-auto shrink-0" />
                        )}
                        {showResults && isSelected && !isCorrect && (
                          <XCircle className="w-4 h-4 text-red-600 ml-auto shrink-0" />
                        )}
                      </span>
                    </button>
                  );
                })}
              </div>

              {/* Explanation toggle */}
              {showResults && q.explanation && (
                <div>
                  <button
                    onClick={() => toggleExplanation(index)}
                    className="text-sm text-primary hover:underline flex items-center gap-1"
                  >
                    <HelpCircle className="w-3 h-3" />
                    {expandedExplanations.has(index) ? "收起解析" : "查看解析"}
                  </button>
                  {expandedExplanations.has(index) && (
                    <p className="text-sm text-muted-foreground mt-2 p-3 bg-muted rounded-md">
                      {q.explanation}
                    </p>
                  )}
                </div>
              )}

              {/* Result indicator */}
              {showResults && hasAnswer && (
                <div className={`text-sm font-medium ${isCorrect ? "text-green-600" : "text-red-600"}`}>
                  {isCorrect ? "✅ 回答正确！" : `❌ 回答错误，正确答案是 ${String.fromCharCode(65 + q.answer)}`}
                </div>
              )}
            </div>
          );
        })}

        {/* Actions */}
        <div className="flex gap-4 pt-4">
          {!showResults && (
            <Button
              onClick={handleSubmit}
              disabled={!allAnswered}
              className="flex-1"
            >
              提交答案 ({answeredCount}/{questions.length})
            </Button>
          )}
          {showResults && (
            <Button
              onClick={handleReset}
              variant="outline"
              className="flex-1 gap-2"
            >
              <RotateCcw className="w-4 h-4" />
              重新答题
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
