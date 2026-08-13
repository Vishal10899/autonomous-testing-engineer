"use client";
import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useAuth } from '../../lib/useAuth';
import { apiFetch } from '../../lib/api';
import { Play, CheckCircle, XCircle, Clock, ShieldAlert, Filter, Plus, RefreshCw } from 'lucide-react';

export default function TestRunHistoryPage() {
  const { loading: authLoading } = useAuth(true);
  const [runs, setRuns] = useState([]);
  const [filter, setFilter] = useState('ALL');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiFetch('/api/v1/runs')
      .then(data => setRuns(data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const filteredRuns = runs.filter(r => {
    if (filter === 'RUNNING') return ['EXECUTING', 'DISCOVERING', 'MODELING', 'PLANNING', 'RISK_ANALYSIS'].includes(r.status);
    if (filter === 'COMPLETED') return r.status === 'COMPLETED';
    if (filter === 'CANCELLED') return r.status === 'CANCELLED';
    return true;
  });

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <Play className="w-6 h-6 text-sky-400 fill-sky-400" />
            <span>Autonomous Test Runs</span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Complete history of state machine orchestration runs and evidence-backed production readiness decisions.
          </p>
        </div>
        <Link
          href="/test/new"
          className="flex items-center gap-2 bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs px-4 py-2 rounded-lg transition shadow-md shadow-sky-600/20"
        >
          <Plus className="w-4 h-4" />
          <span>+ New Test Run</span>
        </Link>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center space-x-2 border-b border-slate-800/80 pb-3 text-xs font-semibold">
        {['ALL', 'RUNNING', 'COMPLETED', 'CANCELLED'].map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`px-3 py-1.5 rounded-lg transition ${
              filter === f ? 'bg-sky-500/20 text-sky-400 border border-sky-500/40' : 'text-slate-400 hover:bg-slate-800'
            }`}
          >
            {f}
          </button>
        ))}
      </div>

      {/* Runs Table */}
      <div className="bg-[#0b0f19] border border-slate-800 rounded-xl overflow-hidden shadow-xl">
        <table className="w-full text-left text-sm text-slate-300">
          <thead className="text-xs font-semibold text-slate-400 uppercase bg-slate-900/60 border-b border-slate-800">
            <tr>
              <th className="px-4 py-3">Run ID</th>
              <th className="px-4 py-3">Status</th>
              <th className="px-4 py-3">Readiness Verdict</th>
              <th className="px-4 py-3">Score</th>
              <th className="px-4 py-3">Created At</th>
              <th className="px-4 py-3">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/80">
            {filteredRuns.map((r) => (
              <tr key={r.id} className="hover:bg-slate-900/40">
                <td className="px-4 py-3.5 font-mono text-sky-400 font-bold">{r.id.slice(0, 12)}...</td>
                <td className="px-4 py-3.5">
                  <span className="text-xs font-mono font-bold px-2 py-0.5 rounded bg-slate-800 text-slate-300">
                    {r.status}
                  </span>
                </td>
                <td className="px-4 py-3.5">
                  <span className={`text-xs font-bold px-2.5 py-1 rounded ${
                    r.readiness_verdict === 'READY' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' :
                    r.readiness_verdict === 'CONDITIONAL' ? 'bg-amber-500/20 text-amber-400' :
                    r.readiness_verdict === 'NOT_READY' ? 'bg-red-500/20 text-red-400 border border-red-500/30' :
                    'bg-slate-800 text-slate-400'
                  }`}>
                    {r.readiness_verdict || 'PENDING'}
                  </span>
                </td>
                <td className="px-4 py-3.5 font-mono">
                  {r.readiness_score !== null ? `${r.readiness_score}%` : '—'}
                </td>
                <td className="px-4 py-3.5 text-xs text-slate-400 font-mono">
                  {new Date(r.created_at).toLocaleTimeString()}
                </td>
                <td className="px-4 py-3.5">
                  <Link href={`/runs/${r.id}`} className="text-xs font-semibold text-sky-400 hover:underline">
                    View Live Pipeline
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
