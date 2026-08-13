"use client";
import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useAuth } from '../../lib/useAuth';
import { apiFetch } from '../../lib/api';
import { FolderKanban, Plus, Play, ShieldAlert, CheckCircle, ArrowRight, RefreshCw } from 'lucide-react';

export default function ProjectsPage() {
  const { loading: authLoading } = useAuth(true);
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchProjects = async () => {
    try {
      const data = await apiFetch('/api/v1/projects');
      setProjects(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  if (authLoading || loading) {
    return (
      <div className="flex items-center justify-center py-20 text-slate-400 gap-2">
        <RefreshCw className="w-5 h-5 animate-spin text-sky-400" />
        <span>Loading projects...</span>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <FolderKanban className="w-6 h-6 text-sky-400" />
            <span>Target Projects</span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Manage target applications, environments, autonomous test runs, and readiness decisions.
          </p>
        </div>
        <Link
          href="/projects/new"
          className="flex items-center gap-2 bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs px-4 py-2.5 rounded-lg transition shadow-md shadow-sky-600/20"
        >
          <Plus className="w-4 h-4" />
          <span>+ Create Project</span>
        </Link>
      </div>

      {error && (
        <div className="p-4 bg-red-500/10 border border-red-500/30 rounded-xl text-xs text-red-400">
          {error}
        </div>
      )}

      {projects.length === 0 ? (
        <div className="bg-[#0b0f19] border border-slate-800 rounded-2xl p-12 text-center space-y-4">
          <FolderKanban className="w-12 h-12 text-slate-600 mx-auto" />
          <h2 className="text-lg font-bold text-white">No projects yet</h2>
          <p className="text-xs text-slate-400 max-w-sm mx-auto">
            Create your first target project to begin autonomous discovery, risk analysis, and testing.
          </p>
          <Link
            href="/projects/new"
            className="inline-flex items-center gap-2 bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs px-5 py-2.5 rounded-xl transition shadow-lg shadow-sky-600/20"
          >
            <Plus className="w-4 h-4" />
            <span>Create your first project</span>
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map((p) => (
            <div key={p.id} className="bg-[#0b0f19] border border-slate-800 hover:border-sky-500/50 rounded-xl p-6 space-y-4 transition flex flex-col justify-between">
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300">STAGING</span>
                  <span className="text-xs font-bold px-2 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30">
                    NOT READY
                  </span>
                </div>
                <h3 className="text-lg font-bold text-white">{p.name}</h3>
                <p className="text-xs text-slate-400 line-clamp-2">{p.description || 'No description provided.'}</p>
              </div>

              <div className="pt-4 border-t border-slate-800/80 flex items-center justify-between text-xs">
                <span className="text-slate-500 font-mono">Created {new Date(p.created_at).toLocaleDateString()}</span>
                <Link href={`/projects/${p.id}`} className="font-semibold text-sky-400 hover:underline flex items-center gap-1">
                  <span>Open Project</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
