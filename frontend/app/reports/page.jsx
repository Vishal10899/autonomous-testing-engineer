"use client";
import { FileCheck, ShieldAlert, CheckCircle, XCircle, AlertTriangle } from 'lucide-react';

export default function ReadinessReportPage() {
  const domains = [
    { name: 'Functional & API Contract', score: 100.0, status: 'PASSED', total: 10, passed: 10 },
    { name: 'Security & Authorization', score: 25.0, status: 'FAILED', total: 4, passed: 1 },
    { name: 'Performance & Latency', score: 75.0, status: 'WARNING', total: 4, passed: 3 },
    { name: 'Database & Concurrency', score: 50.0, status: 'FAILED', total: 2, passed: 1 },
    { name: 'AI Quality & RAG Grounding', score: 66.7, status: 'WARNING', total: 3, passed: 2 }
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between border-b border-gray-800 pb-4">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <FileCheck className="w-6 h-6 text-sky-400" />
            <span>Defensible Production Readiness Report</span>
          </h1>
          <p className="text-sm text-gray-400 mt-1">
            Evidence-backed release decision with transparent multi-domain breakdown and policy blocker enforcement.
          </p>
        </div>
      </div>

      {/* Main Verdict Card */}
      <div className="bg-red-500/10 border border-red-500/40 rounded-2xl p-6 text-center space-y-3">
        <div className="inline-flex items-center gap-2 text-red-400 bg-red-500/20 px-4 py-1.5 rounded-full border border-red-500/30 text-sm font-bold uppercase tracking-wider">
          <XCircle className="w-5 h-5" />
          <span>PRODUCTION VERDICT: NOT READY</span>
        </div>
        <h2 className="text-3xl font-extrabold text-white">Release Blocked by 3 Critical Findings</h2>
        <p className="text-gray-300 max-w-2xl mx-auto text-sm">
          The Autonomous Testing Engineer has determined that this system is NOT READY for production deployment due to unmitigated critical security vulnerabilities and database race conditions.
        </p>
      </div>

      {/* Domain Scorecards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {domains.map((d) => (
          <div key={d.name} className="bg-[#111827] border border-gray-800 rounded-xl p-5 space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm font-bold text-white">{d.name}</span>
              <span className={`text-xs font-bold px-2 py-0.5 rounded ${
                d.status === 'PASSED' ? 'bg-emerald-500/20 text-emerald-400' :
                d.status === 'WARNING' ? 'bg-amber-500/20 text-amber-400' :
                'bg-red-500/20 text-red-400'
              }`}>
                {d.status}
              </span>
            </div>
            <div className="flex items-baseline gap-2">
              <span className="text-2xl font-black text-white">{d.score}%</span>
              <span className="text-xs text-gray-500">({d.passed}/{d.total} tests passed)</span>
            </div>
            <div className="w-full bg-gray-800 h-2 rounded-full overflow-hidden">
              <div
                className={`h-full rounded-full ${
                  d.score >= 90 ? 'bg-emerald-500' : d.score >= 70 ? 'bg-amber-500' : 'bg-red-500'
                }`}
                style={{ width: `${d.score}%` }}
              ></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
