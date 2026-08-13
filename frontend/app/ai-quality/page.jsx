"use client";
import { Cpu, CheckCircle, ShieldAlert, Sparkles } from 'lucide-react';

export default function AIQualityDashboardPage() {
  const aiMetrics = {
    grounding_score: 0.15,
    prompt_injection_resistance: "EXPLOITED",
    hallucination_rate: "85.0%",
    tool_safety: "VERIFIED"
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <Cpu className="w-6 h-6 text-purple-400" />
            <span>AI / LLM & RAG Quality Analytics</span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Evaluates grounding accuracy, hallucination detection, prompt injection vulnerability, and tool permissions (PRD Section 30).
          </p>
        </div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-5 space-y-1">
          <span className="text-xs font-semibold uppercase text-slate-400">RAG Grounding Score</span>
          <div className="text-2xl font-black text-red-400">{aiMetrics.grounding_score}</div>
          <span className="text-[11px] text-slate-500">Threshold: 0.50</span>
        </div>

        <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-5 space-y-1">
          <span className="text-xs font-semibold uppercase text-slate-400">Prompt Injection</span>
          <div className="text-2xl font-black text-red-400">{aiMetrics.prompt_injection_resistance}</div>
          <span className="text-[11px] text-slate-500">System prompt flag leak</span>
        </div>

        <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-5 space-y-1">
          <span className="text-xs font-semibold uppercase text-slate-400">Hallucination Rate</span>
          <div className="text-2xl font-black text-amber-400">{aiMetrics.hallucination_rate}</div>
          <span className="text-[11px] text-slate-500">Unsupported claims</span>
        </div>

        <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-5 space-y-1">
          <span className="text-xs font-semibold uppercase text-slate-400">Tool Safety</span>
          <div className="text-2xl font-black text-emerald-400">{aiMetrics.tool_safety}</div>
          <span className="text-[11px] text-slate-500">MCP tool permissions</span>
        </div>
      </div>
    </div>
  );
}
