/**
 * PhonePerfect – Live E-Commerce Smartphone Price Sync & Deal Tracker
 */
const LivePriceService = {
  API_BASE_URL: 'http://127.0.0.1:5055',
  _cacheKey: 'phonePerfectLivePrices',
  _cache: null,
  _isOnline: navigator.onLine !== false,

  init() {
    try {
      const stored = localStorage.getItem(this._cacheKey);
      this._cache = stored ? JSON.parse(stored) : {};
    } catch (e) {
      this._cache = {};
    }

    window.addEventListener('online', () => {
      this._isOnline = true;
      this.refreshAllVisiblePrices();
    });

    window.addEventListener('offline', () => {
      this._isOnline = false;
    });
  },

  getCache() {
    if (!this._cache) this.init();
    return this._cache;
  },

  saveCache() {
    try {
      localStorage.setItem(this._cacheKey, JSON.stringify(this._cache));
    } catch (e) {}
  },

  getCanonicalPrice(phone) {
    if (!phone) {
      return {
        price: 0,
        priceDisplay: 'Latest price unavailable',
        isLive: false,
        lastChecked: 'Unavailable',
        availability: 'Unavailable',
        merchant: '',
        deal: '',
        asin: 'N/A',
        isUnavailable: true
      };
    }

    const cache = this.getCache();
    const pid = phone.id;
    const asin = phone.asin;

    // Check live cached price entry
    const entry = (asin && cache[asin]) || (pid && cache[pid]);
    if (entry && typeof entry.price === 'number' && entry.price > 0) {
      return {
        price: entry.price,
        priceDisplay: `₹${entry.price.toLocaleString('en-IN')}`,
        isLive: !!entry.is_live && this._isOnline,
        lastChecked: entry.last_checked || entry.timestamp || 'Recently',
        availability: entry.availability || 'In Stock',
        merchant: entry.merchant || 'Amazon Retail India',
        deal: entry.deal_label || '',
        asin: entry.asin || asin,
        isUnavailable: false
      };
    }

    // Baseline catalog price
    const basePrice = (typeof phone.price_numeric === 'number' && phone.price_numeric > 0)
      ? phone.price_numeric
      : (typeof phone.current_price === 'number' && phone.current_price > 0 
          ? phone.current_price 
          : (typeof phone.market_price === 'number' && phone.market_price > 0 ? phone.market_price : 0));

    if (basePrice > 0) {
      return {
        price: basePrice,
        priceDisplay: `₹${basePrice.toLocaleString('en-IN')}`,
        isLive: false,
        lastChecked: 'Last known catalog price',
        availability: 'In Stock',
        merchant: 'Amazon Retail India',
        deal: '',
        asin: asin || 'N/A',
        isUnavailable: false
      };
    }

    return {
      price: 0,
      priceDisplay: 'Latest price unavailable',
      isLive: false,
      lastChecked: 'Unavailable',
      availability: 'Unavailable',
      merchant: '',
      deal: '',
      asin: asin || 'N/A',
      isUnavailable: true
    };
  },

  async fetchLivePrice(phone, force = false) {
    if (!phone) return null;
    const identifier = phone.asin || phone.id;
    if (!identifier) return null;

    try {
      const url = `${this.API_BASE_URL}/api/price/${encodeURIComponent(identifier)}${force ? '?refresh=true' : ''}`;
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 3500);

      const res = await fetch(url, { method: 'GET', headers: { 'Accept': 'application/json' }, signal: controller.signal });
      clearTimeout(timeoutId);

      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      
      if (data && data.success && data.price > 0) {
        // Strict product identity validation
        if (phone.asin && data.asin && data.asin !== phone.asin && phone.id !== data.phone_id) {
          console.warn('Product identifier mismatch on live price response. Rejected.', phone.asin, data.asin);
          return null;
        }

        const cache = this.getCache();
        if (data.asin) cache[data.asin] = data;
        if (data.phone_id) cache[data.phone_id] = data;
        this.saveCache();
        return data;
      }
    } catch (err) {
      // Graceful offline fallback
    }
    return null;
  },

  async fetchBatchLivePrices(phonesArray, force = false) {
    if (!phonesArray || !Array.isArray(phonesArray) || phonesArray.length === 0) return;
    const asins = phonesArray.map(p => p.asin).filter(Boolean);
    const ids = phonesArray.map(p => p.id).filter(Boolean);

    try {
      const url = `${this.API_BASE_URL}/api/prices/batch`;
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 4000);

      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ asins, ids, refresh: force }),
        signal: controller.signal
      });
      clearTimeout(timeoutId);

      if (!res.ok) return;
      const data = await res.json();
      if (data && data.success && data.prices) {
        const cache = this.getCache();
        Object.entries(data.prices).forEach(([k, val]) => {
          if (val && val.price > 0) {
            cache[k] = val;
          }
        });
        this.saveCache();
      }
    } catch (e) {
      // Graceful fallback without blocking UI
    }
  },

  async refreshPhonePrice(phoneId) {
    const phone = (typeof getPhoneById === 'function') ? getPhoneById(phoneId) : null;
    if (!phone) return;
    
    // Show loading indicator
    if (typeof showToast === 'function') {
      showToast('🔄 Fetching latest live price from Amazon India...');
    }

    const res = await this.fetchLivePrice(phone, true);
    if (res && res.price > 0) {
      if (typeof showToast === 'function') {
        showToast(`✅ Price updated to ${res.price_display} (${res.deal_label || 'Live'})`);
      }
    } else {
      if (typeof showToast === 'function') {
        showToast('⚠️ Live price service unavailable. Showing last verified price.');
      }
    }

    if (typeof updateAppAfterPriceRefresh === 'function') {
      updateAppAfterPriceRefresh(phoneId);
    }
  },

  async refreshAllVisiblePrices() {
    if (typeof appState !== 'undefined' && appState.currentScreen === 'screen-results' && typeof generateRecommendations === 'function') {
      generateRecommendations();
    }
  }
};

