import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Scale, Trash2, ArrowLeft } from 'lucide-react';

interface SideBySideCompareProps {
  compareIds: string[];
  onRemoveFromCompare: (phoneId: string) => void;
  onClearCompare: () => void;
  onBack: () => void;
}

export const SideBySideCompare: React.FC<SideBySideCompareProps> = ({
  compareIds,
  onRemoveFromCompare,
  onClearCompare,
  onBack
}) => {
  const [data, setData] = useState<any | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    if (compareIds.length >= 2) {
      loadComparison();
    } else {
      setData(null);
      setLoading(false);
    }
  }, [compareIds]);

  const loadComparison = async () => {
    setLoading(true);
    try {
      const res = await api.comparePhones(compareIds);
      setData(res);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  if (compareIds.length < 2) {
    return (
      <div className="py-24 text-center space-y-4 max-w-md mx-auto">
        <div className="w-16 h-16 rounded-2xl bg-sky-500/10 border border-sky-500/20 text-sky-400 flex items-center justify-center mx-auto">
          <Scale className="w-8 h-8" />
        </div>
        <h3 className="text-xl font-bold text-white">Compare Smartphones</h3>
        <p className="text-sm text-slate-400">
          You currently have {compareIds.length} device selected. Please select at least 2 smartphones from the Catalog or Recommendations to generate a side-by-side spec comparison matrix.
        </p>
        <button
          onClick={onBack}
          className="px-6 py-2.5 rounded-xl bg-sky-500 hover:bg-sky-400 text-slate-950 font-bold text-sm"
        >
          Explore Catalog
        </button>
      </div>
    );
  }

  if (loading || !data) {
    return (
      <div className="py-24 text-center text-slate-500 font-mono text-sm animate-pulse">
        Generating comparative telemetry matrix...
      </div>
    );
  }

  const phones = data.phones;
  const specComp = data.spec_comparison;
  const advantages = data.advantages;

  return (
    <div className="space-y-6 pb-16 max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between p-6 rounded-2xl glass-panel border border-slate-800">
        <div>
          <button
            onClick={onBack}
            className="inline-flex items-center space-x-1 text-xs font-semibold text-slate-400 hover:text-sky-400 mb-1"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Back</span>
          </button>
          <h2 className="text-2xl font-bold text-white">Side-by-Side Spec Matrix</h2>
        </div>
        <button
          onClick={onClearCompare}
          className="px-4 py-2 rounded-xl bg-slate-900 border border-slate-800 hover:bg-slate-800 text-rose-400 text-xs font-semibold flex items-center space-x-1.5 transition-colors"
        >
          <Trash2 className="w-3.5 h-3.5" />
          <span>Clear Matrix</span>
        </button>
      </div>

      {/* Comparison Grid Table */}
      <div className="overflow-x-auto rounded-2xl border border-slate-800 glass-panel">
        <table className="w-full text-left border-collapse text-sm">
          <thead>
            <tr className="border-b border-slate-800 bg-slate-950/80">
              <th className="p-4 w-44 text-xs font-bold text-slate-400 uppercase">Device</th>
              {phones.map((p: any) => (
                <th key={p.id} className="p-4 min-w-[220px] align-top">
                  <div className="flex justify-between items-start">
                    <div className="space-y-1">
                      <div className="text-[10px] font-bold text-sky-400 uppercase">{p.brand.name}</div>
                      <div className="font-extrabold text-white text-base leading-tight">{p.model_name}</div>
                      <div className="text-sm font-black text-slate-200 mt-1">
                        ₹{p.prices[0]?.price_amount?.toLocaleString()}
                      </div>
                    </div>
                    <button
                      onClick={() => onRemoveFromCompare(p.id)}
                      className="p-1 rounded-lg text-slate-500 hover:text-rose-400 transition-colors"
                      title="Remove"
                    >
                      ×
                    </button>
                  </div>
                  <div className="w-24 h-28 rounded-lg bg-slate-900 p-2 mt-3 flex items-center justify-center border border-slate-800">
                    <img src={p.canonical_image_url} alt={p.model_name} className="max-h-full max-w-full object-contain" />
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/80">
            {/* Key Advantages */}
            <tr className="bg-sky-950/20">
              <td className="p-4 font-bold text-sky-400 text-xs uppercase">Key Advantages</td>
              {phones.map((p: any) => (
                <td key={p.id} className="p-4 text-xs">
                  {advantages[p.id]?.length > 0 ? (
                    <ul className="space-y-1 text-emerald-400 font-medium">
                      {advantages[p.id].map((adv: string, i: number) => (
                        <li key={i}>✓ {adv}</li>
                      ))}
                    </ul>
                  ) : (
                    <span className="text-slate-500 italic">Balanced baseline</span>
                  )}
                </td>
              ))}
            </tr>

            {/* Processor */}
            <tr>
              <td className="p-4 font-semibold text-slate-400 text-xs">Processor (SoC)</td>
              {phones.map((p: any) => (
                <td key={p.id} className="p-4 text-white font-medium text-xs">
                  {specComp.chipset[p.id]}
                </td>
              ))}
            </tr>

            {/* Display */}
            <tr>
              <td className="p-4 font-semibold text-slate-400 text-xs">Display & Refresh</td>
              {phones.map((p: any) => (
                <td key={p.id} className="p-4 text-slate-300 text-xs">
                  {specComp.display[p.id]}
                </td>
              ))}
            </tr>

            {/* Battery & Charging */}
            <tr>
              <td className="p-4 font-semibold text-slate-400 text-xs">Battery & Charging</td>
              {phones.map((p: any) => (
                <td key={p.id} className="p-4 text-slate-300 text-xs">
                  {specComp.battery[p.id]}
                </td>
              ))}
            </tr>

            {/* Camera */}
            <tr>
              <td className="p-4 font-semibold text-slate-400 text-xs">Primary Camera</td>
              {phones.map((p: any) => (
                <td key={p.id} className="p-4 text-slate-300 text-xs">
                  {specComp.camera[p.id]}
                </td>
              ))}
            </tr>

            {/* Ingress Protection */}
            <tr>
              <td className="p-4 font-semibold text-slate-400 text-xs">IP Rating</td>
              {phones.map((p: any) => (
                <td key={p.id} className="p-4 text-slate-300 text-xs">
                  {specComp.ip_rating[p.id]}
                </td>
              ))}
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};
