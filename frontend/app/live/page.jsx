"use client";
import { useState, useEffect } from 'react';
import { Zap, Terminal, ShieldAlert, CheckCircle2, AlertOctagon } from 'lucide-react';

export default function LiveStreamPage() {
  const [logs, setLogs] = useState([
    { id: 1, time: '05:38:45', type: 'DISCOVERY', msg: 'Discovery Engine started for target http://127.0.0.1:8002/benchmark' },
    { id: 2, time: '05:38:46', type: 'TECH', msg: 'Technology profile identified: FastAPI, Python 3.14, SQLite/PostgreSQL' },
    { id: 3, time: '05:38:47', type: 'GRAPH', msg: 'Universal System Model Graph constructed: 8 Nodes, 6 Edges' },
    { id: 4, time: '05:38:48', type: 'RISK', msg: 'Risk Engine upgraded GET /api/v1/user/profile to CRITICAL risk' },
    { id: 5, time: '05:38:49', type: 'PLAN', msg: 'Adaptive Test Planner generated 12 deduplicated test cases (SHA-256 verified)' },
    { id: 6, time: '05:38:50', type: 'EXECUTE', msg: 'Security Probe launched: BOLA Authorization Bypass on GET /api/v1/user/profile' },
    { id: 7, time: '05:38:51', type: 'ANOMALY', msg: 'ANOMALY DETECTED: Endpoint returned 200 OK with sensitive SSN data for unauthorized token' },
    { id: 8, time: '05:38:52', type: 'REPRO', msg: 'Reproduction Engine verified defect across 10/10 automated attempts' },
    { id: 9, time: '05:38:53', type: 'RCA', msg: 'RCA Engine inferred DIRECTLY_OBSERVED root cause: Missing endpoint authorization check' },
    { id: 10, time: '05:38:54', type: 'REPORT', msg: 'Production Readiness verdict evaluated: NOT_READY (Blocked by 1 Critical finding)' }
  ]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between border-b border-gray-800 pb-4">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <Zap className="w-6 h-6 text-amber-400" />
            <span>Live Engineering Stream</span>
          </h1>
          <p className="text-sm text-gray-400 mt-1">
            Real-time event feed detailing agent discovery, risk upgrades, anomaly detection, RCA, and retesting.
          </p>
        </div>
        <div className="flex items-center gap-2 text-xs bg-emerald-500/10 text-emerald-400 px-3 py-1.5 rounded-full border border-emerald-500/30">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span>STREAM ACTIVE</span>
        </div>
      </div>

      {/* Terminal Output Container */}
      <div className="bg-[#0c121e] border border-gray-800 rounded-xl p-6 font-mono text-sm space-y-3 shadow-2xl overflow-hidden">
        <div className="flex items-center justify-between pb-3 border-b border-gray-800 text-xs text-gray-500">
          <span>EVENT STREAM LOG</span>
          <span>WEBSOCKET STATUS: CONNECTED</span>
        </div>

        <div className="space-y-2 max-h-[500px] overflow-y-auto pr-2">
          {logs.map((log) => (
            <div key={log.id} className="flex items-start gap-3 hover:bg-gray-900/50 p-2 rounded transition">
              <span className="text-gray-500 text-xs shrink-0 mt-0.5">{log.time}</span>
              <span className={`text-xs font-bold px-2 py-0.5 rounded shrink-0 ${
                log.type === 'ANOMALY' ? 'bg-red-500/20 text-red-400 border border-red-500/30' :
                log.type === 'RISK' ? 'bg-amber-500/20 text-amber-400' :
                log.type === 'REPRO' ? 'bg-sky-500/20 text-sky-400' :
                'bg-gray-800 text-gray-300'
              }`}>
                {log.type}
              </span>
              <span className="text-gray-200">{log.msg}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
