"use client";
import Link from 'next/link';
import { Check } from 'lucide-react';

export default function PricingPage() {
  const plans = [
    {
      name: "Free Developer",
      price: "$0",
      desc: "For individual developers testing local & staging projects.",
      features: [
        "10 Autonomous Test Runs / month",
        "API & Functional Contract testing",
        "Basic OWASP Security Probes",
        "Standard Evidence Artifacts & Repro Scripts",
        "Defensible Production Readiness Verdicts"
      ],
      cta: "Get Started Free",
      href: "/signup",
      highlight: false
    },
    {
      name: "Pro Engineering",
      price: "$299",
      period: "/month",
      desc: "For scaling engineering teams requiring continuous QA & security automation.",
      features: [
        "500 Autonomous Test Runs / month",
        "High-Volume Performance Load Generator",
        "Advanced BOLA / IDOR & SQL Injection Probes",
        "AI / LLM & RAG Quality Benchmarking",
        "Persistent Regression Test Suites",
        "Dedicated High-Capacity Execution Workers"
      ],
      cta: "Start 14-Day Free Trial",
      href: "/signup",
      highlight: true
    },
    {
      name: "Enterprise",
      price: "Custom",
      desc: "For enterprise security and reliability compliance requirements.",
      features: [
        "Unlimited Autonomous Runs & Custom Workers",
        "Self-Hosted Private VPC / On-Prem Deployments",
        "Custom Policy Broker & Governance Controls",
        "SSO, SAML & RBAC Multi-Tenant Scoping",
        "24/7 Dedicated Reliability Engineer Support",
        "Custom CI/CD Integrations & Webhooks"
      ],
      cta: "Contact Enterprise Team",
      href: "/signup",
      highlight: false
    }
  ];

  return (
    <div className="space-y-12 py-8 max-w-6xl mx-auto">
      <div className="text-center space-y-3">
        <h1 className="text-3xl font-extrabold text-white">Transparent Enterprise Pricing</h1>
        <p className="text-slate-400 text-sm max-w-xl mx-auto">
          Choose the appropriate autonomous testing tier for your engineering team.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {plans.map((p) => (
          <div
            key={p.name}
            className={`bg-[#0b0f19] border rounded-2xl p-8 flex flex-col justify-between space-y-6 ${
              p.highlight ? 'border-sky-500/80 shadow-2xl shadow-sky-500/10 ring-1 ring-sky-500/40' : 'border-slate-800'
            }`}
          >
            <div className="space-y-4">
              {p.highlight && (
                <span className="text-[10px] uppercase tracking-wider font-bold bg-sky-500/20 text-sky-400 border border-sky-500/30 px-2.5 py-1 rounded-full">
                  MOST POPULAR
                </span>
              )}
              <h2 className="text-xl font-bold text-white">{p.name}</h2>
              <p className="text-xs text-slate-400">{p.desc}</p>

              <div className="pt-2 flex items-baseline gap-1">
                <span className="text-4xl font-black text-white">{p.price}</span>
                {p.period && <span className="text-xs text-slate-500">{p.period}</span>}
              </div>

              <div className="space-y-2.5 pt-4 border-t border-slate-800/80">
                {p.features.map((f) => (
                  <div key={f} className="flex items-start gap-2 text-xs text-slate-300">
                    <Check className="w-4 h-4 text-sky-400 shrink-0 mt-0.5" />
                    <span>{f}</span>
                  </div>
                ))}
              </div>
            </div>

            <Link
              href={p.href}
              className={`w-full text-center py-3 rounded-xl font-bold text-xs transition shadow-lg ${
                p.highlight
                  ? 'bg-sky-600 hover:bg-sky-500 text-white shadow-sky-600/20'
                  : 'bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-800'
              }`}
            >
              {p.cta}
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}
