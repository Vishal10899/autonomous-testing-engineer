"use client";
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../../../lib/useAuth';
import { apiFetch } from '../../../lib/api';
import { FolderKanban, ArrowRight, Plus } from 'lucide-react';

export default function CreateProjectPage() {
  const { loading: authLoading } = useAuth(true);
  const router = useRouter();
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [targetUrl, setTargetUrl] = useState('http://127.0.0.1:8002/benchmark');
  const [environment, setEnvironment] = useState('STAGING');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleCreate = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const data = await apiFetch('/api/v1/projects', {
        method: 'POST',
        body: JSON.stringify({
          name,
          description,
          target_url: targetUrl,
          environment
        })
      });
      if (data.id) {
        router.push(`/projects/${data.id}`);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6 py-4">
      <div className="border-b border-slate-800 pb-4">
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <FolderKanban className="w-6 h-6 text-sky-400" />
          <span>Create New Target Project</span>
        </h1>
        <p className="text-sm text-slate-400 mt-1">Connect a target application for continuous autonomous testing.</p>
      </div>

      {error && (
        <div className="p-3 bg-red-500/10 border border-red-500/30 rounded-lg text-xs text-red-400">
          {error}
        </div>
      )}

      <form onSubmit={handleCreate} className="bg-[#0b0f19] border border-slate-800 rounded-2xl p-6 space-y-4">
        <div>
          <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Project Name</label>
          <input
            type="text"
            required
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="e.g. Sentinel AI Gateway"
            className="w-full bg-[#070a12] border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-sky-500"
          />
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Description (Optional)</label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="AI model gateway and retrieval search service..."
            rows={3}
            className="w-full bg-[#070a12] border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-sky-500"
          />
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Initial Target Base URL</label>
          <input
            type="text"
            required
            value={targetUrl}
            onChange={(e) => setTargetUrl(e.target.value)}
            placeholder="http://127.0.0.1:8002/benchmark"
            className="w-full bg-[#070a12] border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-sky-500"
          />
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Environment</label>
          <select
            value={environment}
            onChange={(e) => setEnvironment(e.target.value)}
            className="w-full bg-[#070a12] border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-sky-500"
          >
            <option value="STAGING">STAGING (Recommended)</option>
            <option value="DEVELOPMENT">DEVELOPMENT (Local 127.0.0.1)</option>
            <option value="PRODUCTION">PRODUCTION</option>
          </select>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-sky-600 hover:bg-sky-500 text-white font-bold py-3 rounded-xl transition shadow-lg shadow-sky-600/25 flex items-center justify-center gap-2 text-sm"
        >
          <span>{loading ? 'Creating Project...' : 'Create Project'}</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </form>
    </div>
  );
}
