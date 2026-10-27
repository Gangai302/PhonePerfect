import React, { useState, useEffect } from 'react';
import { PhoneDetail, RiskReport } from '../types';
import { api } from '../services/api';
import { ArrowLeft, ShieldCheck, AlertTriangle, CheckCircle2, ExternalLink, Scale, Sparkles } from 'lucide-react';

interface PhoneProfileProps {
  phoneId: string;
  onBack: () => void;
  onAddToCompare: (phoneId: string) => void;
}

export const PhoneProfile: React.FC<PhoneProfileProps> = ({
  phoneId,
  onBack,
  onAddToCompare
}) => {
  const [phone, setPhone] = useState<PhoneDetail | null>(null);
  const [risk, setRisk] = useState<RiskReport | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    loadData();
  }, [phoneId]);

  const loadData = async () => {
    setLoading(true);
    try {
      const [pData, rData] = await Promise.all([
        api.getPhoneDetail(phoneId),
        api.getRiskReport(phoneId)
      ]);
      setPhone(pData);
      setRisk(rData);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  if (loading || !phone) {
    return (
      <div className="py-24 text-center text-slate-500 font-mono text-sm animate-pulse">
        Loading device profile telemetry...
      </div>
    );
  }

  const spec = phone.specification;
  const bestPrice = phone.prices && phone.prices.length > 0 ? phone.prices[0].price_amount : 0;

  return (
    <div className="space-y-8 pb-16 max-w-5xl mx-auto">
      {/* Back button */}
      <button
        onClick={onBack}
        className="inline-flex items-center space-x-1.5 text-xs font-semibold text-slate-400 hover:text-sky-400 transition-colors"
      >
        <ArrowLeft className="w-3.5 h-3.5" />
        <span>Return to Catalog / Recommendations</span>
      </button>

      {/* Main Hero Header */}
      <div className="p-6 md:p-8 rounded-3xl glass-panel border border-slate-800 flex flex-col md:flex-row gap-8 items-start">
        <div className="w-full md:w-56 h-64 rounded-2xl bg-slate-950 p-4 border border-slate-800 flex items-center justify-center flex-shrink-0">
          <img
            src={phone.canonical_image_url}
            alt={phone.model_name}
            className="max-h-full max-w-full object-contain"
          />
        </div>

        <div className="flex-1 space-y-4">
          <div>
            <div className="text-xs font-bold text-sky-400 uppercase tracking-widest">{phone.brand.name}</div>
            <h1 className="text-3xl md:text-4xl font-extrabold text-white mt-0.5">{phone.model_name}</h1>
            <div className="text-xs text-slate-400 mt-1">Release Year: {phone.release_year}</div>
          </div>

          <div className="flex items-baseline space-x-3">
            <span className="text-3xl font-black text-white">₹{bestPrice.toLocaleString()}</span>
            <span className="text-xs font-semibold text-emerald-400 px-2 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/20">
              Verified Catalog Price
            </span>
          </div>

          {/* Quick specs grid */}
          {spec && (
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 pt-2">
              <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
                <div className="text-[10px] text-slate-500 font-medium">Processor SoC</div>
                <div className="text-xs font-bold text-slate-200 mt-0.5 truncate">{spec.chipset}</div>
              </div>
              <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
                <div className="text-[10px] text-slate-500 font-medium">Display</div>
                <div className="text-xs font-bold text-slate-200 mt-0.5">{spec.display_size_in}" {spec.display_tech} {spec.refresh_rate_hz}Hz</div>
              </div>
              <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
                <div className="text-[10px] text-slate-500 font-medium">Battery & Wattage</div>
                <div className="text-xs font-bold text-slate-200 mt-0.5">{spec.battery_mah}mAh ({intFormat(spec.charging_wattage)}W)</div>
              </div>
              <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
                <div className="text-[10px] text-slate-500 font-medium">Primary Camera</div>
                <div className="text-xs font-bold text-slate-200 mt-0.5">{spec.rear_camera_primary_mp}MP (OIS: {spec.rear_camera_has_ois ? 'Yes' : 'No'})</div>
              </div>
            </div>
          )}

          {/* Action CTAs */}
          <div className="flex flex-wrap gap-3 pt-3">
            <a
              href={`https://www.amazon.in/s?k=${encodeURIComponent(phone.brand.name + ' ' + phone.model_name)}`}
              target="_blank"
              rel="noopener noreferrer"
              className="px-6 py-3 rounded-xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 font-bold text-xs flex items-center space-x-2 transition-all shadow-md"
            >
              <span>Search on Amazon India</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
            <button
              onClick={() => onAddToCompare(phone.id)}
              className="px-5 py-3 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 font-semibold text-xs flex items-center space-x-2 transition-all"
            >
              <Scale className="w-3.5 h-3.5" />
              <span>Add to Comparison</span>
            </button>
          </div>
        </div>
      </div>

      {/* Transparent Purchase Risk Analysis Module */}
      {risk && (
        <section className="p-6 md:p-8 rounded-3xl glass-panel border border-slate-800 space-y-6">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 flex items-center justify-center">
                <ShieldCheck className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-white">Purchase-Risk Audit Report</h3>
                <p className="text-xs text-slate-400">Independent risk evaluation based on 4-point verification parameters</p>
              </div>
            </div>

            <div className={`px-4 py-1.5 rounded-full text-xs font-black tracking-wider uppercase border ${
              risk.overall_risk_level === 'LOW'
                ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                : risk.overall_risk_level === 'MODERATE'
                ? 'bg-amber-500/10 text-amber-400 border-amber-500/30'
                : 'bg-rose-500/10 text-rose-400 border-rose-500/30'
            }`}>
              {risk.overall_risk_level} RISK ({risk.overall_risk_score}/100)
            </div>
          </div>

          {/* Risk Factors List */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider">Identified Risk Telemetry</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {risk.factors.map((f, i) => (
                <div key={i} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-1.5">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-white">{f.name}</span>
                    <span className={`text-[10px] font-semibold px-2 py-0.5 rounded ${
                      f.severity === 'LOW' ? 'text-slate-400 bg-slate-800' : 'text-amber-400 bg-amber-500/10'
                    }`}>
                      {f.severity}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400">{f.description}</p>
                  <div className="text-[11px] text-sky-400 font-semibold pt-1">
                    Action: {f.action_item}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Buyer Checklist */}
          <div className="p-4 rounded-2xl bg-slate-950/40 border border-slate-800 space-y-2">
            <h4 className="text-xs font-bold text-emerald-400 flex items-center space-x-1.5">
              <CheckCircle2 className="w-3.5 h-3.5" />
              <span>Smart Buyer Inspection Checklist</span>
            </h4>
            <ul className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs text-slate-300">
              {risk.buyer_checklist.map((item, i) => (
                <li key={i} className="flex items-center space-x-2">
                  <span className="text-emerald-400 font-bold">✓</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>
        </section>
      )}
    </div>
  );
};

function intFormat(val: number) {
  return Math.round(val);
}
