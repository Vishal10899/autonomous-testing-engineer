"use client";
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../../../lib/useAuth';
import { apiFetch } from '../../../lib/api';
import { Play, Sliders, ShieldAlert, Key, Globe, Server, Check, ArrowRight } from 'lucide-react';

export default function NewTestRunWizard() {
  const { loading: authLoading } = useAuth(true);
  const router = useRouter();
  const [targetUrl, setTargetUrl] = useState('http://127.0.0.1:8002/benchmark');
  const [repoPath, setRepoPath] = useState('');
  const [environment, setEnvironment] = useState('STAGING');
  const [authType, setAuthType] = useState('Bearer Token');
  const [authToken, setAuthToken] = useState('');
  
  // Scope Checkboxes (PRD Section 20)
  const [scopes, setScopes] = useState({
    functional: true,
    api: true,
    security: true,
    performance: true,
    browser: true,
    database: true,
    reliability: true,
    ai: true,
    regression: true
  });

  // Safety Controls (PRD Section 21)
  const [maxRps, setMaxRps] = useState(1000);
  const [maxConcurrency, setMaxConcurrency] = useState(500);
  const [destructive, setDestructive] = useState(false);
  const [dbMutation, setDbMutation] = useState(false);
  const [chaos, setChaos] = useState(false);

  const [loading, setLoading] = useState(false);

  const toggleScope = (key) => {
    setScopes(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const handleStartRun = async () => {
    setLoading(true);
    try {
      const data = await apiFetch('/api/v1/runs', {
        method: 'POST',
        body: JSON.stringify({
          target_url: targetUrl,
          repo_path: repoPath,
          environment: environment,
          scopes: scopes,
          policy: { max_rps: maxRps, max_concurrency: maxConcurrency, destructive, db_mutation: dbMutation, chaos }
        })
      });
      if (data.run_id) {
        router.push(`/runs/${data.run_id}`);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 py-4">
      <div className="border-b border-slate-800 pb-4">
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <Play className="w-6 h-6 text-sky-400 fill-sky-400" />
          <span>Configure Autonomous Test Run</span>
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          Specify your application target, testing scope, authentication credentials, and safety policy caps.
        </p>
      </div>

      {/* Step 1: Target Information & Environment */}
      <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-6 space-y-4">
        <h2 className="text-sm font-semibold uppercase text-slate-400 tracking-wider">1. Application Target & Environment</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Target Base URL</label>
            <input
              type="text"
              value={targetUrl}
              onChange={(e) => setTargetUrl(e.target.value)}
              placeholder="https://staging.example.com"
              className="w-full bg-[#070a12] border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-sky-500"
            />
          </div>
          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Environment Scope</label>
            <select
              value={environment}
              onChange={(e) => setEnvironment(e.target.value)}
              className="w-full bg-[#070a12] border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-sky-500"
            >
              <option value="DEVELOPMENT">DEVELOPMENT (Local / 127.0.0.1)</option>
              <option value="STAGING">STAGING (Recommended)</option>
              <option value="PRODUCTION">PRODUCTION (Requires Safety Auth)</option>
            </select>
          </div>
        </div>
      </div>

      {/* Step 2: Target Authentication Credentials */}
      <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-6 space-y-4">
        <h2 className="text-sm font-semibold uppercase text-slate-400 tracking-wider">2. Target Authentication Settings</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Auth Type</label>
            <select
              value={authType}
              onChange={(e) => setAuthType(e.target.value)}
              className="w-full bg-[#070a12] border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-sky-500"
            >
              <option value="None">No Auth / Public Endpoint</option>
              <option value="Bearer Token">Bearer Token</option>
              <option value="API Key">API Key Header</option>
              <option value="Basic Auth">Basic Auth</option>
            </select>
          </div>
          {authType !== 'None' && (
            <div>
              <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Secret Token / Key</label>
              <input
                type="password"
                value={authToken}
                onChange={(e) => setAuthToken(e.target.value)}
                placeholder="••••••••••••••••"
                className="w-full bg-[#070a12] border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-sky-500"
              />
            </div>
          )}
        </div>
      </div>

      {/* Step 3: Testing Scope Checkboxes */}
      <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-6 space-y-4">
        <h2 className="text-sm font-semibold uppercase text-slate-400 tracking-wider">3. Autonomous Vector Testing Scope</h2>
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
          {Object.keys(scopes).map((key) => (
            <div
              key={key}
              onClick={() => toggleScope(key)}
              className={`p-3 rounded-xl border cursor-pointer flex items-center justify-between transition ${
                scopes[key] ? 'bg-sky-500/10 border-sky-500/60 text-white' : 'bg-[#070a12] border-slate-800 text-slate-400'
              }`}
            >
              <span className="text-xs font-bold capitalize">{key} Testing</span>
              <div className={`w-4 h-4 rounded flex items-center justify-center ${scopes[key] ? 'bg-sky-500 text-white' : 'border border-slate-700'}`}>
                {scopes[key] && <Check className="w-3 h-3" />}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Step 4: Safety Policy Controls */}
      <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-6 space-y-4">
        <h2 className="text-sm font-semibold uppercase text-slate-400 tracking-wider">4. Safety Policy Broker Constraints</h2>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Max RPS Limit</label>
            <input
              type="number"
              value={maxRps}
              onChange={(e) => setMaxRps(Number(e.target.value))}
              className="w-full bg-[#070a12] border border-slate-700 rounded-lg px-3 py-2 text-sm text-white"
            />
          </div>
          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Max Concurrency Limit</label>
            <input
              type="number"
              value={maxConcurrency}
              onChange={(e) => setMaxConcurrency(Number(e.target.value))}
              className="w-full bg-[#070a12] border border-slate-700 rounded-lg px-3 py-2 text-sm text-white"
            />
          </div>
        </div>
      </div>

      <button
        onClick={handleStartRun}
        disabled={loading}
        className="w-full bg-sky-600 hover:bg-sky-500 text-white font-bold py-3.5 rounded-xl transition shadow-xl shadow-sky-600/25 flex items-center justify-center gap-2 text-base"
      >
        <span>{loading ? 'Dispatching Orchestrator...' : 'Launch Autonomous Test Engine'}</span>
        <ArrowRight className="w-5 h-5" />
      </button>
    </div>
  );
}
