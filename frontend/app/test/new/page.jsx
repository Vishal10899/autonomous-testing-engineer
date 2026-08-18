"use client";
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../../../lib/useAuth';
import { apiFetch } from '../../../lib/api';
import { 
  Play, Sliders, ShieldAlert, Key, Globe, Server, Check, ArrowRight, 
  Sparkles, Layers, ShieldCheck, Cpu, Terminal, CheckCircle2
} from 'lucide-react';

export default function NewTestRunWizard() {
  const { loading: authLoading } = useAuth(true);
  const router = useRouter();
  
  // 10-Step Wizard State (PRD v8.0 Section 53)
  const [currentStep, setCurrentStep] = useState(1);
  const [onboardingMode, setOnboardingMode] = useState('URL'); // URL, OPENAPI, REPO, DOCKER, ENVIRONMENT
  const [targetUrl, setTargetUrl] = useState('http://127.0.0.1:8000');
  const [repoPath, setRepoPath] = useState('benchmark');
  const [environment, setEnvironment] = useState('STAGING');
  const [authorizedDomains, setAuthorizedDomains] = useState('127.0.0.1, localhost');
  const [authType, setAuthType] = useState('Bearer Token');
  const [authToken, setAuthToken] = useState('');
  const [policyLevel, setPolicyLevel] = useState('STANDARD'); // SAFE, STANDARD, DEEP, PRODUCTION
  
  // Scopes (Auto-select default for Autonomous Mode)
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

  // Budget (PRD Section 41)
  const [maxRps, setMaxRps] = useState(1000);
  const [maxConcurrency, setMaxConcurrency] = useState(500);
  const [maxDurationSecs, setMaxDurationSecs] = useState(3600);
  const [maxRequests, setMaxRequests] = useState(100000);

  const [loading, setLoading] = useState(false);

  const toggleScope = (key) => {
    setScopes(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const handleStartAutonomousRun = async () => {
    setLoading(true);
    try {
      const data = await apiFetch('/api/v1/runs', {
        method: 'POST',
        body: JSON.stringify({
          target_url: targetUrl,
          repo_path: repoPath,
          onboarding_mode: onboardingMode,
          environment: environment,
          scopes: scopes,
          policy_level: policyLevel,
          test_budget: {
            max_rps: maxRps,
            max_concurrency: maxConcurrency,
            max_duration_seconds: maxDurationSecs,
            max_requests: maxRequests
          }
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

  const stepsList = [
    { num: 1, name: 'Target' },
    { num: 2, name: 'Environment' },
    { num: 3, name: 'Authorization' },
    { num: 4, name: 'Auth' },
    { num: 5, name: 'Context' },
    { num: 6, name: 'Scope' },
    { num: 7, name: 'Policy' },
    { num: 8, name: 'Budget' },
    { num: 9, name: 'Review' },
    { num: 10, name: 'Launch' }
  ];

  return (
    <div className="max-w-4xl mx-auto space-y-8 py-4">
      {/* Header */}
      <div className="border-b border-slate-800 pb-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-sky-400" />
            <span>New Autonomous Test Run</span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Master 10-Step Wizard — Auto-select defaults configured for autonomous execution
          </p>
        </div>
        <button
          onClick={handleStartAutonomousRun}
          disabled={loading}
          className="flex items-center justify-center gap-2 bg-gradient-to-r from-sky-600 to-indigo-600 hover:from-sky-500 hover:to-indigo-500 text-white px-5 py-2.5 rounded-xl font-bold text-sm shadow-lg shadow-sky-600/20 transition disabled:opacity-50"
        >
          {loading ? 'Launching Orchestrator...' : 'Start Autonomous Testing'}
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>

      {/* 10-Step Stepper Progress */}
      <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-4 overflow-x-auto">
        <div className="flex items-center justify-between min-w-[650px] gap-2">
          {stepsList.map((s) => (
            <div 
              key={s.num}
              onClick={() => setCurrentStep(s.num)}
              className={`flex items-center gap-1.5 cursor-pointer text-xs font-semibold px-2.5 py-1.5 rounded-lg transition ${
                currentStep === s.num 
                  ? 'bg-sky-600 text-white' 
                  : currentStep > s.num
                  ? 'text-emerald-400 bg-emerald-500/10'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <span className="w-5 h-5 rounded-full flex items-center justify-center bg-black/30 text-[10px]">
                {s.num}
              </span>
              <span>{s.name}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Wizard Steps Form */}
      <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-6 space-y-6">
        
        {/* Step 1: Onboarding Mode & Target */}
        <div className="space-y-4">
          <div className="flex items-center gap-2 text-sm font-bold text-white uppercase tracking-wider">
            <Globe className="w-4 h-4 text-sky-400" />
            <span>1. Onboarding Mode & Target (PRD v8.0 Section 6)</span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-5 gap-2">
            {['URL', 'OPENAPI', 'REPO', 'DOCKER', 'ENVIRONMENT'].map((mode) => (
              <button
                key={mode}
                type="button"
                onClick={() => setOnboardingMode(mode)}
                className={`py-2 px-3 rounded-lg text-xs font-bold border transition ${
                  onboardingMode === mode 
                    ? 'bg-sky-500/20 text-sky-300 border-sky-500/50' 
                    : 'bg-[#0f172a] text-slate-400 border-slate-800 hover:border-slate-700'
                }`}
              >
                {mode}
              </button>
            ))}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
            <div>
              <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Target Base URL</label>
              <input
                type="text"
                value={targetUrl}
                onChange={(e) => setTargetUrl(e.target.value)}
                placeholder="http://127.0.0.1:8000"
                className="w-full bg-[#070a12] border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-sky-500"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Repository Path (Optional)</label>
              <input
                type="text"
                value={repoPath}
                onChange={(e) => setRepoPath(e.target.value)}
                placeholder="e.g. benchmark or path/to/repo"
                className="w-full bg-[#070a12] border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-sky-500"
              />
            </div>
          </div>
        </div>

        {/* Step 2 & 3: Environment & Scope Authorization */}
        <div className="border-t border-slate-800 pt-6 space-y-4">
          <div className="flex items-center gap-2 text-sm font-bold text-white uppercase tracking-wider">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            <span>2 & 3. Environment & Scope Authorization (PRD Section 7 & 8)</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Environment</label>
              <select
                value={environment}
                onChange={(e) => setEnvironment(e.target.value)}
                className="w-full bg-[#070a12] border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-sky-500"
              >
                <option value="DEV">DEV (Local / Sandbox)</option>
                <option value="TEST">TEST (CI/CD Pipeline)</option>
                <option value="STAGING">STAGING (Pre-Production)</option>
                <option value="PRODUCTION">PRODUCTION (Strict Restrictions)</option>
              </select>
            </div>
            <div className="md:col-span-2">
              <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Authorized Domains & IP Ranges</label>
              <input
                type="text"
                value={authorizedDomains}
                onChange={(e) => setAuthorizedDomains(e.target.value)}
                placeholder="127.0.0.1, localhost, staging.internal"
                className="w-full bg-[#070a12] border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-sky-500"
              />
            </div>
          </div>
        </div>

        {/* Step 6: Testing Scope Auto-Selection */}
        <div className="border-t border-slate-800 pt-6 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-sm font-bold text-white uppercase tracking-wider">
              <Layers className="w-4 h-4 text-purple-400" />
              <span>6. Testing Scope Spectrum (PRD Section 16)</span>
            </div>
            <span className="text-[11px] font-bold text-sky-400">All Scopes Enabled (Autonomous Mode)</span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
            {Object.keys(scopes).map((k) => (
              <label key={k} className="flex items-center gap-2.5 bg-[#0f172a] border border-slate-800 p-3 rounded-lg cursor-pointer hover:border-slate-700">
                <input
                  type="checkbox"
                  checked={scopes[k]}
                  onChange={() => toggleScope(k)}
                  className="rounded bg-slate-900 border-slate-700 text-sky-600 focus:ring-0 w-4 h-4"
                />
                <span className="text-xs font-bold text-slate-200 capitalize">{k}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Step 7 & 8: Safety Policy & Test Budget */}
        <div className="border-t border-slate-800 pt-6 space-y-4">
          <div className="flex items-center gap-2 text-sm font-bold text-white uppercase tracking-wider">
            <Sliders className="w-4 h-4 text-amber-400" />
            <span>7 & 8. Safety Broker Policy & Test Budget (PRD Section 38 & 41)</span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div>
              <label className="block text-xs text-slate-400 font-semibold mb-1">Policy Preset</label>
              <select
                value={policyLevel}
                onChange={(e) => setPolicyLevel(e.target.value)}
                className="w-full bg-[#070a12] border border-slate-700 rounded-lg px-3 py-2 text-xs text-white"
              >
                <option value="STANDARD">STANDARD (1000 RPS)</option>
                <option value="SAFE">SAFE (50 RPS)</option>
                <option value="DEEP">DEEP (2000 RPS)</option>
                <option value="PRODUCTION">PRODUCTION (Safe)</option>
              </select>
            </div>
            <div>
              <label className="block text-xs text-slate-400 font-semibold mb-1">Max RPS</label>
              <input
                type="number"
                value={maxRps}
                onChange={(e) => setMaxRps(Number(e.target.value))}
                className="w-full bg-[#070a12] border border-slate-700 rounded-lg px-3 py-2 text-xs text-white"
              />
            </div>
            <div>
              <label className="block text-xs text-slate-400 font-semibold mb-1">Max Concurrency</label>
              <input
                type="number"
                value={maxConcurrency}
                onChange={(e) => setMaxConcurrency(Number(e.target.value))}
                className="w-full bg-[#070a12] border border-slate-700 rounded-lg px-3 py-2 text-xs text-white"
              />
            </div>
            <div>
              <label className="block text-xs text-slate-400 font-semibold mb-1">Max Duration</label>
              <input
                type="number"
                value={maxDurationSecs}
                onChange={(e) => setMaxDurationSecs(Number(e.target.value))}
                className="w-full bg-[#070a12] border border-slate-700 rounded-lg px-3 py-2 text-xs text-white"
              />
            </div>
          </div>
        </div>

        {/* Step 10: Launch CTA */}
        <div className="border-t border-slate-800 pt-6 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="text-xs text-slate-400">
            Clicking <strong className="text-white">Start Autonomous Testing</strong> will initialize the isolated sandbox, explore the target attack surface, execute tests within policy, validate findings with cryptographic SHA-256 evidence, and compute readiness.
          </div>
          <button
            onClick={handleStartAutonomousRun}
            disabled={loading}
            className="w-full sm:w-auto flex items-center justify-center gap-2 bg-gradient-to-r from-sky-600 to-indigo-600 hover:from-sky-500 hover:to-indigo-500 text-white px-8 py-3.5 rounded-xl font-extrabold text-sm shadow-xl shadow-sky-600/30 transition disabled:opacity-50"
          >
            {loading ? 'Initializing Pipeline...' : 'Start Autonomous Testing'}
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>

      </div>
    </div>
  );
}
