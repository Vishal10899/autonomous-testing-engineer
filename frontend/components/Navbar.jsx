"use client";
import { useState } from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import Logo from './Logo';
import { setAuthToken } from '../lib/api';
import { 
  LayoutDashboard, FolderKanban, Play, Network, Zap, ShieldAlert, 
  Eye, BarChart3, ShieldCheck, Cpu, FileCheck, Sliders, Settings, Award, Menu, X, LogOut 
} from 'lucide-react';

export default function Navbar() {
  const pathname = usePathname();
  const router = useRouter();
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleLogout = () => {
    setAuthToken(null);
    router.push('/login');
  };

  const isPublicRoute = ['/', '/pricing', '/docs', '/login', '/signup', '/forgot-password'].includes(pathname);

  if (isPublicRoute) {
    return (
      <header className="border-b border-slate-800/80 bg-[#070a12]/90 backdrop-blur sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <Link href="/" className="flex items-center">
              <Logo size="md" showText={true} />
            </Link>
            <div className="hidden md:flex items-center space-x-6 text-sm font-medium">
              <Link href="/" className={`transition ${pathname === '/' ? 'text-white' : 'text-slate-400 hover:text-slate-200'}`}>Features</Link>
              <Link href="/pricing" className={`transition ${pathname === '/pricing' ? 'text-white' : 'text-slate-400 hover:text-slate-200'}`}>Pricing</Link>
              <Link href="/docs" className={`transition ${pathname === '/docs' ? 'text-white' : 'text-slate-400 hover:text-slate-200'}`}>Documentation</Link>
            </div>
            <div className="flex items-center space-x-3">
              <Link href="/login" className="px-3.5 py-1.5 text-xs font-semibold text-slate-300 hover:text-white transition">
                Sign In
              </Link>
              <Link href="/signup" className="px-3.5 py-1.5 text-xs font-semibold text-white bg-sky-600 hover:bg-sky-500 rounded-lg transition shadow-md shadow-sky-600/20">
                Start Free Trial
              </Link>
            </div>
          </div>
        </div>
      </header>
    );
  }

  // Authenticated Compact Navbar
  const workspaceNavItems = [
    { label: 'Overview', href: '/dashboard', icon: LayoutDashboard },
    { label: 'Projects', href: '/projects', icon: FolderKanban },
    { label: 'Runs', href: '/runs', icon: Play },
    { label: 'System', href: '/system', icon: Network },
    { label: 'Live', href: '/live', icon: Zap },
    { label: 'Findings', href: '/findings', icon: ShieldAlert },
    { label: 'Evidence', href: '/evidence', icon: Eye },
    { label: 'Performance', href: '/performance', icon: BarChart3 },
    { label: 'Security', href: '/security', icon: ShieldCheck },
    { label: 'AI Quality', href: '/ai-quality', icon: Cpu },
    { label: 'Readiness', href: '/reports', icon: FileCheck },
    { label: 'Policies', href: '/policies', icon: Sliders },
  ];

  return (
    <header className="border-b border-slate-800/80 bg-[#070a12]/95 backdrop-blur sticky top-0 z-50">
      <div className="max-w-[1700px] mx-auto px-3 sm:px-4 lg:px-6">
        <div className="flex items-center justify-between h-14">
          {/* Left: Compact 32px Logo + Workspace indicator */}
          <div className="flex items-center space-x-3 shrink-0">
            <Link href="/dashboard" title="Autonomous Testing Engineer Dashboard">
              <Logo size="sm" showText={false} />
            </Link>
            <div className="h-4 w-[1px] bg-slate-800 hidden sm:block"></div>
            <div className="hidden sm:flex items-center space-x-1.5 text-xs bg-slate-900/80 border border-slate-800/80 px-2.5 py-1 rounded-md text-slate-300">
              <span className="font-semibold text-slate-400">Workspace:</span>
              <span className="font-bold text-white">Vishal Engineering</span>
            </div>
          </div>

          {/* Center: Desktop Compact Navigation Links */}
          <nav className="hidden xl:flex items-center space-x-1">
            {workspaceNavItems.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href || (item.href !== '/dashboard' && pathname.startsWith(item.href));
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`flex items-center space-x-1 px-2 py-1 rounded-md text-xs font-medium transition ${
                    isActive
                      ? 'bg-sky-500/15 text-sky-400 border border-sky-500/30'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
                  }`}
                >
                  <Icon className="w-3.5 h-3.5" />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </nav>

          {/* Right: Actions & User Controls */}
          <div className="flex items-center space-x-2 shrink-0">
            <Link
              href="/test/new"
              className="flex items-center gap-1 bg-sky-600 hover:bg-sky-500 text-white text-xs font-semibold px-2.5 py-1 rounded-md transition shadow-sm shadow-sky-600/30"
            >
              <Play className="w-3 h-3 fill-white" />
              <span>+ Run</span>
            </Link>
            <Link href="/admin/benchmarks" className="p-1.5 text-slate-400 hover:text-amber-400 transition" title="Engine Diagnostics & Benchmarks">
              <Award className="w-4 h-4" />
            </Link>
            <Link href="/settings" className="p-1.5 text-slate-400 hover:text-slate-200 transition" title="Settings">
              <Settings className="w-4 h-4" />
            </Link>
            <button
              onClick={handleLogout}
              className="p-1.5 text-slate-400 hover:text-red-400 transition flex items-center gap-1 text-xs"
              title="Sign Out"
            >
              <LogOut className="w-4 h-4" />
            </button>
            <button
              onClick={() => setMobileOpen(!mobileOpen)}
              className="xl:hidden p-1.5 text-slate-400 hover:text-white"
            >
              {mobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>

        {/* Mobile Navigation Drawer */}
        {mobileOpen && (
          <div className="xl:hidden py-3 border-t border-slate-800 grid grid-cols-2 gap-2">
            {workspaceNavItems.map((item) => {
              const Icon = item.icon;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={() => setMobileOpen(false)}
                  className="flex items-center space-x-2 px-3 py-2 rounded-lg text-xs font-medium text-slate-300 hover:bg-slate-800"
                >
                  <Icon className="w-4 h-4 text-sky-400" />
                  <span>{item.label}</span>
                </Link>
              );
            })}
            <button
              onClick={handleLogout}
              className="flex items-center space-x-2 px-3 py-2 rounded-lg text-xs font-medium text-red-400 hover:bg-slate-800 col-span-2"
            >
              <LogOut className="w-4 h-4" />
              <span>Sign Out / Logout</span>
            </button>
          </div>
        )}
      </div>
    </header>
  );
}
