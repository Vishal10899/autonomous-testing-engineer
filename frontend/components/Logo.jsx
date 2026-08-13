import React from 'react';

export default function Logo({ size = 'md', showText = true }) {
  const iconSizes = {
    sm: 'w-6 h-6 text-xs',
    md: 'w-8 h-8 text-sm',
    lg: 'w-10 h-10 text-base',
    xl: 'w-12 h-12 text-lg'
  };

  return (
    <div className="flex items-center gap-3 select-none">
      {/* Geometric ATE Brand Mark */}
      <div className={`relative ${iconSizes[size]} rounded-lg bg-gradient-to-br from-sky-500 via-indigo-600 to-slate-900 p-[1px] shadow-lg shadow-sky-500/20 flex items-center justify-center`}>
        <div className="w-full h-full bg-[#070a12] rounded-[7px] flex items-center justify-center relative overflow-hidden">
          {/* Subtle grid pattern background in mark */}
          <div className="absolute inset-0 bg-sky-500/5 opacity-40"></div>
          {/* Minimalist ATE Geometric Icon */}
          <svg className="w-4/5 h-4/5 text-sky-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M12 2L2 7l10 5 10-5-10-5z" />
            <path d="M2 17l10 5 10-5" />
            <path d="M2 12l10 5 10-5" />
          </svg>
        </div>
      </div>

      {showText && (
        <div className="flex flex-col">
          <span className="font-extrabold tracking-tight text-white font-sans flex items-center gap-1.5 leading-none text-base">
            Autonomous <span className="text-sky-400 font-extrabold">Testing Engineer</span>
          </span>
          <span className="text-[10px] text-gray-400 font-mono tracking-wider uppercase mt-1">
            Enterprise Autonomous QA & Security Platform
          </span>
        </div>
      )}
    </div>
  );
}
