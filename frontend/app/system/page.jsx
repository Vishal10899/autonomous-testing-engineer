"use client";
import { useState } from 'react';
import { Network, Database, Cpu, Server, Shield, Layers } from 'lucide-react';

export default function SystemMapPage() {
  const [selectedNode, setSelectedNode] = useState(null);

  const nodes = [
    { id: 'target_app', name: 'Web Target Gateway', type: 'Service', tech: 'FastAPI / Python', risk: 'HIGH', details: 'Main entry point routing HTTP requests.' },
    { id: 'ep_bola', name: 'GET /api/v1/user/profile', type: 'Endpoint', tech: 'REST', risk: 'CRITICAL', details: 'Exposes user identity & SSN. High security sensitivity.' },
    { id: 'ep_sqli', name: 'GET /api/v1/products/search', type: 'Endpoint', tech: 'REST', risk: 'CRITICAL', details: 'Executes dynamic database search query.' },
    { id: 'ep_race', name: 'POST /api/v1/checkout', type: 'Endpoint', tech: 'REST', risk: 'CRITICAL', details: 'Mutates user account balance and checkout ledger.' },
    { id: 'ep_perf', name: 'GET /api/v1/analytics/report', type: 'Endpoint', tech: 'REST', risk: 'HIGH', details: 'Complex analytics aggregate query.' },
    { id: 'db_postgres', name: 'PostgreSQL System of Record', type: 'Database', tech: 'PostgreSQL', risk: 'CRITICAL', details: 'Primary persistent transactional storage.' },
    { id: 'cache_redis', name: 'Redis Cache & Lock Broker', type: 'Cache', tech: 'Redis', risk: 'MEDIUM', details: 'Session cache and distributed locks.' },
    { id: 'ai_gateway', name: 'AI / RAG Gateway', type: 'AI Model', tech: 'OpenAI / Gemini', risk: 'HIGH', details: 'Handles RAG retrieval & LLM generation.' }
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between border-b border-gray-800 pb-4">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <Network className="w-6 h-6 text-sky-400" />
            <span>Universal System Model Graph</span>
          </h1>
          <p className="text-sm text-gray-400 mt-1">
            Visual topology mapping discovered components, endpoints, databases, caches, and AI models.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Graph Nodes Grid */}
        <div className="lg:col-span-2 bg-[#111827] border border-gray-800 rounded-xl p-6 space-y-4">
          <h2 className="text-sm font-semibold uppercase text-gray-400 tracking-wider">Discovered Graph Nodes</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {nodes.map((node) => (
              <div
                key={node.id}
                onClick={() => setSelectedNode(node)}
                className={`p-4 rounded-xl border cursor-pointer transition ${
                  selectedNode?.id === node.id
                    ? 'bg-sky-500/10 border-sky-500 text-sky-300'
                    : 'bg-[#0c121e] border-gray-800 hover:border-gray-700 text-gray-200'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold px-2 py-0.5 rounded bg-gray-800 text-gray-300">{node.type}</span>
                  <span className={`text-xs font-bold px-2 py-0.5 rounded ${
                    node.risk === 'CRITICAL' ? 'bg-red-500/20 text-red-400 border border-red-500/30' : 'bg-amber-500/20 text-amber-400'
                  }`}>
                    {node.risk} RISK
                  </span>
                </div>
                <div className="text-sm font-bold mt-2">{node.name}</div>
                <div className="text-xs text-gray-400 mt-1">{node.tech}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Node Inspector Panel */}
        <div className="bg-[#111827] border border-gray-800 rounded-xl p-6 space-y-4">
          <h2 className="text-sm font-semibold uppercase text-gray-400 tracking-wider">Node Inspector</h2>
          {selectedNode ? (
            <div className="space-y-4 text-sm">
              <div>
                <label className="text-xs text-gray-500 uppercase font-semibold">Node ID</label>
                <div className="font-mono text-gray-200">{selectedNode.id}</div>
              </div>
              <div>
                <label className="text-xs text-gray-500 uppercase font-semibold">Component Name</label>
                <div className="font-bold text-white text-base">{selectedNode.name}</div>
              </div>
              <div>
                <label className="text-xs text-gray-500 uppercase font-semibold">Technology Stack</label>
                <div className="text-sky-400">{selectedNode.tech}</div>
              </div>
              <div>
                <label className="text-xs text-gray-500 uppercase font-semibold">Risk Classification</label>
                <div className="text-red-400 font-bold">{selectedNode.risk}</div>
              </div>
              <div>
                <label className="text-xs text-gray-500 uppercase font-semibold">Discovery Rationale</label>
                <div className="text-gray-300 mt-1 bg-[#090d16] p-3 rounded-lg border border-gray-800">{selectedNode.details}</div>
              </div>
            </div>
          ) : (
            <div className="text-center py-12 text-gray-500 text-sm">
              Click any node in the system graph to inspect details and risk metrics.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
