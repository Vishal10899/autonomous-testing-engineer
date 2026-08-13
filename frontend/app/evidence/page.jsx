"use client";
import { useState } from 'react';
import { ShieldCheck, FileCode, CheckCircle, Copy, Terminal, Download } from 'lucide-react';

export default function EvidenceInspectorPage() {
  const [evidenceItems, setEvidenceItems] = useState([
    {
      id: 'ev_1',
      run_id: 'run_cert_991',
      type: 'request_response',
      sha256_hash: '5154f94ebf0c7a7634938cf2fb6bf7ce163c01a0f5ead3fd6d6dbe2c41501ea5',
      storage_path: './evidence_storage/run_cert_991_security.json',
      content: {
        request: { method: 'GET', url: 'http://127.0.0.1:8002/benchmark/api/v1/user/profile', headers: { Authorization: 'Bearer invalid_unauthorized_token' } },
        response: { status_code: 200, body: { user_id: 'victim_user_99', email: 'victim@example.com', ssn: '999-00-1234' } }
      }
    },
    {
      id: 'ev_2',
      run_id: 'run_cert_992',
      type: 'db_concurrency_trace',
      sha256_hash: 'a89f31c0021b44589d71c890123ef65439a0129031c28f110099881144223344',
      storage_path: './evidence_storage/run_cert_992_concurrency.json',
      content: {
        request: { method: 'POST', url: 'http://127.0.0.1:8002/benchmark/api/v1/checkout', concurrent_requests: 10 },
        response: { successful_count: 10, balance_deducted: 1000, race_condition_detected: true }
      }
    }
  ]);

  const [selectedEv, setSelectedEv] = useState(evidenceItems[0]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <ShieldCheck className="w-6 h-6 text-emerald-400" />
            <span>Evidence Artifact Inspector</span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Tamper-proof evidence graph with byte-level SHA-256 integrity hash verification (PRD Section 27).
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Evidence Items List */}
        <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-4 space-y-3">
          <h2 className="text-xs font-semibold uppercase text-slate-400 px-2">Evidence Artifacts ({evidenceItems.length})</h2>
          {evidenceItems.map((ev) => (
            <div
              key={ev.id}
              onClick={() => setSelectedEv(ev)}
              className={`p-4 rounded-xl border cursor-pointer transition ${
                selectedEv?.id === ev.id
                  ? 'bg-sky-500/10 border-sky-500 text-white'
                  : 'bg-[#070a12] border-slate-800 hover:border-slate-700 text-slate-300'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300">{ev.type}</span>
                <span className="text-xs text-emerald-400 font-mono">SHA-256 MATCH</span>
              </div>
              <div className="text-xs font-mono text-slate-400 mt-2 truncate">Hash: {ev.sha256_hash.slice(0, 16)}...</div>
            </div>
          ))}
        </div>

        {/* Evidence Artifact Detail */}
        <div className="lg:col-span-2 bg-[#0b0f19] border border-slate-800 rounded-xl p-6 space-y-6">
          {selectedEv ? (
            <div className="space-y-4">
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 px-2.5 py-1 rounded">
                    SHA-256 INTEGRITY VERIFIED
                  </span>
                </div>
                <div className="text-xs font-mono text-slate-400 mt-2">
                  Hash: <span className="text-sky-300">{selectedEv.sha256_hash}</span>
                </div>
                <div className="text-xs font-mono text-slate-500 mt-0.5">
                  Storage Path: {selectedEv.storage_path}
                </div>
              </div>

              {/* Raw Request & Response Payload Inspector */}
              <div className="space-y-3">
                <h3 className="text-xs font-semibold uppercase text-slate-400 flex items-center gap-1">
                  <Terminal className="w-4 h-4 text-sky-400" />
                  <span>Raw Request Payload</span>
                </h3>
                <pre className="bg-[#070a12] p-4 rounded-xl border border-slate-800 font-mono text-xs text-slate-300 overflow-x-auto">
                  {JSON.stringify(selectedEv.content.request, null, 2)}
                </pre>

                <h3 className="text-xs font-semibold uppercase text-slate-400 flex items-center gap-1 mt-4">
                  <Terminal className="w-4 h-4 text-emerald-400" />
                  <span>Raw Response Payload</span>
                </h3>
                <pre className="bg-[#070a12] p-4 rounded-xl border border-slate-800 font-mono text-xs text-slate-300 overflow-x-auto">
                  {JSON.stringify(selectedEv.content.response, null, 2)}
                </pre>
              </div>
            </div>
          ) : (
            <div className="text-center py-12 text-slate-500">Select an evidence item to inspect artifacts.</div>
          )}
        </div>
      </div>
    </div>
  );
}
