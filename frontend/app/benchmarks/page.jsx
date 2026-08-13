"use client";
import { useState } from 'react';
import { Award, Play, CheckCircle2, AlertTriangle, ShieldCheck, Target, RefreshCw } from 'lucide-react';

export default function BenchmarksPage() {
  const [loading, setLoading] = useState(false);
  const [evalResult, setEvalResult] = useState({
    total_ground_truth: 5,
    defects_detected: 4,
    false_positives: 0,
    false_negatives: 1,
    precision: 100.0,
    recall: 80.0,
    f1_score: 88.9,
    rca_accuracy: 100.0,
    reproduction_rate: 100.0
  });

  const defects = [
    { code: 'DEF_BOLA', name: 'BOLA / Authorization Bypass', endpoint: '/api/v1/user/profile', status: 'DETECTED', rca: '100% Correct' },
    { code: 'DEF_SQLI', name: 'SQL Injection Vulnerability', endpoint: '/api/v1/products/search', status: 'DETECTED', rca: '100% Correct' },
    { code: 'DEF_RACE', name: 'Race Condition / Idempotency', endpoint: '/api/v1/checkout', status: 'DETECTED', rca: '100% Correct' },
    { code: 'DEF_PERF', name: 'Performance Degradation', endpoint: '/api/v1/analytics/report', status: 'DETECTED', rca: '100% Correct' },
    { code: 'DEF_AI', name: 'AI RAG Hallucination & Prompt Injection', endpoint: '/api/v1/ai/query', status: 'MISSED', rca: 'N/A' }
  ];

  const handleRunEvaluation = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/benchmarks/evaluate', { method: 'POST' });
      if (res.ok) {
        const data = await res.json();
        setEvalResult(data.evaluation);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between border-b border-gray-800 pb-4">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <Award className="w-6 h-6 text-amber-400" />
            <span>Ground Truth Benchmark Evaluation</span>
          </h1>
          <p className="text-sm text-gray-400 mt-1">
            Automated benchmark evaluator comparing engine detection results against ground truth defect catalog.
          </p>
        </div>
        <button
          onClick={handleRunEvaluation}
          disabled={loading}
          className="flex items-center gap-2 bg-[#0284c7] hover:bg-[#0369a1] text-white px-5 py-2.5 rounded-xl font-semibold transition shadow-lg shadow-sky-600/20"
        >
          {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4 fill-white" />}
          <span>Run Ground Truth Benchmark</span>
        </button>
      </div>

      {/* Benchmark Score Metrics Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="bg-[#111827] border border-gray-800 rounded-xl p-5">
          <span className="text-xs font-semibold text-gray-400 uppercase">Precision</span>
          <div className="text-2xl font-black text-emerald-400 mt-1">{evalResult.precision}%</div>
          <span className="text-xs text-gray-500">True Positives / (TP + FP)</span>
        </div>
        <div className="bg-[#111827] border border-gray-800 rounded-xl p-5">
          <span className="text-xs font-semibold text-gray-400 uppercase">Recall</span>
          <div className="text-2xl font-black text-sky-400 mt-1">{evalResult.recall}%</div>
          <span className="text-xs text-gray-500">{evalResult.defects_detected} of {evalResult.total_ground_truth} Defects</span>
        </div>
        <div className="bg-[#111827] border border-gray-800 rounded-xl p-5">
          <span className="text-xs font-semibold text-gray-400 uppercase">F1 Score</span>
          <div className="text-2xl font-black text-amber-400 mt-1">{evalResult.f1_score}%</div>
          <span className="text-xs text-gray-500">Harmonic Mean</span>
        </div>
        <div className="bg-[#111827] border border-gray-800 rounded-xl p-5">
          <span className="text-xs font-semibold text-gray-400 uppercase">RCA Accuracy</span>
          <div className="text-2xl font-black text-purple-400 mt-1">{evalResult.rca_accuracy}%</div>
          <span className="text-xs text-gray-500">Root Cause Inference</span>
        </div>
      </div>

      {/* Ground Truth Defect Catalog Table */}
      <div className="bg-[#111827] border border-gray-800 rounded-xl p-6 space-y-4">
        <h2 className="text-sm font-semibold uppercase text-gray-400 tracking-wider">Ground Truth Defect Catalog</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-gray-300">
            <thead className="text-xs font-semibold text-gray-500 uppercase bg-[#0c121e] border-b border-gray-800">
              <tr>
                <th className="px-4 py-3">Code</th>
                <th className="px-4 py-3">Defect Description</th>
                <th className="px-4 py-3">Target Endpoint</th>
                <th className="px-4 py-3">Detection Status</th>
                <th className="px-4 py-3">RCA Inference Accuracy</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-800">
              {defects.map((d) => (
                <tr key={d.code} className="hover:bg-gray-900/40">
                  <td className="px-4 py-3 font-mono text-sky-400">{d.code}</td>
                  <td className="px-4 py-3 font-semibold text-white">{d.name}</td>
                  <td className="px-4 py-3 font-mono text-gray-400">{d.endpoint}</td>
                  <td className="px-4 py-3">
                    <span className={`text-xs font-bold px-2 py-0.5 rounded ${
                      d.status === 'DETECTED' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'bg-red-500/20 text-red-400'
                    }`}>
                      {d.status}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-purple-300">{d.rca}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
