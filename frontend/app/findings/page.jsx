"use client";
import { useState, useEffect } from 'react';
import { ShieldAlert, FileCode, CheckCircle, AlertTriangle, Key, Terminal, Copy } from 'lucide-react';

export default function FindingsPage() {
  const [findings, setFindings] = useState([]);
  const [selectedFinding, setSelectedFinding] = useState(null);

  useEffect(() => {
    // Default demonstration findings from engine
    const demoFindings = [
      {
        id: 'find_1',
        title: 'BOLA / IDOR Authorization Bypass',
        severity: 'CRITICAL',
        status: 'CONFIRMED',
        affected_endpoint: '/api/v1/user/profile',
        symptom: 'Endpoint returns sensitive user profile & SSN for unauthorized token.',
        root_cause: 'Missing endpoint authorization check (Broken Object Level Authorization).',
        rca_confidence: 'DIRECTLY_OBSERVED',
        business_impact: {
          technical_impact: 'Unauthorized data access',
          user_impact: 'Critical user data exposure & privacy breach',
          financial_impact: 'High regulatory fine risk',
          security_impact: 'CRITICAL'
        },
        remediation: 'Enforce user role and ownership verification middleware on resource access.',
        reproduction_rate: '10/10 attempts',
        repro_script: `import requests\n\nres = requests.get("http://127.0.0.1:8002/benchmark/api/v1/user/profile", headers={"Authorization": "Bearer invalid_unauthorized_token"})\nprint("Status:", res.status_code)\nprint("Leaked Body:", res.text)`
      },
      {
        id: 'find_2',
        title: 'SQL Injection Vulnerability',
        severity: 'CRITICAL',
        status: 'CONFIRMED',
        affected_endpoint: '/api/v1/products/search',
        symptom: 'Raw SQL syntax error leaked in HTTP response upon injecting quotes.',
        root_cause: 'Unsanitized dynamic database query constructing SQL from raw HTTP parameters.',
        rca_confidence: 'DIRECTLY_OBSERVED',
        business_impact: {
          technical_impact: 'Full database extraction',
          user_impact: 'Account compromise',
          financial_impact: 'High',
          security_impact: 'CRITICAL'
        },
        remediation: 'Use parameterized SQL queries or ORM prepared statements.',
        reproduction_rate: '10/10 attempts',
        repro_script: `import requests\n\nres = requests.get("http://127.0.0.1:8002/benchmark/api/v1/products/search?query=' OR '1'='1")\nprint("Status:", res.status_code)\nprint("Response:", res.text)`
      },
      {
        id: 'find_3',
        title: 'Duplicate Checkout Transaction Race Condition',
        severity: 'CRITICAL',
        status: 'CONFIRMED',
        affected_endpoint: '/api/v1/checkout',
        symptom: '10 parallel concurrent requests resulted in multiple balance deductions.',
        root_cause: 'Missing database transaction isolation / missing unique idempotency key lock.',
        rca_confidence: 'STRONGLY_INFERRED',
        business_impact: {
          technical_impact: 'State corruption',
          user_impact: 'Duplicate account debiting',
          financial_impact: 'Direct financial discrepancy',
          security_impact: 'HIGH'
        },
        remediation: 'Implement Redis distributed locks (Redlock) or SELECT FOR UPDATE transaction locks.',
        reproduction_rate: '10/10 attempts',
        repro_script: `import asyncio, httpx\n\nasync function test_race() {\n  // 10 concurrent requests to checkout\n}`
      }
    ];
    setFindings(demoFindings);
    setSelectedFinding(demoFindings[0]);
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between border-b border-gray-800 pb-4">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <ShieldAlert className="w-6 h-6 text-red-400" />
            <span>Findings & Reproducible Evidence</span>
          </h1>
          <p className="text-sm text-gray-400 mt-1">
            Confirmed defects with evidence integrity hashes, root cause analysis, and standalone reproduction scripts.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Findings List */}
        <div className="bg-[#111827] border border-gray-800 rounded-xl p-4 space-y-3">
          <h2 className="text-xs font-semibold uppercase text-gray-400 px-2">Confirmed Findings ({findings.length})</h2>
          {findings.map((f) => (
            <div
              key={f.id}
              onClick={() => setSelectedFinding(f)}
              className={`p-4 rounded-xl border cursor-pointer transition ${
                selectedFinding?.id === f.id
                  ? 'bg-sky-500/10 border-sky-500 text-white'
                  : 'bg-[#0c121e] border-gray-800 hover:border-gray-700 text-gray-300'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold px-2 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30">
                  {f.severity}
                </span>
                <span className="text-xs text-emerald-400 font-medium">{f.status}</span>
              </div>
              <div className="text-sm font-bold mt-2">{f.title}</div>
              <div className="text-xs text-gray-400 font-mono mt-1">{f.affected_endpoint}</div>
            </div>
          ))}
        </div>

        {/* Finding Detail & Evidence Viewer */}
        <div className="lg:col-span-2 bg-[#111827] border border-gray-800 rounded-xl p-6 space-y-6">
          {selectedFinding ? (
            <div className="space-y-6">
              <div>
                <div className="flex items-center gap-3">
                  <span className="text-xs font-bold px-2.5 py-1 rounded bg-red-500/20 text-red-400 border border-red-500/30">
                    {selectedFinding.severity}
                  </span>
                  <span className="text-xs font-semibold px-2.5 py-1 rounded bg-sky-500/20 text-sky-400 border border-sky-500/30">
                    Confidence: {selectedFinding.rca_confidence}
                  </span>
                </div>
                <h2 className="text-xl font-bold text-white mt-3">{selectedFinding.title}</h2>
                <div className="text-xs font-mono text-gray-400 mt-1">Target Endpoint: {selectedFinding.affected_endpoint}</div>
              </div>

              {/* Root Cause & Remediation */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-[#0c121e] p-4 rounded-xl border border-gray-800">
                  <h3 className="text-xs font-semibold uppercase text-sky-400">Root Cause Analysis</h3>
                  <p className="text-sm text-gray-200 mt-2">{selectedFinding.root_cause}</p>
                </div>
                <div className="bg-[#0c121e] p-4 rounded-xl border border-gray-800">
                  <h3 className="text-xs font-semibold uppercase text-emerald-400">Remediation Recommendation</h3>
                  <p className="text-sm text-gray-200 mt-2">{selectedFinding.remediation}</p>
                </div>
              </div>

              {/* Reproduction Script */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-semibold uppercase text-gray-400 flex items-center gap-1">
                    <Terminal className="w-4 h-4 text-sky-400" />
                    <span>Standalone Python Reproduction Script</span>
                  </span>
                  <span className="text-xs text-emerald-400">Reproduction Success: {selectedFinding.reproduction_rate}</span>
                </div>
                <pre className="bg-[#090d16] p-4 rounded-xl border border-gray-800 font-mono text-xs text-sky-300 overflow-x-auto">
                  {selectedFinding.repro_script}
                </pre>
              </div>
            </div>
          ) : (
            <div className="text-center py-12 text-gray-500">Select a finding to inspect evidence and reproduction script.</div>
          )}
        </div>
      </div>
    </div>
  );
}
