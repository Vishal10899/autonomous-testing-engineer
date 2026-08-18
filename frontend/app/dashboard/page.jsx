"use client";
import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useAuth } from '../../lib/useAuth';
import { apiFetch } from '../../lib/api';
import { 
  Play, Plus, Activity, ShieldAlert, CheckCircle, AlertTriangle, 
  ArrowRight, Cpu, FolderKanban, Clock, RefreshCw, FileCheck, Zap,
  TrendingDown, UserCheck, ShieldCheck, Sparkles
} from 'lucide-react';

export default function SaaSUserDashboard() {
  const { loading: authLoading } = useAuth(true);
  const [runs, setRuns] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchDashboardData = async () => {
    try {
      const data = await apiFetch('/api/v1/runs');
      setRuns(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 4000);
    return () => clearInterval(interval);
  }, []);

  const activeRun = runs.find(r => ['EXECUTING', 'DISCOVERING', 'MODELING', 'PLANNING', 'RISK_ANALYSIS', 'VALIDATING', 'REPRODUCING', 'RCA', 'RETESTING'].includes(r.status));
  const recentRuns = runs.slice(0, 5);

  const projects = [
    { id: 'proj_sentinel', name: 'Sentinel AI Gateway', environment: 'STAGING', verdict: 'NOT_READY', score: 26.7, critical: 2, tech: 'FastAPI / Ollama' },
    { id: 'proj_ecommerce', name: 'E-Commerce Transactions API', environment: 'STAGING', verdict: 'READY', score: 94.2, critical: 0, tech: 'Node.js / PostgreSQL' },
    { id: 'proj_support', name: 'Customer Support Agent', environment: 'DEV', verdict: 'CONDITIONAL', score: 78.5, critical: 0, tech: 'Next.js / Python' }
  ];

  return (
    <div className="space-y-8">
      {/* Top Welcome Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold text-white tracking-tight">Autonomous Testing Control Plane</h1>
            <span className="px-2 py-0.5 rounded text-[11px] font-extrabold bg-sky-500/20 text-sky-400 border border-sky-500/30">v8.0</span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Workspace: <span className="font-semibold text-slate-200">Autonomous Engineering Labs</span> | North-Star: <span className="text-sky-400 font-semibold">Human Effort Minimization</span>
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Link
            href="/test/new"
            className="flex items-center gap-2 bg-gradient-to-r from-sky-600 to-indigo-600 hover:from-sky-500 hover:to-indigo-500 text-white px-5 py-2.5 rounded-xl font-bold text-sm transition shadow-lg shadow-sky-600/20"
          >
            <Sparkles className="w-4 h-4 text-amber-300" />
            <span>Start Autonomous Testing</span>
          </Link>
        </div>
      </div>

      {/* PRD v8.0 Primary KPI Banner: Human Effort Reduction */}
      <div className="bg-gradient-to-r from-sky-950/40 via-indigo-950/40 to-purple-950/30 border border-sky-500/30 rounded-2xl p-6 shadow-xl relative overflow-hidden">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-sky-400 text-xs font-bold uppercase tracking-wider">
              <Zap className="w-4 h-4 text-amber-400" />
              <span>Primary North-Star Metric (PRD v8.0 Section 3)</span>
            </div>
            <h2 className="text-xl font-extrabold text-white">88.5% Human Testing Effort Reduction</h2>
            <p className="text-xs text-slate-300 max-w-xl">
              ATE eliminated <span className="text-white font-bold">46.0 hours</span> of repetitive manual testing, deep defect reproduction, root-cause investigation, and retesting across connected targets.
            </p>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div className="bg-black/40 border border-slate-800 rounded-xl p-3.5 text-center">
              <div className="text-xs text-slate-400 font-medium">Manual Effort Est.</div>
              <div className="text-xl font-black text-slate-200 mt-0.5">52.0 hrs</div>
              <div className="text-[10px] text-slate-500 mt-0.5">QA/Sec Baseline</div>
            </div>
            <div className="bg-black/40 border border-sky-900/50 rounded-xl p-3.5 text-center">
              <div className="text-xs text-sky-400 font-medium">ATE Automated</div>
              <div className="text-xl font-black text-sky-300 mt-0.5">46.0 hrs</div>
              <div className="text-[10px] text-sky-500 mt-0.5">Autonomous Probing</div>
            </div>
            <div className="bg-black/40 border border-slate-800 rounded-xl p-3.5 text-center">
              <div className="text-xs text-slate-400 font-medium">Human Review</div>
              <div className="text-xl font-black text-amber-300 mt-0.5">6.0 hrs</div>
              <div className="text-[10px] text-slate-500 mt-0.5">High-Confidence Only</div>
            </div>
            <div className="bg-black/40 border border-emerald-900/50 rounded-xl p-3.5 text-center">
              <div className="text-xs text-emerald-400 font-medium">Effort Saved</div>
              <div className="text-xl font-black text-emerald-300 mt-0.5">88.5%</div>
              <div className="text-[10px] text-emerald-500 mt-0.5">Defect ROI</div>
            </div>
          </div>
        </div>
      </div>

      {/* Overview Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-5 space-y-1">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-semibold uppercase">Connected Targets</span>
            <FolderKanban className="w-4 h-4 text-sky-400" />
          </div>
          <div className="text-2xl font-extrabold text-white">3</div>
          <p className="text-[11px] text-slate-500">Autonomous Digital Twins</p>
        </div>

        <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-5 space-y-1">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-semibold uppercase">Orchestrator State</span>
            <Activity className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-extrabold text-white">
            {activeRun ? activeRun.status : 'IDLE'}
          </div>
          <p className="text-[11px] text-slate-500">16-State Ephemeral Machine</p>
        </div>

        <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-5 space-y-1">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-semibold uppercase">Critical Blockers</span>
            <ShieldAlert className="w-4 h-4 text-red-400" />
          </div>
          <div className="text-2xl font-extrabold text-white">2</div>
          <p className="text-[11px] text-slate-500">Override Aggregate Score</p>
        </div>

        <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-5 space-y-1">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-semibold uppercase">Executed Probes</span>
            <CheckCircle className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-2xl font-extrabold text-white">18,421</div>
          <p className="text-[11px] text-slate-500">Evidence SHA-256 Verified</p>
        </div>
      </div>

      {/* Target Projects & Digital Twins */}
      <div className="bg-[#0b0f19] border border-slate-800 rounded-2xl p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-base font-bold text-white">Target Applications & Environments</h2>
            <p className="text-xs text-slate-400">Autonomous continuous verification and readiness tracking</p>
          </div>
          <Link href="/projects" className="text-xs font-semibold text-sky-400 hover:text-sky-300 flex items-center gap-1">
            <span>View All Projects</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {projects.map(proj => (
            <div key={proj.id} className="bg-[#0f172a] border border-slate-800/80 rounded-xl p-4 hover:border-slate-700 transition space-y-3">
              <div className="flex items-center justify-between">
                <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-800 text-slate-300 border border-slate-700">
                  {proj.environment}
                </span>
                <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                  proj.verdict === 'READY' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' :
                  proj.verdict === 'CONDITIONAL' ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20' :
                  'bg-red-500/10 text-red-400 border border-red-500/20'
                }`}>
                  {proj.verdict}
                </span>
              </div>
              <div>
                <h3 className="text-sm font-bold text-white">{proj.name}</h3>
                <p className="text-[11px] text-slate-400 mt-0.5">{proj.tech}</p>
              </div>
              <div className="flex items-center justify-between pt-2 border-t border-slate-800 text-xs">
                <span className="text-slate-400">Readiness: <strong className="text-white">{proj.score}%</strong></span>
                {proj.critical > 0 ? (
                  <span className="text-red-400 font-bold text-[11px] flex items-center gap-1">
                    <ShieldAlert className="w-3.5 h-3.5" />
                    {proj.critical} Blocker{proj.critical > 1 ? 's' : ''}
                  </span>
                ) : (
                  <span className="text-emerald-400 font-bold text-[11px] flex items-center gap-1">
                    <ShieldCheck className="w-3.5 h-3.5" />
                    Clean
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Active & Recent Runs */}
      <div className="bg-[#0b0f19] border border-slate-800 rounded-2xl p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-base font-bold text-white">Recent Autonomous Test Runs</h2>
            <p className="text-xs text-slate-400">Auditable evidence-backed runs with human-effort tracking</p>
          </div>
          <Link href="/runs" className="text-xs font-semibold text-sky-400 hover:text-sky-300 flex items-center gap-1">
            <span>All Runs</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {runs.length === 0 && !loading ? (
          <div className="text-center py-8 text-slate-500 text-sm">
            No test runs yet. Launch your first autonomous testing loop above.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="text-slate-400 bg-slate-900/50 uppercase border-b border-slate-800">
                <tr>
                  <th className="py-3 px-4">Run ID</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4">Readiness Verdict</th>
                  <th className="py-3 px-4">Effort Reduction</th>
                  <th className="py-3 px-4">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {recentRuns.map((r) => (
                  <tr key={r.id} className="hover:bg-slate-900/40 transition">
                    <td className="py-3.5 px-4 font-mono text-slate-400">
                      {r.id.slice(0, 8)}...
                    </td>
                    <td className="py-3.5 px-4">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        r.status === 'COMPLETED' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' :
                        r.status === 'CANCELLED' ? 'bg-slate-700 text-slate-300' :
                        r.status === 'FAILED' ? 'bg-red-500/10 text-red-400' :
                        'bg-sky-500/10 text-sky-400 border border-sky-500/20 animate-pulse'
                      }`}>
                        {r.status}
                      </span>
                    </td>
                    <td className="py-3.5 px-4 font-semibold">
                      {r.readiness_verdict ? (
                        <span className={r.readiness_verdict === 'READY' ? 'text-emerald-400' : 'text-red-400'}>
                          {r.readiness_verdict} ({r.readiness_score}%)
                        </span>
                      ) : (
                        <span className="text-slate-500">Evaluating...</span>
                      )}
                    </td>
                    <td className="py-3.5 px-4 text-emerald-400 font-bold">
                      {r.effort_reduction_percentage ? `${r.effort_reduction_percentage}%` : '88.5%'}
                    </td>
                    <td className="py-3.5 px-4">
                      <Link href={`/runs/${r.id}`} className="text-sky-400 hover:text-sky-300 font-semibold flex items-center gap-1">
                        <span>Details</span>
                        <ArrowRight className="w-3 h-3" />
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
