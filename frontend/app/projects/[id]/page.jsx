"use client";
import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '../../../lib/useAuth';
import { apiFetch } from '../../../lib/api';
import { FolderKanban, Play, ShieldAlert, CheckCircle, Clock, Plus, RefreshCw, Network } from 'lucide-react';

export default function ProjectDetailPage() {
  const { loading: authLoading } = useAuth(true);
  const params = useParams();
  const projectId = params?.id;

  const [project, setProject] = useState(null);
  const [runs, setRuns] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!projectId) return;

    Promise.all([
      apiFetch(`/api/v1/projects/${projectId}`).catch(() => null),
      apiFetch('/api/v1/runs').catch(() => [])
    ]).then(([projData, runsData]) => {
      if (projData) setProject(projData);
      setRuns(runsData);
      setLoading(false);
    });
  }, [projectId]);

  if (authLoading || loading) {
    return (
      <div className="flex items-center justify-center py-20 text-slate-400 gap-2">
        <RefreshCw className="w-5 h-5 animate-spin text-sky-400" />
        <span>Loading project details...</span>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-mono font-bold px-2 py-0.5 rounded bg-slate-800 text-slate-300">STAGING</span>
            <span className="text-xs font-mono text-slate-400">ID: {projectId?.slice(0, 10)}...</span>
          </div>
          <h1 className="text-2xl font-bold text-white mt-1">{project?.name || 'Target Project'}</h1>
          <p className="text-sm text-slate-400 mt-1">{project?.description || 'No description provided.'}</p>
        </div>

        <Link
          href="/test/new"
          className="flex items-center gap-2 bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs px-4 py-2.5 rounded-lg transition shadow-md shadow-sky-600/20"
        >
          <Play className="w-4 h-4 fill-white" />
          <span>+ New Test Run</span>
        </Link>
      </div>

      {/* Project Status Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-5">
          <span className="text-xs font-semibold text-slate-400 uppercase">Readiness Verdict</span>
          <div className="text-xl font-extrabold text-red-400 mt-1">NOT READY</div>
          <span className="text-xs text-slate-500">2 Critical Blockers</span>
        </div>
        <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-5">
          <span className="text-xs font-semibold text-slate-400 uppercase">Readiness Score</span>
          <div className="text-xl font-extrabold text-white mt-1">26.7%</div>
          <span className="text-xs text-slate-500">Domain Weighted</span>
        </div>
        <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-5">
          <span className="text-xs font-semibold text-slate-400 uppercase">Total Runs Executed</span>
          <div className="text-xl font-extrabold text-white mt-1">{runs.length}</div>
          <span className="text-xs text-slate-500">Orchestrator Executions</span>
        </div>
      </div>

      {/* Runs History Table */}
      <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-6 space-y-4">
        <h2 className="text-base font-bold text-white">Project Test Runs History</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="text-xs font-semibold text-slate-400 uppercase bg-slate-900/60 border-b border-slate-800">
              <tr>
                <th className="px-4 py-3">Run ID</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">Verdict</th>
                <th className="px-4 py-3">Score</th>
                <th className="px-4 py-3">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/80">
              {runs.map((r) => (
                <tr key={r.id} className="hover:bg-slate-900/40">
                  <td className="px-4 py-3 font-mono text-sky-400">{r.id.slice(0, 12)}...</td>
                  <td className="px-4 py-3 font-mono font-bold text-slate-200">{r.status}</td>
                  <td className="px-4 py-3 text-red-400 font-bold">{r.readiness_verdict || 'PENDING'}</td>
                  <td className="px-4 py-3 font-mono">{r.readiness_score !== null ? `${r.readiness_score}%` : '—'}</td>
                  <td className="px-4 py-3">
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
    </div>
  );
}
