import React, { useState, useEffect } from 'react';
import { PhoneCard, Brand } from '../types';
import { api } from '../services/api';
import { Search, Filter, SlidersHorizontal, Scale, ArrowRight } from 'lucide-react';

interface DiscoveryCatalogProps {
  onSelectPhone: (phoneId: string) => void;
  onAddToCompare: (phoneId: string) => void;
}

export const DiscoveryCatalog: React.FC<DiscoveryCatalogProps> = ({
  onSelectPhone,
  onAddToCompare
}) => {
  const [phones, setPhones] = useState<PhoneCard[]>([]);
  const [brands, setBrands] = useState<Brand[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [search, setSearch] = useState<string>('');
  const [selectedBrand, setSelectedBrand] = useState<string>('');
  const [selectedTier, setSelectedTier] = useState<string>('');
  const [page, setPage] = useState<number>(1);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [totalCount, setTotalCount] = useState<number>(0);

  useEffect(() => {
    loadBrands();
  }, []);

  useEffect(() => {
    loadCatalog();
  }, [page, selectedBrand, selectedTier]);

  const loadBrands = async () => {
    try {
      const data = await api.getBrands();
      setBrands(data);
    } catch (e) {
      console.error(e);
    }
  };

  const loadCatalog = async () => {
    setLoading(true);
    try {
      const data = await api.getCatalog({
        page,
        limit: 24,
        brand: selectedBrand || undefined,
        search: search.trim() || undefined,
        chipset_tier: selectedTier || undefined
      });
      setPhones(data.items);
      setTotalPages(data.pages);
      setTotalCount(data.total);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(1);
    loadCatalog();
  };

  return (
    <div className="space-y-6 pb-16">
      {/* Search & Filter Bar */}
      <div className="p-6 rounded-2xl glass-panel border border-slate-800 space-y-4">
        <form onSubmit={handleSearchSubmit} className="flex gap-3">
          <div className="relative flex-1">
            <Search className="w-5 h-5 text-slate-500 absolute left-3.5 top-1/2 transform -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search phone name, brand, or processor..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-11 pr-4 py-3 rounded-xl bg-slate-900 border border-slate-800 text-white placeholder-slate-500 focus:outline-none focus:border-sky-500 text-sm"
            />
          </div>
          <button
            type="submit"
            className="px-6 py-3 rounded-xl bg-sky-500 hover:bg-sky-400 text-slate-950 font-bold text-sm transition-all shadow-md shadow-sky-500/20"
          >
            Search
          </button>
        </form>

        {/* Filter Pills */}
        <div className="flex flex-wrap items-center gap-2 pt-2 border-t border-slate-800/80">
          <span className="text-xs text-slate-400 font-semibold mr-2 flex items-center gap-1">
            <Filter className="w-3.5 h-3.5" /> Brands:
          </span>
          <button
            onClick={() => { setSelectedBrand(''); setPage(1); }}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all ${
              selectedBrand === ''
                ? 'bg-sky-500 text-slate-950 border-sky-400'
                : 'bg-slate-900 text-slate-400 border-slate-800 hover:border-slate-700'
            }`}
          >
            All Brands
          </button>
          {brands.slice(0, 8).map((b) => (
            <button
              key={b.id}
              onClick={() => { setSelectedBrand(b.id); setPage(1); }}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all ${
                selectedBrand === b.id
                  ? 'bg-sky-500 text-slate-950 border-sky-400'
                  : 'bg-slate-900 text-slate-400 border-slate-800 hover:border-slate-700'
              }`}
            >
              {b.name}
            </button>
          ))}
        </div>
      </div>

      {/* Catalog Grid Header */}
      <div className="flex items-center justify-between text-xs text-slate-400 px-1">
        <span>Showing {phones.length} of {totalCount} Smartphones</span>
        <span>Page {page} of {totalPages}</span>
      </div>

      {/* Phone Cards Grid */}
      {loading ? (
        <div className="py-20 text-center text-slate-500 font-mono text-sm animate-pulse">
          Loading smartphone catalog...
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5">
          {phones.map((phone) => (
            <div
              key={phone.id}
              className="rounded-2xl border border-slate-800 bg-slate-900/60 hover:border-slate-700 hover:bg-slate-900/90 transition-all p-4 flex flex-col justify-between group"
            >
              <div>
                <div className="w-full h-44 rounded-xl bg-slate-950/70 p-3 flex items-center justify-center overflow-hidden mb-3 border border-slate-800/80">
                  <img
                    src={phone.canonical_image_url}
                    alt={phone.model_name}
                    className="max-h-full max-w-full object-contain group-hover:scale-105 transition-transform"
                    loading="lazy"
                  />
                </div>
                <div className="text-[10px] font-bold text-sky-400 uppercase tracking-wider">{phone.brand_name}</div>
                <h4 className="font-bold text-white text-base truncate mt-0.5" title={phone.model_name}>
                  {phone.model_name}
                </h4>

                <div className="mt-3 space-y-1 text-xs text-slate-400">
                  <div className="truncate">⚡ {phone.chipset || 'Octa-Core SoC'}</div>
                  <div>💾 {phone.ram_gb}GB RAM / {phone.storage_gb}GB</div>
                  <div>🔋 {phone.battery_mah}mAh Battery</div>
                </div>
              </div>

              <div className="mt-5 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <div>
                  <div className="text-lg font-black text-white">
                    {phone.best_price ? `₹${phone.best_price.toLocaleString()}` : 'Price on check'}
                  </div>
                  <span className="text-[9px] font-semibold text-emerald-400 uppercase">{phone.price_verification}</span>
                </div>
                <div className="flex gap-1.5">
                  <button
                    onClick={() => onAddToCompare(phone.id)}
                    className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors"
                    title="Add to Compare"
                  >
                    <Scale className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => onSelectPhone(phone.id)}
                    className="p-2 rounded-lg bg-sky-500 hover:bg-sky-400 text-slate-950 transition-colors"
                    title="View Full Profile"
                  >
                    <ArrowRight className="w-4 h-4 font-bold" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Pagination Controls */}
      <div className="flex justify-center items-center gap-2 pt-6">
        <button
          onClick={() => setPage((p) => Math.max(1, p - 1))}
          disabled={page <= 1}
          className="px-4 py-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 text-xs font-semibold disabled:opacity-30"
        >
          Previous
        </button>
        <span className="text-xs text-slate-400 font-mono px-3">
          {page} / {totalPages}
        </span>
        <button
          onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
          disabled={page >= totalPages}
          className="px-4 py-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 text-xs font-semibold disabled:opacity-30"
        >
          Next
        </button>
      </div>
    </div>
  );
};
