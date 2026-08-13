"use client";
import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useAuth } from '../../lib/useAuth';
import { apiFetch } from '../../lib/api';
import { 
  Play, Plus, Activity, ShieldAlert, CheckCircle, AlertTriangle, 
  ArrowRight, Cpu, FolderKanban, Clock, RefreshCw, FileCheck 
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

  const activeRun = runs.find(r => ['EXECUTING', 'DISCOVERING', 'MODELING', 'PLANNING', 'RISK_ANALYSIS'].includes(r.status));
  const recentRuns = runs.slice(0, 5);

  const projects = [
    { id: 'proj_sentinel', name: 'Sentinel AI Gateway', environment: 'STAGING', verdict: 'NOT_READY', score: 26.7, critical: 2 },
    { id: 'proj_ecommerce', name: 'E-Commerce Transactions API', environment: 'STAGING', verdict: 'READY', score: 94.2, critical: 0 },
    { id: 'proj_support', name: 'Customer Support Bot', environment: 'DEV', verdict: 'CONDITIONAL', score: 78.5, critical: 0 }
  ];

  return (
    <div className="space-y-8">
      {/* Top Welcome Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Good morning, Vishal</h1>
          <p className="text-sm text-slate-400 mt-1">
            Workspace: <span className="font-semibold text-slate-200">Vishal Engineering</span> | Enterprise Plan
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Link
            href="/test/new"
            className="flex items-center gap-2 bg-sky-600 hover:bg-sky-500 text-white px-5 py-2.5 rounded-xl font-bold text-sm transition shadow-lg shadow-sky-600/20"
          >
            <Plus className="w-4 h-4" />
            <span>+ New Test Run</span>
          </Link>
        </div>
      </div>

      {/* Overview Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-5 space-y-1">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-semibold uppercase">Active Projects</span>
            <FolderKanban className="w-4 h-4 text-sky-400" />
          </div>
          <div className="text-2xl font-extrabold text-white">3</div>
          <p className="text-[11px] text-slate-500">Connected target apps</p>
        </div>

        <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-5 space-y-1">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-semibold uppercase">Active Orchestration</span>
            <Activity className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-extrabold text-white">
            {activeRun ? activeRun.status : 'IDLE'}
          </div>
          <p className="text-[11px] text-slate-500">State Machine Status</p>
        </div>

        <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-5 space-y-1">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-semibold uppercase">Critical Blockers</span>
            <ShieldAlert className="w-4 h-4 text-red-400" />
          </div>
          <div className="text-2xl font-extrabold text-white">2</div>
          <p className="text-[11px] text-slate-500">Evidence-backed findings</p>
        </div>

        <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-5 space-y-1">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-semibold uppercase">Executed Probes</span>
            <CheckCircle className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-2xl font-extrabold text-white">18,421</div>
          <p className="text-[11px] text-slate-500">This billing period</p>
        </div>
      </div>

      {/* Recent Projects Table */}
      <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-6 space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-base font-bold text-white">Project Production Status</h2>
          <Link href="/projects" className="text-xs font-semibold text-sky-400 hover:underline flex items-center gap-1">
            <span>View All Projects</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="text-xs font-semibold text-slate-400 uppercase bg-slate-900/60 border-b border-slate-800">
              <tr>
                <th className="px-4 py-3">Project Name</th>
                <th className="px-4 py-3">Environment</th>
                <th className="px-4 py-3">Readiness Score</th>
                <th className="px-4 py-3">Verdict</th>
                <th className="px-4 py-3">Blockers</th>
                <th className="px-4 py-3">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/80">
              {projects.map((p) => (
                <tr key={p.id} className="hover:bg-slate-900/40">
                  <td className="px-4 py-3.5 font-bold text-white">{p.name}</td>
                  <td className="px-4 py-3.5">
                    <span className="text-xs font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300">
                      {p.environment}
                    </span>
                  </td>
                  <td className="px-4 py-3.5 font-mono text-slate-200">{p.score}%</td>
                  <td className="px-4 py-3.5">
                    <span className={`text-xs font-bold px-2.5 py-1 rounded ${
                      p.verdict === 'READY' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' :
                      p.verdict === 'CONDITIONAL' ? 'bg-amber-500/20 text-amber-400' :
                      'bg-red-500/20 text-red-400 border border-red-500/30'
                    }`}>
                      {p.verdict}
                    </span>
                  </td>
                  <td className="px-4 py-3.5 text-slate-400">{p.critical} Critical</td>
                  <td className="px-4 py-3.5">
                    <Link href={`/runs`} className="text-xs font-semibold text-sky-400 hover:underline">
                      View Runs
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
