"use client";
import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import Logo from '../../components/Logo';
import { apiFetch, setAuthToken } from '../../lib/api';
import { Mail, Lock, User, Building, ArrowRight } from 'lucide-react';

export default function SignupPage() {
  const router = useRouter();
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSignup = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Backend POST /api/v1/auth/register expects: { email, password, full_name }
      const data = await apiFetch('/api/v1/auth/register', {
        method: 'POST',
        body: JSON.stringify({ email, password, full_name: fullName })
      });
      if (data.access_token) {
        setAuthToken(data.access_token);
        router.push('/dashboard');
      }
    } catch (err) {
      setError(err.message || 'Registration failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center py-12">
      <div className="max-w-xl w-full bg-[#0b0f19] border border-slate-800 rounded-2xl p-8 shadow-2xl space-y-6">
        <div className="text-center space-y-2">
          <div className="flex justify-center"><Logo size="md" showText={false} /></div>
          <h1 className="text-2xl font-bold text-white">Create Your Engineering Account</h1>
          <p className="text-xs text-slate-400">Start autonomous testing across your web, API, and AI applications</p>
        </div>

        {error && (
          <div className="p-3 bg-red-500/10 border border-red-500/30 rounded-lg text-xs text-red-400 font-medium">
            {error}
          </div>
        )}

        <form onSubmit={handleSignup} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Full Name</label>
            <div className="relative">
              <User className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
              <input
                type="text"
                required
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="Vishal Sharma"
                className="w-full bg-[#070a12] border border-slate-700 rounded-lg pl-9 pr-3 py-2 text-sm text-white focus:outline-none focus:border-sky-500"
              />
            </div>
          </div>

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
            <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Password</label>
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
            <span>{loading ? 'Creating Account...' : 'Create Free Account'}</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </form>

        <div className="text-center text-xs text-slate-400">
          Already have an account?{' '}
          <Link href="/login" className="text-sky-400 font-semibold hover:underline">Sign in</Link>
        </div>
      </div>
    </div>
  );
}
