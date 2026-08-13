"use client";
import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import Logo from '../../components/Logo';
import { apiFetch, setAuthToken } from '../../lib/api';
import { Lock, Mail, ArrowRight } from 'lucide-react';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const data = await apiFetch('/api/v1/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password })
      });
      if (data.access_token) {
        setAuthToken(data.access_token);
        router.push('/dashboard');
      }
    } catch (err) {
      setError(err.message || 'Invalid email or password.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center py-12">
      <div className="max-w-4xl w-full grid grid-cols-1 md:grid-cols-2 bg-[#0b0f19] border border-slate-800 rounded-2xl overflow-hidden shadow-2xl">
        {/* Left Branding Column */}
        <div className="p-8 bg-gradient-to-br from-slate-950 via-slate-900 to-sky-950/40 border-r border-slate-800 flex flex-col justify-between">
          <Logo size="md" showText={true} />
          
          <div className="space-y-4 my-8">
            <h2 className="text-2xl font-bold text-white leading-snug">
              Find the failures before your users do.
            </h2>
            <p className="text-xs text-slate-300 leading-relaxed">
              Autonomous AI testing engine providing reproducible, evidence-backed security, API, database, and performance validation.
            </p>
          </div>

          <div className="text-xs text-slate-500 font-mono">
            Protected by Policy Broker Engine v5.0
          </div>
        </div>

        {/* Right Form Column */}
        <div className="p-8 flex flex-col justify-center space-y-6">
          <div>
            <h2 className="text-xl font-bold text-white">Welcome back</h2>
            <p className="text-xs text-slate-400 mt-1">Sign in to your enterprise workspace</p>
          </div>

          {error && (
            <div className="p-3 bg-red-500/10 border border-red-500/30 rounded-lg text-xs text-red-400 font-medium">
              {error}
            </div>
          )}

          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Work Email</label>
              <div className="relative">
                <Mail className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="developer@company.com"
                  className="w-full bg-[#070a12] border border-slate-700 rounded-lg pl-9 pr-3 py-2 text-sm text-white focus:outline-none focus:border-sky-500"
                />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between mb-1">
                <label className="text-xs font-semibold text-slate-400 uppercase">Password</label>
                <Link href="/forgot-password" className="text-xs text-sky-400 hover:underline">Forgot password?</Link>
              </div>
              <div className="relative">
                <Lock className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••••••"
                  className="w-full bg-[#070a12] border border-slate-700 rounded-lg pl-9 pr-3 py-2 text-sm text-white focus:outline-none focus:border-sky-500"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-sky-600 hover:bg-sky-500 text-white font-bold py-2.5 rounded-lg transition shadow-lg shadow-sky-600/20 text-sm flex items-center justify-center gap-2"
            >
              <span>{loading ? 'Authenticating...' : 'Sign In'}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </form>

          <div className="text-center text-xs text-slate-400">
            Don't have an account?{' '}
            <Link href="/signup" className="text-sky-400 font-semibold hover:underline">Create account</Link>
          </div>
        </div>
      </div>
    </div>
  );
}
