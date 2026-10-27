import React from 'react';
import { Sparkles, ShieldCheck, Scale, Zap, ArrowRight, Award } from 'lucide-react';

interface HomeDashboardProps {
  onStartWizard: () => void;
  onExploreCatalog: () => void;
  onCompare: () => void;
}

export const HomeDashboard: React.FC<HomeDashboardProps> = ({
  onStartWizard,
  onExploreCatalog,
  onCompare
}) => {
  return (
    <div className="space-y-12 pb-16">
      {/* Hero Section */}
      <section className="relative overflow-hidden rounded-3xl border border-slate-800 bg-gradient-to-b from-slate-900/90 via-slate-900/40 to-slate-950 p-8 md:p-14 text-center">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-sky-500/15 via-transparent to-transparent pointer-events-none" />
        
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-sky-500/10 border border-sky-500/30 text-sky-400 text-xs font-semibold mb-6 animate-pulse">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Next-Generation Intelligence Engine Active</span>
        </div>

        <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight max-w-4xl mx-auto leading-tight md:leading-tight">
          Find Your Exact Match. <br className="hidden md:block"/>
          <span className="bg-gradient-to-r from-sky-400 via-indigo-300 to-white bg-clip-text text-transparent">
            Without Marketing Noise.
          </span>
        </h1>

        <p className="text-slate-400 text-base md:text-lg max-w-2xl mx-auto mt-5 leading-relaxed">
          PhonePerfect 2.0 uses multi-criteria hardware telemetry, strict budget constraints, and real-time purchase risk analysis to find your ideal smartphone.
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mt-8">
          <button
            onClick={onStartWizard}
            className="w-full sm:w-auto px-7 py-3.5 rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white font-bold text-base shadow-lg shadow-sky-500/25 flex items-center justify-center space-x-2 transition-all transform hover:-translate-y-0.5 active:translate-y-0"
          >
            <span>Launch Match Wizard</span>
            <ArrowRight className="w-4 h-4" />
          </button>
          <button
            onClick={onExploreCatalog}
            className="w-full sm:w-auto px-7 py-3.5 rounded-xl bg-slate-900/80 hover:bg-slate-800 text-slate-200 border border-slate-700/80 font-semibold text-base transition-all"
          >
            Explore 560+ Catalog
          </button>
        </div>

        {/* Live Metrics Row */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-12 pt-8 border-t border-slate-800/80 max-w-3xl mx-auto">
          <div>
            <div className="text-2xl font-black text-white">562</div>
            <div className="text-xs text-slate-400 mt-0.5">Verified Devices</div>
          </div>
          <div>
            <div className="text-2xl font-black text-sky-400">0 Over-Budget</div>
            <div className="text-xs text-slate-400 mt-0.5">Strict Constraint</div>
          </div>
          <div>
            <div className="text-2xl font-black text-indigo-400">100%</div>
            <div className="text-xs text-slate-400 mt-0.5">Spec-Backed Logic</div>
          </div>
          <div>
            <div className="text-2xl font-black text-emerald-400">4-Tier</div>
            <div className="text-xs text-slate-400 mt-0.5">Purchase Risk Model</div>
          </div>
        </div>
      </section>

      {/* Feature Pillars */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 rounded-2xl glass-panel border border-slate-800 hover:border-slate-700 transition-colors">
          <div className="w-12 h-12 rounded-xl bg-sky-500/10 border border-sky-500/20 text-sky-400 flex items-center justify-center mb-4">
            <Zap className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-white mb-2">Hard Budget Discipline</h3>
          <p className="text-sm text-slate-400 leading-relaxed">
            Unlike commercial portals that upsell devices outside your comfort zone, our algorithms strictly respect your budget ceiling.
          </p>
        </div>

        <div className="p-6 rounded-2xl glass-panel border border-slate-800 hover:border-slate-700 transition-colors">
          <div className="w-12 h-12 rounded-xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 flex items-center justify-center mb-4">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-white mb-2">Purchase-Risk Audit</h3>
          <p className="text-sm text-slate-400 leading-relaxed">
            Every device undergoes a 4-point verification check for price freshness, specification completeness, and software support lifespan.
          </p>
        </div>

        <div className="p-6 rounded-2xl glass-panel border border-slate-800 hover:border-slate-700 transition-colors">
          <div className="w-12 h-12 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-400 flex items-center justify-center mb-4">
            <Scale className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-white mb-2">Side-by-Side Spec Matrix</h3>
          <p className="text-sm text-slate-400 leading-relaxed">
            Directly compare display tech, thermal dissipation, camera sensors, and battery charging speeds without sponsored bias.
          </p>
        </div>
      </section>
    </div>
  );
};
