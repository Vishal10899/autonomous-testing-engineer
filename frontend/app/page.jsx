"use client";
import Link from 'next/link';
import { 
  ShieldAlert, Activity, Network, Zap, CheckCircle, ArrowRight, Play, 
  Cpu, Lock, Database, Server, Terminal, ShieldCheck, Layers, ChevronRight, FileCheck 
} from 'lucide-react';

export default function LandingPage() {
  const capabilities = [
    { title: "API Testing", desc: "REST, GraphQL, OpenAPI contract validation, authorization checks, idempotency, and schema drift detection.", icon: Server },
    { title: "Web / Browser Testing", desc: "Deterministic browser navigation, form submissions, session handling, visual trace logging, and console error capture.", icon: Network },
    { title: "Security Testing", desc: "BOLA / IDOR, SQL Injection, SSRF, Broken Auth, Session Hijack, and hardcoded secret scanner.", icon: ShieldAlert },
    { title: "Performance Testing", desc: "High-volume load generation, RPS ramping, p50/p90/p95/p99 latency analysis, and resource safety triggers.", icon: Activity },
    { title: "Reliability & Chaos", desc: "Timeout boundaries, circuit breaker validation, dependency fault injection, retry policy verification, and crash recovery.", icon: Zap },
    { title: "Database & Concurrency", desc: "Concurrency race condition probes, duplicate transactions, transaction isolation locks, and deadlock detection.", icon: Database },
    { title: "AI / LLM / RAG Testing", desc: "Prompt injection vectors, hallucination rate scoring, RAG context grounding metrics, and agent tool safety.", icon: Cpu },
    { title: "Regression & Retesting", desc: "Converts confirmed findings into persistent regression tests. Retests fixes against evidence baselines.", icon: CheckCircle }
  ];

  const steps = [
    { num: '01', title: 'DISCOVER', desc: 'Independently inspects APIs, repositories, documentation, and entrypoints.' },
    { num: '02', title: 'MODEL', desc: 'Constructs the Universal System Model Graph mapping services, databases, and dependencies.' },
    { num: '03', title: 'PLAN', desc: 'Formulates risk-based test strategies using Expected Information Gain.' },
    { num: '04', title: 'EXECUTE', desc: 'Dispatches deterministic execution engines through policy safety brokers.' },
    { num: '05', title: 'VERIFY', desc: 'Reproduces anomalies across multiple runs to filter out flaky behavior.' },
    { num: '06', title: 'EXPLAIN', desc: 'Infers root cause with evidence-backed confidence ratings and business impact.' },
    { num: '07', title: 'RETEST', desc: 'Verifies engineering fixes against initial evidence baselines.' },
    { num: '08', title: 'CERTIFY', desc: 'Provides defensible READY / CONDITIONAL / NOT_READY release decisions.' }
  ];

  const techStack = [
    'Python', 'JavaScript/TypeScript', 'Go', 'Rust', 'Java', '.NET',
    'FastAPI', 'Next.js', 'Express', 'Django', 'React', 'Spring Boot',
    'PostgreSQL', 'Redis', 'MongoDB', 'SQLite',
    'OpenAI', 'Gemini', 'Anthropic', 'Ollama', 'Qdrant'
  ];

  return (
    <div className="space-y-24 py-8">
      {/* SECTION 1: HERO */}
      <section className="relative overflow-hidden pt-8 pb-12">
        <div className="text-center max-w-4xl mx-auto space-y-6">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-sky-500/10 border border-sky-500/30 text-sky-400 text-xs font-medium">
            <SparklesIcon className="w-3.5 h-3.5" />
            <span>Autonomous Software Testing & Production Readiness</span>
          </div>

          <h1 className="text-4xl sm:text-6xl font-extrabold text-white tracking-tight leading-tight">
            Find the failures <br className="hidden sm:block" />
            <span className="bg-gradient-to-r from-sky-400 via-indigo-300 to-purple-400 bg-clip-text text-transparent">
              before your users do.
            </span>
          </h1>

          <p className="text-lg text-slate-300 max-w-2xl mx-auto leading-relaxed">
            Autonomous Testing Engineer discovers, attacks, validates, reproduces, and explains failures across APIs, web applications, databases, security, performance, and AI systems.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
            <Link href="/signup" className="w-full sm:w-auto px-8 py-3.5 rounded-xl font-bold text-white bg-sky-600 hover:bg-sky-500 transition shadow-xl shadow-sky-600/25 flex items-center justify-center gap-2">
              <span>Start Testing Free</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
            <Link href="/dashboard" className="w-full sm:w-auto px-8 py-3.5 rounded-xl font-semibold text-slate-300 bg-slate-900 border border-slate-800 hover:bg-slate-800 transition flex items-center justify-center gap-2">
              <Play className="w-4 h-4 text-sky-400 fill-sky-400" />
              <span>Explore Live Console</span>
            </Link>
          </div>
        </div>

        {/* HERO VISUALIZATION: AUTONOMOUS TESTING PIPELINE */}
        <div className="mt-12 max-w-5xl mx-auto bg-[#0b0f19] border border-slate-800 rounded-2xl p-6 shadow-2xl space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800/80 pb-3 text-xs text-slate-400 font-mono">
            <span className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
              <span>AUTONOMOUS ENGINE ACTIVE</span>
            </span>
            <span>TARGET: https://staging.api.internal</span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-6 gap-3 text-center">
            {['Application', 'Discovery', 'Risk Analysis', 'Autonomous Tests', 'Evidence Graph', 'Readiness Decision'].map((step, idx) => (
              <div key={step} className="bg-slate-900/90 border border-slate-800 rounded-xl p-3 space-y-1">
                <div className="text-[10px] font-mono text-sky-400">STAGE 0{idx+1}</div>
                <div className="text-xs font-bold text-slate-200">{step}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* SECTION 2: TRUST STATEMENT */}
      <section className="border-y border-slate-800/80 py-12 bg-slate-950/40 text-center">
        <h2 className="text-2xl font-bold text-white tracking-tight">
          One autonomous engineer. <span className="text-sky-400">Every layer of your software.</span>
        </h2>
        <p className="text-sm text-slate-400 mt-2 max-w-xl mx-auto">
          Built for modern multidisciplinary engineering organizations—from developer branch testing to release engineering verification.
        </p>
      </section>

      {/* SECTION 3: HOW IT WORKS */}
      <section className="max-w-6xl mx-auto space-y-12">
        <div className="text-center space-y-3">
          <h2 className="text-3xl font-extrabold text-white">How The Autonomous Engineer Operates</h2>
          <p className="text-slate-400 text-sm">8-stage autonomous pipeline executing continuous system discovery and verification.</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {steps.map((s) => (
            <div key={s.num} className="bg-[#0b0f19] border border-slate-800 rounded-xl p-5 space-y-2 hover:border-sky-500/40 transition">
              <span className="text-xs font-mono font-bold text-sky-400">{s.num}</span>
              <h3 className="text-base font-bold text-white">{s.title}</h3>
              <p className="text-xs text-slate-400 leading-relaxed">{s.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* SECTION 4: TESTING CAPABILITIES */}
      <section className="max-w-6xl mx-auto space-y-12">
        <div className="text-center space-y-3">
          <h2 className="text-3xl font-extrabold text-white">Multidisciplinary Testing Capabilities</h2>
          <p className="text-slate-400 text-sm">Engineered across all core technical vectors with specialized deterministic engines.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {capabilities.map((cap) => {
            const Icon = cap.icon;
            return (
              <div key={cap.title} className="bg-[#0b0f19] border border-slate-800 rounded-xl p-6 space-y-3 hover:border-sky-500/40 transition">
                <div className="w-10 h-10 rounded-lg bg-sky-500/10 border border-sky-500/30 flex items-center justify-center text-sky-400">
                  <Icon className="w-5 h-5" />
                </div>
                <h3 className="text-base font-bold text-white">{cap.title}</h3>
                <p className="text-xs text-slate-400 leading-relaxed">{cap.desc}</p>
              </div>
            );
          })}
        </div>
      </section>

      {/* SECTION 5: REAL EVIDENCE SHOWCASE */}
      <section className="max-w-5xl mx-auto bg-[#0b0f19] border border-slate-800 rounded-2xl p-8 space-y-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
          <div>
            <div className="text-xs font-mono text-sky-400 uppercase font-bold">Evidence-First Assurance</div>
            <h2 className="text-2xl font-bold text-white mt-1">Every Important Finding Is Backed By Evidence</h2>
          </div>
          <span className="text-xs font-mono bg-emerald-500/10 text-emerald-400 px-3 py-1 rounded-full border border-emerald-500/30">
            SHA-256 INTEGRITY VERIFIED
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-3 bg-slate-900/80 p-5 rounded-xl border border-slate-800">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold bg-red-500/20 text-red-400 border border-red-500/30 px-2 py-0.5 rounded">CRITICAL</span>
              <span className="text-xs font-mono text-slate-400">Confidence: DIRECTLY_OBSERVED</span>
            </div>
            <h3 className="text-base font-bold text-white">BOLA / IDOR Authorization Bypass</h3>
            <div className="text-xs font-mono text-sky-400">GET /api/v1/users/profile</div>
            <p className="text-xs text-slate-300">Endpoint returned sensitive SSN and billing profile for unauthorized Bearer token.</p>
          </div>

          <div className="space-y-3 bg-slate-900/80 p-5 rounded-xl border border-slate-800">
            <div className="text-xs font-mono text-slate-400">Reproduction Success: 10/10 attempts</div>
            <div className="text-xs font-mono text-slate-400">Artifact SHA-256: 5154f94ebf0c7a7...</div>
            <div className="text-xs text-emerald-400 font-bold">Root Cause: Missing endpoint ownership check middleware</div>
            <p className="text-xs text-slate-400">Includes standalone executable Python reproduction script.</p>
          </div>
        </div>
      </section>

      {/* SECTION 6: SUPPORTED TECHNOLOGIES */}
      <section className="max-w-5xl mx-auto space-y-6 text-center">
        <h2 className="text-2xl font-bold text-white">Dynamic Technology Stack Integration</h2>
        <div className="flex flex-wrap items-center justify-center gap-2">
          {techStack.map((tech) => (
            <span key={tech} className="text-xs font-mono bg-slate-900 text-slate-300 border border-slate-800 px-3 py-1.5 rounded-lg">
              {tech}
            </span>
          ))}
        </div>
      </section>
    </div>
  );
}

function SparklesIcon(props) {
  return (
    <svg {...props} fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-6.857 2.286L12 21l-2.286-6.857L3 12l6.857-2.286L12 3z" />
    </svg>
  );
}
