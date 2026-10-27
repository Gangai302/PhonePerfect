import React, { useState } from 'react';
import { RecommendationRequest, RecommendationResponse } from '../types';
import { api } from '../services/api';
import { ArrowRight, ArrowLeft, Sliders, CheckCircle2, AlertCircle, Sparkles } from 'lucide-react';

interface RequirementsWizardProps {
  onResultsGenerated: (results: RecommendationResponse) => void;
  onCancel: () => void;
}

export const RequirementsWizard: React.FC<RequirementsWizardProps> = ({
  onResultsGenerated,
  onCancel
}) => {
  const [step, setStep] = useState<number>(1);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Wizard state
  const [budget, setBudget] = useState<number>(35000);
  const [primaryUse, setPrimaryUse] = useState<string>('DAILY');
  const [minRam, setMinRam] = useState<number>(8);
  const [minStorage, setMinStorage] = useState<number>(128);
  const [require5G, setRequire5G] = useState<boolean>(true);
  const [requireOIS, setRequireOIS] = useState<boolean>(false);
  
  const [priorities, setPriorities] = useState({
    performance: 4,
    camera: 3,
    battery: 4,
    display: 4,
    longevity: 3
  });

  const [excludedBrands, setExcludedBrands] = useState<string[]>([]);

  const toggleBrandExclusion = (brandSlug: string) => {
    if (excludedBrands.includes(brandSlug)) {
      setExcludedBrands(excludedBrands.filter(b => b !== brandSlug));
    } else {
      setExcludedBrands([...excludedBrands, brandSlug]);
    }
  };

  const handleCompute = async () => {
    setLoading(true);
    setError(null);
    try {
      const payload: RecommendationRequest = {
        budget_max: budget,
        primary_use: primaryUse,
        priorities,
        min_ram_gb: minRam,
        min_storage_gb: minStorage,
        excluded_brands: excludedBrands,
        require_5g: require5G,
        require_ois: requireOIS
      };
      const response = await api.getRecommendations(payload);
      onResultsGenerated(response);
    } catch (err: any) {
      setError(err.message || 'Failed to calculate recommendations');
    } finally {
      setLoading(false);
    }
  };

  const primaryUseOptions = [
    { id: 'GAMING', title: 'Intense 3D Gaming', desc: 'Prioritizes flagship SoC thermal limits, high refresh rate, and touch sampling' },
    { id: 'CAMERA', title: 'Content & Photography', desc: 'Focuses on large primary sensor, OIS, optical zoom, and portrait tuning' },
    { id: 'BATTERY', title: 'Heavy Traveler / Endurance', desc: 'Maximizes battery capacity (5500mAh+), efficient display, and rapid wired charging' },
    { id: 'DAILY', title: 'Balanced Everyday Use', desc: 'Well-rounded device with smooth display, clean UI, and durable build quality' },
    { id: 'WORK', title: 'Productivity & Multitasking', desc: 'Prioritizes high RAM (12GB+), long software update guarantees, and fast storage' }
  ];

  return (
    <div className="max-w-3xl mx-auto py-6">
      {/* Step Indicator */}
      <div className="mb-8 flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <span className="text-xs font-semibold text-sky-400 uppercase tracking-wider">Step {step} of 3</span>
          <h2 className="text-2xl font-bold text-white mt-1">
            {step === 1 && 'Set Your Budget Ceiling'}
            {step === 2 && 'Primary Usage & Priorities'}
            {step === 3 && 'Hardware Thresholds & Brand Filters'}
          </h2>
        </div>
        <div className="flex space-x-1.5">
          {[1, 2, 3].map((s) => (
            <div
              key={s}
              className={`w-7 h-1.5 rounded-full transition-all ${
                step >= s ? 'bg-sky-500' : 'bg-slate-800'
              }`}
            />
          ))}
        </div>
      </div>

      {error && (
        <div className="mb-6 p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-400 flex items-center space-x-3 text-sm">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* STEP 1: Budget Ceiling */}
      {step === 1 && (
        <div className="space-y-6">
          <div className="p-6 rounded-2xl glass-panel border border-slate-800">
            <label className="block text-sm font-medium text-slate-300 mb-2">
              Maximum Budget (Strict Constraint)
            </label>
            <div className="flex items-center space-x-4 mb-4">
              <span className="text-4xl font-extrabold text-sky-400">₹{budget.toLocaleString()}</span>
              <span className="text-xs px-2.5 py-1 rounded-md bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-semibold">
                Hard Ceiling Enforced
              </span>
            </div>

            <input
              type="range"
              min="10000"
              max="150000"
              step="2500"
              value={budget}
              onChange={(e) => setBudget(Number(e.target.value))}
              className="w-full h-2.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-sky-500"
            />

            <div className="flex justify-between text-xs text-slate-500 mt-2 font-mono">
              <span>₹10,000</span>
              <span>₹50,000</span>
              <span>₹1,00,000</span>
              <span>₹1,50,000+</span>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 mt-6">
              {[20000, 30000, 45000, 75000].map((preset) => (
                <button
                  key={preset}
                  onClick={() => setBudget(preset)}
                  className={`py-2 px-3 rounded-lg text-xs font-semibold border transition-all ${
                    budget === preset
                      ? 'bg-sky-500 text-slate-950 border-sky-400'
                      : 'bg-slate-900 text-slate-300 border-slate-800 hover:border-slate-700'
                  }`}
                >
                  ₹{preset.toLocaleString()}
                </button>
              ))}
            </div>
          </div>

          <div className="flex justify-end pt-4">
            <button
              onClick={() => setStep(2)}
              className="px-6 py-3 rounded-xl bg-sky-500 hover:bg-sky-400 text-slate-950 font-bold flex items-center space-x-2 transition-all shadow-md shadow-sky-500/20"
            >
              <span>Next: Usage Priorities</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {/* STEP 2: Usage Profile & Priorities */}
      {step === 2 && (
        <div className="space-y-6">
          <div className="space-y-3">
            <label className="block text-sm font-semibold text-slate-200">
              Select Primary Daily Use Case
            </label>
            <div className="grid grid-cols-1 gap-2.5">
              {primaryUseOptions.map((opt) => (
                <div
                  key={opt.id}
                  onClick={() => setPrimaryUse(opt.id)}
                  className={`p-4 rounded-xl border cursor-pointer transition-all flex items-start space-x-3.5 ${
                    primaryUse === opt.id
                      ? 'bg-sky-500/10 border-sky-500/40 text-white'
                      : 'bg-slate-900/60 border-slate-800 text-slate-400 hover:border-slate-700'
                  }`}
                >
                  <div className={`mt-0.5 w-4 h-4 rounded-full border flex items-center justify-center ${
                    primaryUse === opt.id ? 'border-sky-400 bg-sky-500' : 'border-slate-600'
                  }`}>
                    {primaryUse === opt.id && <div className="w-1.5 h-1.5 rounded-full bg-slate-950" />}
                  </div>
                  <div>
                    <div className="font-bold text-sm text-slate-200">{opt.title}</div>
                    <div className="text-xs text-slate-400 mt-0.5">{opt.desc}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="flex justify-between pt-4">
            <button
              onClick={() => setStep(1)}
              className="px-5 py-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-300 font-semibold flex items-center space-x-2 border border-slate-800"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Back</span>
            </button>
            <button
              onClick={() => setStep(3)}
              className="px-6 py-2.5 rounded-xl bg-sky-500 hover:bg-sky-400 text-slate-950 font-bold flex items-center space-x-2 transition-all shadow-md shadow-sky-500/20"
            >
              <span>Next: Hardware Thresholds</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {/* STEP 3: Hardware Constraints */}
      {step === 3 && (
        <div className="space-y-6">
          <div className="p-6 rounded-2xl glass-panel border border-slate-800 space-y-6">
            <div>
              <label className="block text-sm font-semibold text-slate-200 mb-2">
                Minimum Memory (RAM)
              </label>
              <div className="grid grid-cols-4 gap-2">
                {[6, 8, 12, 16].map((ram) => (
                  <button
                    key={ram}
                    onClick={() => setMinRam(ram)}
                    className={`py-2 rounded-lg text-xs font-semibold border ${
                      minRam === ram 
                        ? 'bg-sky-500 text-slate-950 border-sky-400' 
                        : 'bg-slate-900 text-slate-400 border-slate-800 hover:border-slate-700'
                    }`}
                  >
                    {ram} GB+
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-semibold text-slate-200 mb-2">
                Minimum Internal Storage
              </label>
              <div className="grid grid-cols-3 gap-2">
                {[128, 256, 512].map((storage) => (
                  <button
                    key={storage}
                    onClick={() => setMinStorage(storage)}
                    className={`py-2 rounded-lg text-xs font-semibold border ${
                      minStorage === storage 
                        ? 'bg-sky-500 text-slate-950 border-sky-400' 
                        : 'bg-slate-900 text-slate-400 border-slate-800 hover:border-slate-700'
                    }`}
                  >
                    {storage} GB+
                  </button>
                ))}
              </div>
            </div>

            <div className="pt-2 border-t border-slate-800/80 flex flex-col sm:flex-row gap-4">
              <label className="flex items-center space-x-3 cursor-pointer">
                <input
                  type="checkbox"
                  checked={require5G}
                  onChange={(e) => setRequire5G(e.target.checked)}
                  className="w-4 h-4 rounded text-sky-500 bg-slate-900 border-slate-700 focus:ring-sky-500"
                />
                <span className="text-sm text-slate-300">Require 5G Connectivity</span>
              </label>

              <label className="flex items-center space-x-3 cursor-pointer">
                <input
                  type="checkbox"
                  checked={requireOIS}
                  onChange={(e) => setRequireOIS(e.target.checked)}
                  className="w-4 h-4 rounded text-sky-500 bg-slate-900 border-slate-700 focus:ring-sky-500"
                />
                <span className="text-sm text-slate-300">Require OIS (Camera Stabilization)</span>
              </label>
            </div>
          </div>

          <div className="flex justify-between pt-4">
            <button
              onClick={() => setStep(2)}
              className="px-5 py-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-300 font-semibold flex items-center space-x-2 border border-slate-800"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Back</span>
            </button>
            <button
              onClick={handleCompute}
              disabled={loading}
              className="px-8 py-3 rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white font-bold flex items-center space-x-2 transition-all shadow-lg shadow-sky-500/25 disabled:opacity-50"
            >
              {loading ? (
                <span>Calculating Telemetry...</span>
              ) : (
                <>
                  <Sparkles className="w-4 h-4" />
                  <span>Generate Recommendations</span>
                </>
              )}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
