"use client";
import { useState } from 'react';
import { Settings, Key, Shield, User, Users, Bell } from 'lucide-react';

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState('profile');

  return (
    <div className="space-y-6">
      <div className="border-b border-slate-800 pb-4">
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <Settings className="w-6 h-6 text-sky-400" />
          <span>Workspace & Account Settings</span>
        </h1>
        <p className="text-sm text-slate-400 mt-1">Manage profile, workspace API keys, team members, and security controls.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="space-y-1">
          {['profile', 'workspace', 'api-keys', 'security'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`w-full text-left px-3 py-2 rounded-lg text-xs font-semibold uppercase tracking-wider transition ${
                activeTab === tab ? 'bg-sky-500/20 text-sky-400 border border-sky-500/30' : 'text-slate-400 hover:bg-slate-900'
              }`}
            >
              {tab.replace('-', ' ')}
            </button>
          ))}
        </div>

        <div className="md:col-span-3 bg-[#0b0f19] border border-slate-800 rounded-xl p-6 space-y-4">
          {activeTab === 'profile' && (
            <div className="space-y-4 text-sm">
              <h2 className="text-base font-bold text-white">Developer Profile</h2>
              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Full Name</label>
                <input type="text" defaultValue="Vishal Sharma" className="w-full bg-[#070a12] border border-slate-700 rounded-lg px-3 py-2 text-white" />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Work Email</label>
                <input type="email" defaultValue="vishal@company.com" className="w-full bg-[#070a12] border border-slate-700 rounded-lg px-3 py-2 text-white" />
              </div>
            </div>
          )}

          {activeTab === 'api-keys' && (
            <div className="space-y-4 text-sm">
              <h2 className="text-base font-bold text-white">Workspace API Keys</h2>
              <p className="text-xs text-slate-400">Use API keys to trigger autonomous test runs from your CI/CD pipelines.</p>
              <div className="bg-[#070a12] p-4 rounded-xl border border-slate-800 font-mono text-xs text-sky-300 flex items-center justify-between">
                <span>ate_live_pk_9941a87...</span>
                <span className="text-xs text-slate-500">Created 2 days ago</span>
              </div>
            </div>
          )}

          {activeTab === 'workspace' && (
            <div className="space-y-4 text-sm">
              <h2 className="text-base font-bold text-white">Workspace Configuration</h2>
              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Workspace Name</label>
                <input type="text" defaultValue="Vishal Engineering" className="w-full bg-[#070a12] border border-slate-700 rounded-lg px-3 py-2 text-white" />
              </div>
            </div>
          )}

          {activeTab === 'security' && (
            <div className="space-y-4 text-sm">
              <h2 className="text-base font-bold text-white">Security & Multi-Factor Auth</h2>
              <div className="text-xs text-slate-300">Enforce SAML SSO and strict Policy Broker limits for all workspace members.</div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
