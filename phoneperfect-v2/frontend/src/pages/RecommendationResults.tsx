import React from 'react';
import { RecommendationResponse, RecommendationItem } from '../types';
import { CheckCircle2, AlertTriangle, ShieldCheck, ExternalLink, Scale, ArrowLeft } from 'lucide-react';

interface RecommendationResultsProps {
  results: RecommendationResponse;
  onSelectPhone: (phoneId: string) => void;
  onAddToCompare: (phoneId: string) => void;
  onBackToWizard: () => void;
}

export const RecommendationResults: React.FC<RecommendationResultsProps> = ({
  results,
  onSelectPhone,
  onAddToCompare,
  onBackToWizard
}) => {
  return (
    <div className="space-y-8 pb-16">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 rounded-2xl glass-panel border border-slate-800">
        <div>
          <button
            onClick={onBackToWizard}
            className="inline-flex items-center space-x-1.5 text-xs font-semibold text-slate-400 hover:text-sky-400 mb-2 transition-colors"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Modify Filters & Budget</span>
          </button>
          <h2 className="text-2xl md:text-3xl font-extrabold text-white">
            Top Recommendations ({results.recommendations.length} Matches)
          </h2>
          <p className="text-slate-400 text-xs md:text-sm mt-1">
            Evaluated <strong className="text-slate-200">{results.total_evaluated}</strong> devices. Strictly constrained under <strong className="text-sky-400">₹{results.budget_max.toLocaleString()}</strong>.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <div className="px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-800 text-center">
            <div className="text-xs text-slate-400">Eligible Under Budget</div>
            <div className="text-lg font-bold text-emerald-400">{results.eligible_count}</div>
          </div>
        </div>
      </div>

      {/* Recommendations Cards Grid */}
      <div className="space-y-6">
        {results.recommendations.map((item: RecommendationItem, index: number) => {
          const phone = item.phone;
          const isWinner = index === 0;

          return (
            <div
              key={phone.id}
              className={`rounded-2xl border transition-all overflow-hidden ${
                isWinner 
                  ? 'bg-gradient-to-b from-sky-950/40 via-slate-900/80 to-slate-900/90 border-sky-500/40 shadow-xl shadow-sky-500/10'
                  : 'bg-slate-900/70 border-slate-800 hover:border-slate-700'
              }`}
            >
              <div className="p-6 md:p-8 flex flex-col md:flex-row gap-6 md:gap-8 items-start">
                {/* Phone Image & Best Tag */}
                <div className="flex flex-col items-center flex-shrink-0 w-full md:w-44">
                  {isWinner && (
                    <span className="mb-3 px-3 py-1 rounded-full bg-sky-500 text-slate-950 text-xs font-extrabold tracking-wide uppercase shadow-md shadow-sky-500/30">
                      🏆 #1 Best Match
                    </span>
                  )}
                  <div className="w-36 h-48 rounded-xl bg-slate-950/60 p-3 border border-slate-800 flex items-center justify-center overflow-hidden">
                    <img
                      src={phone.canonical_image_url}
                      alt={phone.model_name}
                      className="max-h-full max-w-full object-contain hover:scale-105 transition-transform"
                      loading="lazy"
                    />
                  </div>
                  <div className="mt-3 text-center">
                    <div className="text-2xl font-black text-white">₹{item.current_price.toLocaleString()}</div>
                    <span className="text-[10px] font-semibold text-emerald-400 px-2 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/20">
                      {item.price_verification}
                    </span>
                  </div>
                </div>

                {/* Main Content Details */}
                <div className="flex-1 space-y-5">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-3">
                    <div>
                      <div className="text-xs font-bold text-sky-400 uppercase tracking-wider">{phone.brand_name}</div>
                      <h3 className="text-xl md:text-2xl font-black text-white">{phone.model_name}</h3>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="px-3.5 py-1.5 rounded-xl bg-sky-500/10 border border-sky-500/30 text-sky-400 font-black text-lg">
                        {item.match_score}% Match
                      </div>
                    </div>
                  </div>

                  {/* Hardware Telemetry Pills */}
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
                    <div className="p-2 rounded-lg bg-slate-950/60 border border-slate-800/80">
                      <div className="text-slate-400 text-[10px]">Chipset</div>
                      <div className="font-semibold text-slate-200 truncate">{phone.chipset || 'Octa-Core'}</div>
                    </div>
                    <div className="p-2 rounded-lg bg-slate-950/60 border border-slate-800/80">
                      <div className="text-slate-400 text-[10px]">Memory & Storage</div>
                      <div className="font-semibold text-slate-200">{phone.ram_gb}GB / {phone.storage_gb}GB</div>
                    </div>
                    <div className="p-2 rounded-lg bg-slate-950/60 border border-slate-800/80">
                      <div className="text-slate-400 text-[10px]">Battery & Pack</div>
                      <div className="font-semibold text-slate-200">{phone.battery_mah}mAh</div>
                    </div>
                    <div className="p-2 rounded-lg bg-slate-950/60 border border-slate-800/80">
                      <div className="text-slate-400 text-[10px]">Main Camera</div>
                      <div className="font-semibold text-slate-200">{phone.rear_camera_mp} MP</div>
                    </div>
                  </div>

                  {/* Why Recommended & Trade-offs */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="p-3.5 rounded-xl bg-slate-950/40 border border-slate-800/80">
                      <div className="text-xs font-bold text-emerald-400 mb-2 flex items-center space-x-1.5">
                        <CheckCircle2 className="w-3.5 h-3.5" />
                        <span>Why It Fits Your Profile</span>
                      </div>
                      <ul className="text-xs text-slate-300 space-y-1">
                        {item.why_recommended.map((reason, rIdx) => (
                          <li key={rIdx} className="flex items-start space-x-1.5">
                            <span className="text-emerald-400">•</span>
                            <span>{reason}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div className="p-3.5 rounded-xl bg-slate-950/40 border border-slate-800/80">
                      <div className="text-xs font-bold text-amber-400 mb-2 flex items-center space-x-1.5">
                        <AlertTriangle className="w-3.5 h-3.5" />
                        <span>Identified Trade-Offs</span>
                      </div>
                      <ul className="text-xs text-slate-400 space-y-1">
                        {item.trade_offs.length > 0 ? (
                          item.trade_offs.map((to, tIdx) => (
                            <li key={tIdx} className="flex items-start space-x-1.5">
                              <span className="text-amber-400">•</span>
                              <span>{to}</span>
                            </li>
                          ))
                        ) : (
                          <li className="text-slate-500 italic">No significant trade-offs detected in this bracket.</li>
                        )}
                      </ul>
                    </div>
                  </div>

                  {/* Actions Row */}
                  <div className="flex flex-wrap gap-3 pt-2">
                    <button
                      onClick={() => onSelectPhone(phone.id)}
                      className="px-5 py-2.5 rounded-xl bg-sky-500 hover:bg-sky-400 text-slate-950 font-bold text-xs flex items-center space-x-2 transition-all shadow-md shadow-sky-500/20"
                    >
                      <span>View Full Profile & Risk Audit</span>
                    </button>
                    <button
                      onClick={() => onAddToCompare(phone.id)}
                      className="px-4 py-2.5 rounded-xl bg-slate-950 hover:bg-slate-800 text-slate-300 border border-slate-700 font-semibold text-xs flex items-center space-x-1.5 transition-all"
                    >
                      <Scale className="w-3.5 h-3.5" />
                      <span>Compare</span>
                    </button>
                    <a
                      href={`https://www.amazon.in/s?k=${encodeURIComponent(phone.brand_name + ' ' + phone.model_name)}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="px-4 py-2.5 rounded-xl bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 border border-amber-500/30 font-semibold text-xs flex items-center space-x-1.5 transition-all ml-auto"
                    >
                      <span>Check Amazon India</span>
                      <ExternalLink className="w-3.5 h-3.5" />
                    </a>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