LivePriceService.init();
window.LivePriceService = LivePriceService;

function renderSparkline(canvas, data, color = '#8b5cf6') {
  if (!canvas || !data || data.length === 0) return;
  const ctx = canvas.getContext('2d');
  const W = canvas.width;
  const H = canvas.height;
  const pad = 4;
  
  ctx.clearRect(0, 0, W, H);
  
  const min = Math.min(...data) * 0.98;
  const max = Math.max(...data) * 1.02;
  const range = max - min || 1;
  
  const points = data.map((v, i) => ({
    x: pad + (i / (data.length - 1)) * (W - pad * 2),
    y: pad + (1 - (v - min) / range) * (H - pad * 2)
  }));
  
  // Gradient fill
  const gradient = ctx.createLinearGradient(0, 0, 0, H);
  gradient.addColorStop(0, color + '40');
  gradient.addColorStop(1, color + '05');
  
  ctx.beginPath();
  ctx.moveTo(points[0].x, H);
  points.forEach(p => ctx.lineTo(p.x, p.y));
  ctx.lineTo(points[points.length - 1].x, H);
  ctx.closePath();
  ctx.fillStyle = gradient;
  ctx.fill();
  
  // Line
  ctx.beginPath();
  points.forEach((p, i) => {
    if (i === 0) ctx.moveTo(p.x, p.y);
    else {
      // Smooth curve
      const prev = points[i - 1];
      const cpx = (prev.x + p.x) / 2;
      ctx.bezierCurveTo(cpx, prev.y, cpx, p.y, p.x, p.y);
    }
  });
  ctx.strokeStyle = color;
  ctx.lineWidth = 2;
  ctx.stroke();
  
  // Current price dot
  const last = points[points.length - 1];
  ctx.beginPath();
  ctx.arc(last.x, last.y, 3, 0, Math.PI * 2);
  ctx.fillStyle = color;
  ctx.fill();
  ctx.strokeStyle = '#fff';
  ctx.lineWidth = 1.5;
  ctx.stroke();
}

// Seeded random number generator
function mulberry32(a) {
  return function() {
    var t = a += 0x6D2B79F5;
    t = Math.imul(t ^ t >>> 15, t | 1);
    t ^= t + Math.imul(t ^ t >>> 7, t | 61);
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  }
}

// Generate a daily simulated live price
function getLivePrice(phone) {
  const basePrice = getPhonePrice(phone);
  // Hash the phone ID into an integer seed
  let idHash = 0;
  for (let i = 0; i < phone.id.length; i++) {
    idHash = Math.imul(31, idHash) + phone.id.charCodeAt(i) | 0;
  }
  
  // Create a daily seed
  const today = new Date();
  const dateSeed = today.getFullYear() * 10000 + (today.getMonth() + 1) * 100 + today.getDate();
  const seed = idHash + dateSeed;
  
  const rng = mulberry32(seed);
  // Fluctuate between -3% and +1%
  const fluctuation = (rng() * 0.04) - 0.03; 
  return Math.round(basePrice * (1 + fluctuation));
}

