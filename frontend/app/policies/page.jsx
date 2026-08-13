"use client";
import { useState } from 'react';
import { Sliders, Shield, AlertTriangle, Check } from 'lucide-react';

export default function PolicyEnginePage() {
  const [maxRps, setMaxRps] = useState(1000);
  const [maxConcurrency, setMaxConcurrency] = useState(500);
  const [destructive, setDestructive] = useState(false);
  const [dbMutation, setDbMutation] = useState(false);
  const [chaos, setChaos] = useState(false);
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between border-b border-gray-800 pb-4">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <Sliders className="w-6 h-6 text-sky-400" />
            <span>Deterministic Policy & Safety Broker</span>
          </h1>
          <p className="text-sm text-gray-400 mt-1">
            Enforces strict environment limits (PRD Section 2.2). AI proposed actions are validated against this policy before execution.
          </p>
        </div>
      </div>

      <div className="bg-[#111827] border border-gray-800 rounded-xl p-6 space-y-6 max-w-3xl">
        <h2 className="text-sm font-semibold uppercase text-gray-400 tracking-wider">Safety Policy Parameters</h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div>
            <label className="block text-xs font-semibold text-gray-400 uppercase mb-1">Max RPS Cap</label>
            <input
              type="number"
              value={maxRps}
              onChange={(e) => setMaxRps(Number(e.target.value))}
              className="w-full bg-[#090d16] border border-gray-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-sky-500"
            />
          </div>
          <div>
            <label className="block text-xs font-semibold text-gray-400 uppercase mb-1">Max Concurrency Cap</label>
            <input
              type="number"
              value={maxConcurrency}
              onChange={(e) => setMaxConcurrency(Number(e.target.value))}
              className="w-full bg-[#090d16] border border-gray-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-sky-500"
            />
          </div>
        </div>

        <div className="space-y-4 pt-4 border-t border-gray-800">
          <div className="flex items-center justify-between p-4 bg-[#0c121e] border border-gray-800 rounded-xl">
            <div>
              <div className="text-sm font-bold text-white">Destructive Tests</div>
              <div className="text-xs text-gray-400">Allows payloads that modify system state or purge resources.</div>
            </div>
            <input
              type="checkbox"
              checked={destructive}
              onChange={(e) => setDestructive(e.target.checked)}
              className="w-5 h-5 accent-sky-500 rounded"
            />
          </div>

          <div className="flex items-center justify-between p-4 bg-[#0c121e] border border-gray-800 rounded-xl">
            <div>
              <div className="text-sm font-bold text-white">Database Mutation</div>
              <div className="text-xs text-gray-400">Allows writing temporary records directly into connected databases.</div>
            </div>
            <input
              type="checkbox"
              checked={dbMutation}
              onChange={(e) => setDbMutation(e.target.checked)}
              className="w-5 h-5 accent-sky-500 rounded"
            />
          </div>

          <div className="flex items-center justify-between p-4 bg-[#0c121e] border border-gray-800 rounded-xl">
            <div>
              <div className="text-sm font-bold text-white">Chaos & Fault Injection</div>
              <div className="text-xs text-gray-400">Injects artificial delays, circuit breaker triggers, and packet drops.</div>
            </div>
            <input
              type="checkbox"
              checked={chaos}
              onChange={(e) => setChaos(e.target.checked)}
              className="w-5 h-5 accent-sky-500 rounded"
            />
          </div>
        </div>

        <button
          onClick={handleSave}
          className="flex items-center gap-2 bg-sky-600 hover:bg-sky-500 text-white px-5 py-2 rounded-lg font-medium transition shadow-lg shadow-sky-600/20"
        >
          {saved ? <Check className="w-4 h-4" /> : null}
          <span>{saved ? 'Policy Saved' : 'Save Safety Policy'}</span>
        </button>
      </div>
    </div>
  );
}
