"use client";
import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { useAuth } from '../../../lib/useAuth';
import { apiFetch } from '../../../lib/api';
import { Play, CheckCircle, Square, ShieldAlert, Cpu, Terminal, RefreshCw, FileCheck } from 'lucide-react';

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
    { name: 'Risk Analysis', key: 'RISK_ANALYSIS' },
    { name: 'Planning', key: 'PLANNING' },
    { name: 'Execution', key: 'EXECUTING' },
    { name: 'Observation', key: 'OBSERVING' },
    { name: 'Reproduction', key: 'REPRODUCING' },
    { name: 'RCA', key: 'INVESTIGATING' },
    { name: 'Readiness', key: 'COMPLETED' }
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
            <span className="text-xs text-slate-400 font-mono">Target: Target System Under Test</span>
          </div>
          <h1 className="text-xl font-bold text-white mt-2">Autonomous Execution Live Pipeline</h1>
        </div>

        <div className="flex items-center gap-3">
          {run && ['EXECUTING', 'DISCOVERING', 'MODELING', 'PLANNING'].includes(run.status) && (
            <button
              onClick={handleKill}
              className="flex items-center gap-2 bg-red-600/20 hover:bg-red-600/30 text-red-400 border border-red-500/40 px-4 py-2 rounded-lg font-medium text-xs transition"
            >
              <Square className="w-4 h-4" />
              <span>Emergency Kill Switch</span>
            </button>
          )}
        </div>
      </div>

      {/* Live Pipeline Progress Indicator (PRD Section 23) */}
      <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-6 space-y-4">
        <h2 className="text-xs font-semibold uppercase text-slate-400 tracking-wider">State Machine Orchestration Pipeline</h2>
        <div className="grid grid-cols-3 sm:grid-cols-9 gap-2">
          {pipelineStages.map((s, idx) => {
            const isCurrent = run?.status === s.key;
            return (
              <div
                key={s.name}
                className={`p-3 rounded-xl border text-center transition ${
                  isCurrent
                    ? 'bg-sky-500/20 border-sky-500 text-sky-300 font-bold shadow-lg shadow-sky-500/10'
                    : 'bg-slate-900/60 border-slate-800 text-slate-400'
                }`}
              >
                <div className="text-[10px] font-mono text-slate-500">STAGE 0{idx+1}</div>
                <div className="text-xs font-semibold mt-1">{s.name}</div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Live Findings Grid */}
      <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-6 space-y-4">
        <h2 className="text-sm font-bold text-white">Confirmed Findings in This Run ({findings.length})</h2>
        <div className="space-y-3">
          {findings.map((f) => (
            <div key={f.id} className="p-4 rounded-xl border border-slate-800 bg-slate-900/60 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold bg-red-500/20 text-red-400 border border-red-500/30 px-2 py-0.5 rounded">
                  {f.severity}
                </span>
                <span className="text-xs font-mono text-slate-400">Reproduction: {f.reproduction_rate}</span>
              </div>
              <div className="text-sm font-bold text-white">{f.title}</div>
              <div className="text-xs font-mono text-sky-400">{f.affected_endpoint}</div>
              <p className="text-xs text-slate-300 bg-[#070a12] p-3 rounded-lg border border-slate-800">{f.root_cause}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