// Generate or retrieve realistic price history
function getPriceHistory(phone, days = 30) {
  // Check if explicit price history exists on the object
  const existingHist = phone.priceHistory || phone.price_history;
  if (Array.isArray(existingHist) && existingHist.length > 0) {
    return existingHist.map(item => {
      if (typeof item === 'number') return item;
      if (typeof item === 'object' && item !== null && typeof item.price === 'number') return item.price;
      return getPhonePrice(phone);
    });
  }

  const basePrice = getPhonePrice(phone);
  const cat = phone.priceCategory || 3;
  
  let idHash = 0;
  if (phone && phone.id) {
    for (let i = 0; i < phone.id.length; i++) {
      idHash = Math.imul(31, idHash) + phone.id.charCodeAt(i) | 0;
    }
  }
  
  const history = [];
  const today = new Date();
  
  const decayRate = cat >= 4 ? 0.90 : (cat >= 2 ? 0.85 : 0.80);
  
  for (let i = days - 1; i >= 0; i--) {
    const d = new Date(today);
    d.setDate(d.getDate() - i);
    
    const dateSeed = d.getFullYear() * 10000 + (d.getMonth() + 1) * 100 + d.getDate();
    const rng = mulberry32(idHash + dateSeed);
    
    const progress = 1 - (i / days);
    
    const currentBase = basePrice * (1 - ((1 - decayRate) * (1 - progress)));
    const noise = (rng() * 0.06) - 0.03;
    
    history.push(Math.round(currentBase * (1 + noise)));
  }
  return history;
}

// Price alert system using localStorage
function getPriceAlerts() {
  return JSON.parse(localStorage.getItem('phonePerfectAlerts') || '{}');
}

function setPriceAlert(phoneId, targetPrice) {
  const alerts = getPriceAlerts();
  alerts[phoneId] = { targetPrice, setAt: Date.now() };
  localStorage.setItem('phonePerfectAlerts', JSON.stringify(alerts));
}

function removePriceAlert(phoneId) {
  const alerts = getPriceAlerts();
  delete alerts[phoneId];
  localStorage.setItem('phonePerfectAlerts', JSON.stringify(alerts));
}

function hasPriceAlert(phoneId) {
  return !!getPriceAlerts()[phoneId];
}

function togglePriceAlert(phoneId) {
  if (hasPriceAlert(phoneId)) {
    removePriceAlert(phoneId);
    showToast('🔕 Price alert removed');
  } else {
    // Request notification permission if needed
    if ("Notification" in window && Notification.permission !== "granted" && Notification.permission !== "denied") {
      Notification.requestPermission().then(function (permission) {
        if (permission === "granted") {
          setAlertForPhone(phoneId);
        } else {
          showToast('⚠️ Notifications denied. Alert will only work while app is open.');
          setAlertForPhone(phoneId);
        }
      });
    } else {
      setAlertForPhone(phoneId);
    }
  }
}

function setAlertForPhone(phoneId) {
  const phone = PHONES.find(p => p.id === phoneId);
  if (phone) {
    const price = getPhonePrice(phone);
    const target = Math.round(price * 0.9); // Alert at 10% drop
    setPriceAlert(phoneId, target);
    showToast(`🔔 Alert set! We'll notify when price drops below ₹${(target/1000).toFixed(0)}K`);
    
    // Test notification immediately if granted
    if ("Notification" in window && Notification.permission === "granted") {
      new Notification("Alert Set!", {
        body: `We will notify you when ${phone.name} drops below ₹${(target/1000).toFixed(0)}K.`,
        icon: phone.images && phone.images.length > 0 ? phone.images[0] : null
      });
    }
  }
}

function showToast(message) {
  // Remove existing toast
  const existing = document.querySelector('.toast-notification');
  if (existing) existing.remove();
  
  const toast = document.createElement('div');
  toast.className = 'toast-notification';
  toast.innerHTML = message;
  document.body.appendChild(toast);
  
  requestAnimationFrame(() => toast.classList.add('show'));
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}
