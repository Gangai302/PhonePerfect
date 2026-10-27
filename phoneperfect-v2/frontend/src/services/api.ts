import { PhoneCard, PhoneDetail, Brand, RecommendationRequest, RecommendationResponse, RiskReport } from '../types';

const API_BASE = '/api/v1';

export const api = {
  // Health
  getHealth: async () => {
    const res = await fetch(`${API_BASE}/health`);
    if (!res.ok) throw new Error('Failed to fetch API health');
    return res.json();
  },

  // Brands
  getBrands: async (): Promise<Brand[]> => {
    const res = await fetch(`${API_BASE}/brands`);
    if (!res.ok) throw new Error('Failed to fetch brands');
    return res.json();
  },

  // Catalog
  getCatalog: async (params: {
    page?: number;
    limit?: number;
    brand?: string;
    search?: string;
    min_price?: number;
    max_price?: number;
    chipset_tier?: string;
  }): Promise<{ items: PhoneCard[]; total: number; page: number; pages: number }> => {
    const query = new URLSearchParams();
    if (params.page) query.append('page', params.page.toString());
    if (params.limit) query.append('limit', params.limit.toString());
    if (params.brand) query.append('brand', params.brand);
    if (params.search) query.append('search', params.search);
    if (params.min_price) query.append('min_price', params.min_price.toString());
    if (params.max_price) query.append('max_price', params.max_price.toString());
    if (params.chipset_tier) query.append('chipset_tier', params.chipset_tier);

    const res = await fetch(`${API_BASE}/catalog?${query.toString()}`);
    if (!res.ok) throw new Error('Failed to fetch catalog');
    return res.json();
  },

  // Phone Details
  getPhoneDetail: async (phoneId: string): Promise<PhoneDetail> => {
    const res = await fetch(`${API_BASE}/catalog/${phoneId}`);
    if (!res.ok) throw new Error('Failed to fetch phone detail');
    return res.json();
  },

  // Recommendation Engine
  getRecommendations: async (req: RecommendationRequest): Promise<RecommendationResponse> => {
    const res = await fetch(`${API_BASE}/recommendations`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(req)
    });
    if (!res.ok) throw new Error('Failed to compute recommendations');
    return res.json();
  },

  // Compare Phones
  comparePhones: async (phoneIds: string[]): Promise<any> => {
    const res = await fetch(`${API_BASE}/compare`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phone_ids: phoneIds })
    });
    if (!res.ok) throw new Error('Failed to generate comparison matrix');
    return res.json();
  },

  // Purchase-Risk Assessment
  getRiskReport: async (phoneId: string): Promise<RiskReport> => {
    const res = await fetch(`${API_BASE}/risk/${phoneId}`);
    if (!res.ok) throw new Error('Failed to retrieve risk report');
    return res.json();
  },

  // Price Tracking
  getPricing: async (phoneId: string): Promise<any> => {
    const res = await fetch(`${API_BASE}/pricing/${phoneId}`);
    if (!res.ok) throw new Error('Failed to retrieve pricing telemetry');
    return res.json();
  }
};
