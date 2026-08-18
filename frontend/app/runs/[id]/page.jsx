"use client";
import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '../../../lib/useAuth';
import { apiFetch } from '../../../lib/api';
import { 
  Play, CheckCircle, Square, ShieldAlert, Cpu, Terminal, RefreshCw, FileCheck,
  Zap, ArrowRight, GitPullRequest, Code, CheckCircle2, ShieldCheck, Sparkles
} from 'lucide-react';

export default function DedicatedTestRunPage() {
  const { loading: authLoading } = useAuth(true);
  const params = useParams();
  const runId = params?.id;
  const [run, setRun] = useState(null);
  const [findings, setFindings] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchRunDetails = async () => {
    try {
      const data = await apiFetch('/api/v1/runs');
      const found = data.find(r => r.id === runId);
      if (found) setRun(found);

      if (runId) {
        const fData = await apiFetch(`/api/v1/runs/${runId}/findings`);
        setFindings(fData);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRunDetails();
    const interval = setInterval(fetchRunDetails, 3000);
    return () => clearInterval(interval);
  }, [runId]);

  const pipelineStages = [
    { name: 'Discovery', key: 'DISCOVERING' },
    { name: 'Modeling', key: 'MODELING' },
    { name: 'Risk', key: 'RISK_ANALYSIS' },
    { name: 'Planning', key: 'PLANNING' },
    { name: 'Execution', key: 'EXECUTING' },
    { name: 'Observation', key: 'OBSERVING' },
    { name: 'Validation', key: 'VALIDATING' },
    { name: 'Reproduction', key: 'REPRODUCING' },
    { name: 'RCA', key: 'RCA' },
    { name: 'Remediation', key: 'REMEDIATION_PENDING' },
    { name: 'Retest', key: 'RETESTING' },
    { name: 'Regression', key: 'REGRESSION' },
    { name: 'Certify', key: 'CERTIFYING' },
    { name: 'Done', key: 'COMPLETED' }
  ];

  const handleKill = async () => {
    try {
      await fetch(`/api/v1/runs/${runId}/kill`, { method: 'POST' });
      fetchRunDetails();
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-3">
            <span className="text-xs font-mono font-bold bg-sky-500/20 text-sky-400 px-2.5 py-1 rounded border border-sky-500/30">
              RUN #{runId?.slice(0, 10)}
            </span>
            <span className="text-xs text-slate-400 font-mono">Autonomous Testing Pipeline v8.0</span>
          </div>
          <h1 className="text-xl font-bold text-white mt-2">Autonomous Execution & Evidence Graph</h1>
        </div>

        <div className="flex items-center gap-3">
          {run && !['COMPLETED', 'FAILED', 'CANCELLED'].includes(run.status) && (
            <button
              onClick={handleKill}
              className="flex items-center gap-2 bg-red-600/20 hover:bg-red-600/30 text-red-400 border border-red-500/40 px-4 py-2 rounded-lg font-medium text-xs transition"
            >
              <Square className="w-4 h-4" />
              <span>Emergency Kill Switch</span>
            </button>
          )}
          <Link
            href={`/reports`}
            className="flex items-center gap-2 bg-sky-600 hover:bg-sky-500 text-white px-4 py-2 rounded-lg font-medium text-xs transition shadow-lg shadow-sky-600/20"
          >
            <FileCheck className="w-4 h-4" />
            <span>View Full Report</span>
          </Link>
        </div>
      </div>

      {/* Human Effort KPI Widget for this Run */}
      <div className="bg-gradient-to-r from-sky-950/30 to-indigo-950/30 border border-sky-500/20 rounded-xl p-5 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-sky-500/20 border border-sky-500/30 flex items-center justify-center text-sky-400">
            <Zap className="w-5 h-5" />
          </div>
          <div>
            <div className="text-sm font-bold text-white">Human Effort Reduction KPI (PRD Section 3)</div>
            <div className="text-xs text-slate-400">
              Manual effort: <strong className="text-slate-200">{run?.estimated_manual_hours || 48.0} hrs</strong> | ATE Automated: <strong className="text-sky-300">{run?.automated_hours || 0.5} hrs</strong> | Human review: <strong className="text-amber-300">{run?.human_review_hours || 4.0} hrs</strong>
            </div>
          </div>
        </div>
        <div className="text-right">
          <div className="text-2xl font-black text-emerald-400">{run?.effort_reduction_percentage || 88.5}%</div>
          <div className="text-[10px] uppercase font-bold text-emerald-500">Effort Reduction</div>
        </div>
      </div>

      {/* Live 14-State Pipeline Stepper (PRD Section 61) */}
      <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-6 space-y-4">
        <h2 className="text-xs font-semibold uppercase text-slate-400 tracking-wider">Mandatory State Machine Flow</h2>
        <div className="grid grid-cols-2 sm:grid-cols-7 gap-2">
          {pipelineStages.map((s) => {
            const isCurrent = run?.status === s.key;
            return (
              <div
                key={s.name}
                className={`p-2.5 rounded-xl border text-center transition ${
                  isCurrent
                    ? 'bg-sky-500/20 border-sky-500 text-sky-300 font-bold shadow-lg shadow-sky-500/10 animate-pulse'
                    : 'bg-slate-900/60 border-slate-800 text-slate-400'
                }`}
              >
                <div className="text-[11px] font-bold">{s.name}</div>
                <div className="text-[9px] uppercase tracking-wider mt-0.5 opacity-80">{s.key}</div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Findings with Code Diffs & Retest Verdicts */}
      <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-6 space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-bold text-white">Validated Findings & Autonomous Remediations ({findings.length})</h2>
          <span className="text-xs text-slate-400">Cryptographically hashed SHA-256 evidence</span>
        </div>

        {findings.length === 0 ? (
          <div className="text-center py-6 text-slate-500 text-sm">
            No defects found yet. The autonomous engine is currently executing test cases.
          </div>
        ) : (
          <div className="space-y-4">
            {findings.map((f, idx) => (
              <div key={f.id || idx} className="bg-[#0f172a] border border-slate-800 rounded-xl p-5 space-y-3">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <span className={`px-2.5 py-0.5 rounded text-[10px] font-extrabold ${
                      f.severity === 'CRITICAL' ? 'bg-red-500/20 text-red-400 border border-red-500/30' :
                      f.severity === 'HIGH' ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' :
                      'bg-sky-500/20 text-sky-400 border border-sky-500/30'
                    }`}>
                      {f.severity}
                    </span>
                    <h3 className="text-sm font-bold text-white">{f.title}</h3>
                  </div>
                  <div className="flex items-center gap-2 text-xs">
                    <span className="text-slate-400">Retest:</span>
                    <span className={`font-bold px-2 py-0.5 rounded text-[10px] ${
                      f.retest_verdict === 'RESOLVED' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-red-500/20 text-red-400'
                    }`}>
                      {f.retest_verdict || 'STILL_VULNERABLE'}
                    </span>
                  </div>
                </div>

                <div className="text-xs text-slate-300">
                  <strong>Affected Endpoint:</strong> <code className="bg-slate-900 px-1.5 py-0.5 rounded text-sky-300">{f.affected_endpoint || '/api/v1/resource'}</code>
                </div>

                <div className="text-xs text-slate-400">
                  <strong>Root Cause Analysis:</strong> {f.root_cause}
                </div>

                {f.remediation_diff && (
                  <div className="bg-black/50 border border-slate-800 rounded-lg p-3 text-xs font-mono text-emerald-400 overflow-x-auto">
                    <div className="text-[10px] text-slate-500 uppercase font-bold mb-1">// Actionable Code-Level Remediation Diff (PRD Section 29)</div>
                    <pre>{f.remediation_diff}</pre>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
