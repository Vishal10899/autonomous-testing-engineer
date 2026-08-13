"use client";
import { ShieldCheck, ShieldAlert, Key, Lock, AlertTriangle, Bug } from 'lucide-react';

export default function SecurityDashboardPage() {
  const securityFindings = [
    { title: 'BOLA / IDOR Authorization Bypass', endpoint: '/api/v1/user/profile', severity: 'CRITICAL', status: 'CONFIRMED' },
    { title: 'SQL Injection Vulnerability', endpoint: '/api/v1/products/search', severity: 'CRITICAL', status: 'CONFIRMED' }
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <ShieldCheck className="w-6 h-6 text-red-400" />
            <span>Security & Vulnerability Dashboard</span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            OWASP security probes, BOLA authorization, SQL injection, and secret exposure analysis (PRD Section 29).
          </p>
        </div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-5 space-y-1">
          <span className="text-xs font-semibold uppercase text-slate-400">Critical Vulnerabilities</span>
          <div className="text-2xl font-black text-red-400">2</div>
        </div>
        <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-5 space-y-1">
          <span className="text-xs font-semibold uppercase text-slate-400">High Severity</span>
          <div className="text-2xl font-black text-amber-400">0</div>
        </div>
        <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-5 space-y-1">
          <span className="text-xs font-semibold uppercase text-slate-400">Medium Severity</span>
          <div className="text-2xl font-black text-white">0</div>
        </div>
        <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-5 space-y-1">
          <span className="text-xs font-semibold uppercase text-slate-400">Security Score</span>
          <div className="text-2xl font-black text-red-400">25.0%</div>
        </div>
      </div>

      <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-6 space-y-4">
        <h2 className="text-sm font-semibold uppercase text-slate-400 tracking-wider">Active Security Vulnerabilities</h2>
        <div className="space-y-3">
          {securityFindings.map((f) => (
            <div key={f.title} className="p-4 rounded-xl border border-slate-800 bg-slate-900/60 flex items-center justify-between">
              <div>
                <div className="text-sm font-bold text-white">{f.title}</div>
                <div className="text-xs font-mono text-sky-400 mt-1">{f.endpoint}</div>
              </div>
              <span className="text-xs font-bold px-2.5 py-1 rounded bg-red-500/20 text-red-400 border border-red-500/30">
                {f.severity}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
