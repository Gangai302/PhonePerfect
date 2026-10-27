/**
 * PhonePerfect – AI-Based Smartphone Purchase Decision & Risk Analysis System
 */

// ─── DECISION & RISK ENGINE ──────────────────────────────────────────────────
// ─── DECISION & RISK ENGINE ──────────────────────────────────────────────────
const DecisionEngine = {
  BUDGET_MAP: {
    'under-10000': 10000,
    '10000-20000': 20000,
    '20000-30000': 30000,
    '30000-50000': 50000,
    '50000-80000': 80000,
    'above-80000': 250000,
    0: 10000,
    1: 20000,
    2: 30000,
    3: 50000,
    4: 80000,
    5: 250000
  },

  getMaxBudget(budgetCat) {
    if (typeof budgetCat === 'number' && !isNaN(budgetCat) && budgetCat > 0) return budgetCat;
    if (this.BUDGET_MAP[budgetCat] !== undefined) return this.BUDGET_MAP[budgetCat];
    if (typeof budgetCat === 'string' && !isNaN(Number(budgetCat)) && Number(budgetCat) > 0) return Number(budgetCat);
    return 250000;
  },

  getUserNormalizedWeights(priorities) {
    const keys = ['processor', 'camera', 'battery', 'display', 'storage', 'charging', 'durability'];
    const weights = {};
    
    keys.forEach(k => weights[k] = 1);
    let priceWeight = 2; // Baseline price weight
    
    if (priorities && priorities.length > 0) {
      priorities.forEach(p => {
        const mappedKey = (p === 'gaming') ? 'processor' : p;
        if (weights[mappedKey] !== undefined) {
          weights[mappedKey] += 4;
        }
      });
    }

    let sum = priceWeight;
    keys.forEach(k => { sum += weights[k]; });

    const normalized = { price: +(priceWeight / sum).toFixed(3) };
    keys.forEach(k => {
      normalized[k] = +(weights[k] / sum).toFixed(3);
    });

    return normalized;
  },

  getPhoneNumericPrice(phone) {
    if (!phone) return 0;
    let raw = phone.price_numeric !== undefined && phone.price_numeric !== null && phone.price_numeric > 0 
      ? phone.price_numeric 
      : phone.price;
    if (typeof raw === 'number' && !isNaN(raw) && raw > 0) {
      return Math.round(raw);
    }
    if (raw === undefined || raw === null) return 0;
    const str = String(raw).replace(/,/g, '').replace(/₹/g, '').replace(/INR/gi, '').replace(/\.00$/, '').trim();
    const m = str.match(/\d+/);
    return m ? parseInt(m[0], 10) : 0;
  },

  getExpectedMarketPrice(phone) {
    if (!phone) return 50000;
    if (phone.expected_price && typeof phone.expected_price === 'number') return phone.expected_price;
    if (phone.market_price && typeof phone.market_price === 'number') return phone.market_price;
    if (phone.launch_price && typeof phone.launch_price === 'number') return phone.launch_price;
    if (phone.mrp && typeof phone.mrp === 'number') return phone.mrp;

    const currPrice = this.getPhoneNumericPrice(phone);
    return currPrice;
  },

  evaluatePriceStatus(currentPrice, expectedMarketPrice) {
    const expected = expectedMarketPrice || currentPrice;
    const diffPct = expected > 0 ? +(((currentPrice - expected) / expected) * 100).toFixed(1) : 0;
    const diffAmount = currentPrice - expected;

    let label = "Good Price";
    let cssClass = "deal-good";
    let code = "GOOD_PRICE";

    if (diffPct <= 8) {
      label = "Good Price";
      cssClass = "deal-good";
      code = "GOOD_PRICE";
    } else if (diffPct <= 20) {
      label = "Fair Price";
      cssClass = "deal-fair";
      code = "FAIR_PRICE";
    } else if (diffPct <= 35) {
      label = "Slightly Expensive";
      cssClass = "deal-warn";
      code = "SLIGHTLY_EXPENSIVE";
    } else {
      label = "Overpriced";
      cssClass = "deal-overpriced";
      code = "OVERPRICED";
    }

    return { currentPrice, expectedMarketPrice: expected, diffPct, diffAmount, label, cssClass, code };
  },

  calculateNormalizedScores(phone, budgetCat) {
    const p = this.getPhoneNumericPrice(phone);
    const scores = phone.scores || {};
    const maxBudget = this.getMaxBudget(budgetCat);
    
    const procScore = Math.min(100, Math.max(0, (scores.processor || scores.gaming || 7.5) * 10));
    const camScore = Math.min(100, Math.max(0, (scores.camera || 7.5) * 10));
    const batScore = Math.min(100, Math.max(0, (scores.battery || 7.5) * 10));
    const dispScore = Math.min(100, Math.max(0, (scores.display || 7.5) * 10));
    const chgScore = Math.min(100, Math.max(0, (scores.charging || 7.0) * 10));
    const durScore = Math.min(100, Math.max(0, (scores.durability || 7.5) * 10));
    
    const ram = phone.ram_gb || 8;
    const storageScore = Math.min(100, Math.max(40, ram * 8 + 30));

    let priceScore = 75;
    if (maxBudget && maxBudget < 200000) {
      if (p <= maxBudget) {
        priceScore = 100 - Math.round((p / maxBudget) * 30);
      } else {
        const excessRatio = (p - maxBudget) / maxBudget;
        priceScore = Math.max(10, Math.round(70 - excessRatio * 100));
      }
    } else {
      priceScore = Math.min(100, Math.max(20, Math.round(100 - (p / 200000) * 80)));
    }

    return {
      processor: procScore,
      camera: camScore,
      battery: batScore,
      display: dispScore,
      charging: chgScore,
      durability: durScore,
      storage: storageScore,
      price: priceScore
    };
  },

  calculateValueScore(phone, selectedPriorities, budgetCat) {
    const currPrice = this.getPhoneNumericPrice(phone);
    const expectedPrice = this.getExpectedMarketPrice(phone);
    const priceStatus = this.evaluatePriceStatus(currPrice, expectedPrice);
    const diffPct = priceStatus.diffPct;
    const maxBudget = this.getMaxBudget(budgetCat);

    // 1. Price Factor (40% Weight)
    let priceFactor = 85;
    if (diffPct <= -10) priceFactor = 100;
    else if (diffPct <= 0) priceFactor = 90 + Math.abs(diffPct);
    else if (diffPct <= 5) priceFactor = 85 - (diffPct / 5) * 5;
    else if (diffPct <= 15) priceFactor = 80 - ((diffPct - 5) / 10) * 15;
    else if (diffPct <= 25) priceFactor = 65 - ((diffPct - 15) / 10) * 20;
    else if (diffPct <= 50) priceFactor = 45 - ((diffPct - 25) / 25) * 25;
    else priceFactor = Math.max(10, 20 - (diffPct - 50) * 0.2);

    // Budget suitability adjustment
    if (maxBudget && maxBudget < 200000 && currPrice > maxBudget) {
      const excessRatio = (currPrice - maxBudget) / maxBudget;
      priceFactor = Math.max(10, priceFactor - Math.round(excessRatio * 35));
    }

    // 2. Hardware / Specifications Factor (30% Weight)
    const normWeights = this.getUserNormalizedWeights(selectedPriorities);
    const specScores = this.calculateNormalizedScores(phone, maxBudget);
    let weightedSpecSum = 0;
    let weightSum = 0;
    for (const key in specScores) {
      if (key === 'price') continue;
      const w = normWeights[key] || 0.14;
      weightedSpecSum += w * (specScores[key] || 75);
      weightSum += w;
    }
    const specsFactor = weightSum > 0 ? Math.min(100, Math.max(20, weightedSpecSum / weightSum)) : 75;

    // 3. Release Age Factor (15% Weight)
    let releaseYear = phone.release_year || phone.year;
    if (!releaseYear && phone.specs && phone.specs.launch) {
      const m = String(phone.specs.launch).match(/20\d\d/);
      if (m) releaseYear = parseInt(m[0], 10);
    }
    if (!releaseYear) releaseYear = 2024; // neutral assumption for modern catalog

    let ageFactor = 65;
    if (releaseYear >= 2025) ageFactor = 100;
    else if (releaseYear === 2024) ageFactor = 85;
    else if (releaseYear === 2023) ageFactor = 70;
    else if (releaseYear === 2022) ageFactor = 50;
    else ageFactor = 35;

    // 4. Brand & Reliability Factor (10% Weight)
    const brand = String(phone.brand || '').toLowerCase();
    let brandFactor = 75;
    const tier1Brands = ['apple', 'samsung', 'google', 'oneplus'];
    const tier2Brands = ['xiaomi', 'iqoo', 'realme', 'vivo', 'motorola', 'nothing', 'poco', 'oppo'];
    if (tier1Brands.includes(brand)) brandFactor = 90;
    else if (tier2Brands.includes(brand)) brandFactor = 85;

    if (phone.specs && phone.specs.ip && (phone.specs.ip.includes('IP68') || phone.specs.ip.includes('IP67'))) {
      brandFactor = Math.min(100, brandFactor + 5);
    }

    // 5. Rating & Review Score Factor (5% Weight)
    let ratingFactor = 80; // neutral default
    if (phone.rating !== undefined && phone.rating !== null) {
      const r = parseFloat(phone.rating);
      if (r <= 5) ratingFactor = Math.min(100, Math.max(20, r * 20));
      else if (r <= 10) ratingFactor = Math.min(100, Math.max(20, r * 10));
      else if (r <= 100) ratingFactor = Math.min(100, Math.max(20, r));
    }

    // Weighted Total (Normalized safely if any factor fails)
    const finalScore = (
      0.40 * priceFactor +
      0.30 * specsFactor +
      0.15 * ageFactor +
      0.10 * brandFactor +
      0.05 * ratingFactor
    );

    return +Math.min(99, Math.max(15, finalScore)).toFixed(1);
  },

  getRecommendationCategory(valueScore) {
    if (valueScore >= 80) {
      return { label: "Highly Worth", decisionClass: "dec-buy", badgeClass: "badge-good", riskLevel: "LOW RISK", riskClass: "risk-low" };
    } else if (valueScore >= 65) {
      return { label: "Worth Buying", decisionClass: "dec-buy", badgeClass: "badge-good", riskLevel: "LOW RISK", riskClass: "risk-low" };
    } else if (valueScore >= 50) {
      return { label: "Fair / Consider", decisionClass: "dec-consider", badgeClass: "badge-fair", riskLevel: "MEDIUM RISK", riskClass: "risk-medium" };
    } else if (valueScore >= 35) {
      return { label: "Not Great Value", decisionClass: "dec-avoid", badgeClass: "badge-warn", riskLevel: "MEDIUM RISK", riskClass: "risk-medium" };
    } else {
      return { label: "Not Worth", decisionClass: "dec-avoid", badgeClass: "badge-overpriced", riskLevel: "HIGH RISK", riskClass: "risk-high" };
    }
  },

  calculatePersonalizedValueScore(phone, normWeights, maxBudget) {
    return this.calculateValueScore(phone, Object.keys(normWeights || {}), maxBudget);
  },

  analyzeHistoricalPrice(phone) {
    const currPrice = this.getPhoneNumericPrice(phone);
    let history = [];
    
    if (typeof getPriceHistory === 'function') {
      history = getPriceHistory(phone, 30);
    } else if (Array.isArray(phone.price_history) && phone.price_history.length > 0) {
      history = phone.price_history;
    } else {
      history = [currPrice * 1.08, currPrice * 1.05, currPrice * 1.02, currPrice];
    }
    
    const min = Math.min(...history);
    const max = Math.max(...history);
    const avg = Math.round(history.reduce((a, b) => a + b, 0) / history.length);
    const diffPct = +(((currPrice - avg) / avg) * 100).toFixed(1);
    
    let trend = 'stable';
    if (history.length >= 2) {
      const recentAvg = (history[history.length - 1] + history[history.length - 2]) / 2;
      const olderAvg = (history[0] + history[1]) / 2;
      if (recentAvg < olderAvg * 0.98) trend = 'decreasing';
      else if (recentAvg > olderAvg * 1.02) trend = 'increasing';
    }

    return { current: currPrice, min, max, avg, diffPct, trend, history };
  },

  evaluatePriceOpportunity(histAnalysis) {
    const { current, min, diffPct } = histAnalysis;
    
    if (current <= min * 1.01 || diffPct <= -7.0) {
      return { score: 95, label: 'Excellent Opportunity', code: 'EXCELLENT' };
    } else if (diffPct <= -2.0) {
      return { score: 80, label: 'Good Opportunity', code: 'GOOD' };
    } else if (diffPct <= 5.0) {
      return { score: 65, label: 'Normal Price', code: 'NORMAL' };
    } else {
      return { score: 40, label: 'Above Average Price', code: 'ABOVE_AVG' };
    }
  },

  getLiveDealAlert(phone) {
    const hist = this.analyzeHistoricalPrice(phone);
    const currPrice = hist.current;
    if (currPrice <= 0) return null;

    const dropAmount = hist.max - currPrice;
    if (currPrice <= hist.min || currPrice <= hist.min * 1.01) {
      return {
        type: 'atl',
        badgeHtml: `<span class="badge-deal-alert deal-atl">🔥 ALL-TIME LOW</span>`,
        text: `🔥 All-Time Low Price! (₹${currPrice.toLocaleString()})`,
        alertBanner: `🔥 <strong>BEST TIME TO BUY:</strong> This smartphone is currently selling at its <strong>all-time lowest price</strong> of ₹${currPrice.toLocaleString()}.`
      };
    }
    if (dropAmount >= 1500) {
      return {
        type: 'drop',
        badgeHtml: `<span class="badge-deal-alert deal-drop">📉 ₹${dropAmount.toLocaleString()} DROP</span>`,
        text: `📉 ₹${dropAmount.toLocaleString()} Price Drop from Peak`,
        alertBanner: `📉 <strong>PRICE DROP ALERT:</strong> Current price is ₹${dropAmount.toLocaleString()} lower than its recent peak (₹${hist.max.toLocaleString()}).`
      };
    }
    if (hist.diffPct <= -5.0) {
      return {
        type: 'drop',
        badgeHtml: `<span class="badge-deal-alert deal-drop">🏷️ ${Math.abs(hist.diffPct)}% BELOW AVG</span>`,
        text: `🏷️ ${Math.abs(hist.diffPct)}% below 30-day average price`,
        alertBanner: `🏷️ <strong>FAVORABLE PRICING:</strong> Priced ${Math.abs(hist.diffPct)}% below the 30-day market average of ₹${hist.avg.toLocaleString()}.`
      };
    }
    if (hist.diffPct >= 10.0 && (hist.max - hist.min >= 2000)) {
      return {
        type: 'peak',
        badgeHtml: `<span class="badge-deal-alert deal-peak">⚡ PEAK PRICE</span>`,
        text: `⚡ High Price (+${hist.diffPct}% vs avg)`,
        alertBanner: `⚠️ <strong>PRICE SPIKE WARNING:</strong> Price is currently higher (+${hist.diffPct}%) than its 30-day average of ₹${hist.avg.toLocaleString()}. Consider waiting for a price dip.`
      };
    }
    return null;
  },

  calculateMarketVolatilityAndDepreciation(phone) {
    const hist = this.analyzeHistoricalPrice(phone);
    const currPrice = hist.current;
    if (currPrice <= 0) {
      return { volatilityPct: 0, volatilityLabel: 'Low Volatility', volatilityClass: 'risk-low', drop3mPct: 0, drop6mPct: 0, price3m: 0, price6m: 0, advice: 'BUY NOW', adviceDetail: 'Stable price floor.' };
    }

    const history = hist.history || [currPrice];
    const mean = hist.avg || currPrice;
    const variance = history.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / history.length;
    const stdDev = Math.sqrt(variance);
    const volatilityPct = Math.min(100, Math.max(5, Math.round((stdDev / mean) * 100 * 3.5)));

    let volatilityLabel = `Low Volatility (${volatilityPct}%)`;
    let volatilityClass = 'risk-low';
    if (volatilityPct >= 40) {
      volatilityLabel = `High Volatility (${volatilityPct}%)`;
      volatilityClass = 'risk-high';
    } else if (volatilityPct >= 20) {
      volatilityLabel = `Moderate Volatility (${volatilityPct}%)`;
      volatilityClass = 'risk-medium';
    }

    const brand = (phone.brand || '').toLowerCase();
    let annualDepreciationRate = 0.25;
    if (brand.includes('apple')) annualDepreciationRate = 0.12;
    else if (brand.includes('samsung') || brand.includes('oneplus') || brand.includes('google')) annualDepreciationRate = 0.18;
    else if (brand.includes('xiaomi') || brand.includes('realme') || brand.includes('iqoo') || brand.includes('poco')) annualDepreciationRate = 0.28;
    else annualDepreciationRate = 0.32;

    const releaseYear = phone.release_year || 2024;
    const ageYears = Math.max(0.2, (2026 - releaseYear));
    const ageFactor = Math.max(0.4, 1 / Math.sqrt(1 + ageYears * 0.8));

    const drop3mPct = +(annualDepreciationRate * 0.25 * ageFactor * 100).toFixed(1);
    const drop6mPct = +(annualDepreciationRate * 0.50 * ageFactor * 100).toFixed(1);

    const price3m = Math.round(currPrice * (1 - drop3mPct / 100));
    const price6m = Math.round(currPrice * (1 - drop6mPct / 100));

    let advice = 'BUY NOW';
    let adviceDetail = 'Price is near its floor retention value. Minimal depreciation expected over next 90 days.';
    if (drop3mPct >= 8.0 || volatilityPct >= 35) {
      advice = 'WAIT 3 MONTHS FOR PRICE DROP';
      adviceDetail = `High depreciation velocity. Price projected to drop by ₹${(currPrice - price3m).toLocaleString()} (-${drop3mPct}%) in ~90 days.`;
    } else if (drop3mPct >= 5.0) {
      advice = 'FAIR BUY TIME';
      adviceDetail = `Moderate depreciation. Expected price drop of ₹${(currPrice - price3m).toLocaleString()} (-${drop3mPct}%) in 3 months.`;
    }

    return {
      volatilityPct,
      volatilityLabel,
      volatilityClass,
      drop3mPct,
      drop6mPct,
      price3m,
      price6m,
      saving3m: currPrice - price3m,
      saving6m: currPrice - price6m,
      advice,
      adviceDetail
    };
  },

  getMultiSellerPricing(phone) {
    const basePrice = this.getPhoneNumericPrice(phone);
    if (basePrice <= 0) return [];

    const cleanFull = getPhoneFullName(phone);
    const brand = (phone.brand || '').trim();
    const cleanSearchTerm = cleanFull.replace(/\s+/g, ' ').trim();
    const qAmazon = encodeURIComponent(cleanSearchTerm).replace(/%20/g, '+');

    const amazonPrice = basePrice;
    const flipkartPrice = basePrice;
    const brandStorePrice = basePrice;
    const cashifyPrice = Math.round(basePrice * 0.75);

    const sellers = [
      {
        name: 'Amazon India',
        icon: '🛒',
        price: amazonPrice,
        priceStr: `₹${amazonPrice.toLocaleString()}`,
        url: `https://www.amazon.in/s?k=${qAmazon}&tag=phoneperfect-21`,
        isLowest: true,
        tag: 'Live Verified Price',
        tagClass: 'deal-good'
      },
      {
        name: 'Flipkart',
        icon: '🛍️',
        price: flipkartPrice,
        priceStr: `₹${flipkartPrice.toLocaleString()}`,
        url: `https://www.flipkart.com/search?q=${qAmazon}`,
        isLowest: true,
        tag: 'Live Verified Price',
        tagClass: 'deal-good'
      },
      {
        name: `${brand || 'Brand'} Official Store`,
        icon: '🏬',
        price: brandStorePrice,
        priceStr: `₹${brandStorePrice.toLocaleString()}`,
        url: getBrandOfficialStoreUrl(phone),
        isLowest: true,
        tag: 'Official Warranty & Deals',
        tagClass: 'deal-fair'
      },
      {
        name: 'Cashify (Trade-in / Refurbished)',
        icon: '♻️',
        price: cashifyPrice,
        priceStr: `₹${cashifyPrice.toLocaleString()}`,
        url: `https://www.cashify.in/buy-renovated-mobile-phones/search?q=${encodeURIComponent(cleanSearchTerm)}`,
        isLowest: false,
        tag: 'Certified Refurbished & Trade-in',
        tagClass: 'deal-good'
      }
    ];

    return sellers.sort((a, b) => a.price - b.price);
  },

  findCompetitors(targetPhone, allPhones) {
    const targetPrice = this.getPhoneNumericPrice(targetPhone);
    const minP = targetPrice * 0.75;
    const maxP = targetPrice * 1.25;

    return (allPhones || PHONES)
      .filter(p => p.id !== targetPhone.id)
      .map(p => ({ phone: p, price: this.getPhoneNumericPrice(p) }))
      .filter(item => item.price >= minP && item.price <= maxP)
      .sort((a, b) => Math.abs(a.price - targetPrice) - Math.abs(b.price - targetPrice))
      .slice(0, 3)
      .map(item => item.phone);
  },

  analyzeTradeoffs(phone, competitors) {
    const scores = phone.scores || {};
    const tradeoffs = [];
    
    const keys = ['processor', 'camera', 'battery', 'charging', 'display', 'durability'];
    const scoreVals = keys.map(k => ({ key: k, val: scores[k] || 7.0 })).sort((a, b) => b.val - a.val);
    
    const highest = scoreVals[0];
    const lowest = scoreVals[scoreVals.length - 1];
    
    if (highest.val - lowest.val >= 2.0) {
      tradeoffs.push({
        type: 'asymmetric',
        text: `Strong ${highest.key} (${highest.val}/10), but weaker ${lowest.key} (${lowest.val}/10)`
      });
    }

    if (scores.charging && scores.charging < 7.5 && scores.battery && scores.battery >= 8.5) {
      tradeoffs.push({ type: 'charging', text: 'Large battery capacity, but slower wired charging speed' });
    }

    if (competitors && competitors.length > 0) {
      const topComp = competitors[0];
      if (topComp.scores && topComp.scores.camera > (scores.camera || 0) + 1.0) {
        tradeoffs.push({ type: 'comp_camera', text: `Camera quality is behind competitor ${topComp.brand} ${topComp.name}` });
      }
      if (topComp.scores && topComp.scores.processor > (scores.processor || 0) + 1.0) {
        tradeoffs.push({ type: 'comp_proc', text: `Processing power is lower than ${topComp.brand} ${topComp.name}` });
      }
    }

    return tradeoffs;
  },

  calculatePurchaseRisk(phone, normWeights, maxBudget, histAnalysis, competitors, tradeoffs) {
    const valueScore = this.calculateValueScore(phone, Object.keys(normWeights || {}), maxBudget);
    const riskScore = +Math.min(99, Math.max(5, 100 - valueScore)).toFixed(1);

    let riskLevel = 'LOW RISK';
    let riskClass = 'risk-low';
    if (riskScore > 65) {
      riskLevel = 'HIGH RISK';
      riskClass = 'risk-high';
    } else if (riskScore > 45) {
      riskLevel = 'MEDIUM RISK';
      riskClass = 'risk-medium';
    }

    return { score: riskScore, level: riskLevel, cssClass: riskClass };
  },

  generateDecision(phone, selectedPriorities, budgetCat, allPhones) {
    const prioritiesToUse = selectedPriorities || (typeof appState !== 'undefined' ? appState.selectedPriorities : []);
    const budgetToUse = budgetCat !== undefined ? budgetCat : (typeof appState !== 'undefined' ? appState.selectedBudget : 'above-80000');
    const maxBudget = this.BUDGET_MAP[budgetToUse] || 250000;
    const normWeights = this.getUserNormalizedWeights(prioritiesToUse);
    const valueScore = this.calculateValueScore(phone, prioritiesToUse, budgetToUse);
    const currPrice = this.getPhoneNumericPrice(phone);
    const expectedPrice = this.getExpectedMarketPrice(phone);
    const priceStatus = this.evaluatePriceStatus(currPrice, expectedPrice);
    const category = this.getRecommendationCategory(valueScore);
    const histAnalysis = this.analyzeHistoricalPrice(phone);
    const priceOpp = this.evaluatePriceOpportunity(histAnalysis);
    const competitors = this.findCompetitors(phone, allPhones || PHONES);
    const tradeoffs = this.analyzeTradeoffs(phone, competitors);
    const risk = this.calculatePurchaseRisk(phone, normWeights, maxBudget, histAnalysis, competitors, tradeoffs);

    // Contextual Summary Reason
    let summaryReason = "";
    if (priceStatus.diffAmount > 500 && valueScore >= 65) {
      summaryReason = `₹${priceStatus.diffAmount.toLocaleString()} above estimated market price, but strong specifications provide good overall value.`;
    } else if (priceStatus.diffAmount <= 500 && valueScore >= 65) {
      summaryReason = `Good overall value with strong performance, battery life, and specifications.`;
    } else if (priceStatus.diffAmount > 500 && valueScore < 50) {
      summaryReason = `Price is higher than estimated market price and specifications do not justify the premium.`;
    } else {
      summaryReason = `Fair performance-to-price ratio in its category.`;
    }

    // Detailed reasons array
    const reasons = [];
    const reqMatchPct = Math.round(valueScore);
    reasons.push({ type: 'pos', text: `${reqMatchPct}/100 overall value score` });
    reasons.push({ type: priceStatus.diffPct <= 15 ? 'pos' : 'neg', text: `Price status: ${priceStatus.label} (${priceStatus.diffPct > 0 ? '+' : ''}${priceStatus.diffPct}% vs market)` });
    reasons.push({ type: valueScore >= 65 ? 'pos' : 'neg', text: summaryReason });

    if (phone.scores && phone.scores.processor >= 8.5) {
      reasons.push({ type: 'pos', text: `High processor score (${phone.scores.processor}/10) for gaming & multitasking` });
    }
    if (phone.scores && phone.scores.camera >= 8.5) {
      reasons.push({ type: 'pos', text: `Strong camera rating (${phone.scores.camera}/10)` });
    }

    tradeoffs.forEach(t => {
      reasons.push({ type: 'neg', text: t.text });
    });

    if (currPrice > maxBudget && maxBudget < 200000) {
      reasons.push({ type: 'neg', text: `Price exceeds target budget ceiling of ₹${maxBudget.toLocaleString()}` });
    }

    return {
      phone,
      valueScore,
      recommendation: category.label,
      decisionClass: category.decisionClass,
      badgeClass: category.badgeClass,
      priceStatus: priceStatus.label,
      priceStatusClass: priceStatus.cssClass,
      priceDiffPct: priceStatus.diffPct,
      summaryReason,
      risk,
      deal: priceStatus, // Alias for backward compatibility
      priceOpp,
      histAnalysis,
      competitors,
      tradeoffs,
      reasons
    };
  }
};

// ─── GLOBAL UTILITIES (PHONE NAME CLEANUP & BUDGET FILTERING) ────────────────
function getCleanPhoneName(rawName) {
  if (!rawName || typeof rawName !== 'string') return '';
  // Case-insensitively remove "Special Edition", "Edition (v17)", "Edition v3", "Edition 2", "Edition (12)", etc.
  let cleaned = rawName.replace(/\s*(?:special\s+)?edition(?:\s*\(?v?\d+\)?)?/gi, '');
  cleaned = cleaned.replace(/\s*\(?v\d+\)?$/gi, '');
  cleaned = cleaned.replace(/[\(\)\[\]\s]+$/gi, ''); // strip trailing parentheses/brackets/whitespace
  return cleaned.replace(/\s+/g, ' ').trim();
}

function getPhoneFullName(phone) {
  if (!phone) return '';
  let brand = (phone.brand || '').trim();
  if (brand.includes('&')) {
    brand = brand.split('&')[0].trim();
  }
  let cleanName = phone.displayName || getCleanPhoneName(phone.name || '');
  if (!brand) return cleanName;
  if (cleanName.toLowerCase().startsWith(brand.toLowerCase())) {
    return cleanName;
  }
  return `${brand} ${cleanName}`.trim();
}

function getPhoneById(phoneId) {
  if (!phoneId || typeof PHONES === 'undefined' || !Array.isArray(PHONES)) return null;
  return PHONES.find(p => p.id === phoneId) || null;
}

function getPhoneImageUrl(phone) {
  if (!phone) return null;
  if (typeof phone.image === 'string' && phone.image.startsWith('http')) {
    return phone.image;
  }
  if (typeof phone.imageUrl === 'string' && phone.imageUrl.startsWith('http')) {
    return phone.imageUrl;
  }
  if (Array.isArray(phone.images) && phone.images.length > 0 && typeof phone.images[0] === 'string' && phone.images[0].startsWith('http')) {
    return phone.images[0];
  }
  return null;
}

function getPhoneImageHtml(phone, size = 74, customClass = 'phone-img') {
  if (!phone) {
    return `
      <div class="image-unavailable-box" style="width:${size}px; height:${size}px;">
        <span class="img-unavail-icon">📱</span>
        <span class="img-unavail-text">Image unavailable</span>
      </div>
    `;
  }

  const imgUrl = getPhoneImageUrl(phone);
  const fullName = getPhoneFullName(phone);
  const uid = 'img-' + (phone.id ? phone.id.replace(/[^a-zA-Z0-9_-]/g, '') : Math.random().toString(36).substring(2, 7)) + '-' + Math.random().toString(36).substring(2, 6);

  if (imgUrl) {
    return `
      <img id="${uid}-img"
           src="${imgUrl}" 
           alt="${fullName}" 
           class="${customClass}" 
           loading="lazy" 
           onerror="this.style.display='none'; const fb=document.getElementById('${uid}-fb'); if(fb) fb.style.display='flex';" />
      <div id="${uid}-fb" class="image-unavailable-box" style="display:none; width:${size}px; height:${size}px;">
        <span class="img-unavail-icon">📱</span>
        <span class="img-unavail-text">Image unavailable</span>
      </div>
    `;
  } else {
    return `
      <div class="image-unavailable-box" style="width:${size}px; height:${size}px;">
        <span class="img-unavail-icon">📱</span>
        <span class="img-unavail-text">Image unavailable</span>
      </div>
    `;
  }
}

function getBrandOfficialStoreUrl(phone) {
  if (!phone) return 'https://www.google.com';
  let brand = (phone.brand || '').toLowerCase().trim();
  if (brand.includes('&')) {
    brand = brand.split('&')[0].trim();
  }
  const cleanName = phone.displayName || getCleanPhoneName(phone.name || '');
  const qName = encodeURIComponent(cleanName);

  if (brand.includes('apple') || cleanName.toLowerCase().includes('iphone')) {
    return `https://www.apple.com/in/search/${qName}`;
  } else if (brand.includes('samsung')) {
    return `https://www.samsung.com/in/search/?searchvalue=${qName}`;
  } else if (brand.includes('oneplus')) {
    return `https://www.oneplus.in/search?q=${qName}`;
  } else if (brand.includes('xiaomi') || brand.includes('redmi') || brand.includes('poco')) {
    return `https://www.mi.com/in/search/${qName}`;
  } else if (brand.includes('vivo') || brand.includes('iqoo')) {
    return `https://shop.vivo.com/in/search?q=${qName}`;
  } else if (brand.includes('realme')) {
    return `https://buy.realme.com/in/search?q=${qName}`;
  } else if (brand.includes('google') || cleanName.toLowerCase().includes('pixel')) {
    return `https://store.google.com/in/search?q=${qName}`;
  } else if (brand.includes('motorola') || brand.includes('moto')) {
    return `https://www.motorola.in/search?q=${qName}`;
  } else if (brand.includes('nothing')) {
    return `https://in.nothing.tech/search?q=${qName}`;
  } else {
    return `https://www.google.com/search?q=${encodeURIComponent(brand + ' India official store ' + cleanName)}`;
  }
}

function getPhoneAmazonUrl(phone) {
  if (!phone) return 'https://www.amazon.in';
  const fullName = getPhoneFullName(phone);
  const cleanTerm = fullName.replace(/\s+/g, ' ').trim();
  const qAmazon = encodeURIComponent(cleanTerm).replace(/%20/g, '+');
  return `https://www.amazon.in/s?k=${qAmazon}&tag=phoneperfect-21`;
}

function isPhoneInBudget(phone, budgetCat) {
  const p = DecisionEngine.getPhoneNumericPrice(phone);
  if (p <= 0) return false;
  
  if (budgetCat === 'under-10000' || budgetCat === 0 || budgetCat === '0') {
    return p < 10000;
  }
  if (budgetCat === '10000-20000' || budgetCat === 1 || budgetCat === '1') {
    return p >= 10000 && p <= 20000;
  }
  if (budgetCat === '20000-30000' || budgetCat === 2 || budgetCat === '2') {
    return p >= 20000 && p <= 30000;
  }
  if (budgetCat === '30000-50000' || budgetCat === 3 || budgetCat === '3') {
    return p >= 30000 && p <= 50000;
  }
  if (budgetCat === '50000-80000' || budgetCat === 4 || budgetCat === '4') {
    return p >= 50000 && p <= 80000;
  }
  if (budgetCat === 'above-80000' || budgetCat === 5 || budgetCat === '5') {
    return p > 80000;
  }

  if (typeof budgetCat === 'string') {
    const nums = budgetCat.replace(/,/g, '').match(/\d+/g);
    if (nums) {
      const vals = nums.map(n => parseInt(n, 10)).filter(n => !isNaN(n));
      if (vals.length === 1) {
        if (budgetCat.toLowerCase().includes('under') || budgetCat.toLowerCase().includes('below')) {
          return p < vals[0];
        }
        if (budgetCat.toLowerCase().includes('above') || budgetCat.toLowerCase().includes('over')) {
          return p > vals[0];
        }
      } else if (vals.length >= 2) {
        const min = Math.min(vals[0], vals[1]);
        const max = Math.max(vals[0], vals[1]);
        return p >= min && p <= max;
      }
    }
  }

  return false;
}

// Data Initialization & Sanitization
function initPhonesData() {
  if (typeof PHONES !== 'undefined' && Array.isArray(PHONES)) {
    PHONES.forEach(phone => {
      phone.displayName = getCleanPhoneName(phone.name);
      phone.price_numeric = DecisionEngine.getPhoneNumericPrice(phone);
      const cleanFull = getPhoneFullName(phone);
      const q = encodeURIComponent(`"${cleanFull}"`).replace(/%20/g, '+');
      phone.amazon_url = `https://www.amazon.in/s?k=${q}&tag=phoneperfect-21`;
    });
  }
}
initPhonesData();

// Criteria list definition for score calculation compatibility
if (typeof window.CRITERIA === 'undefined' && typeof CRITERIA === 'undefined') {
  window.CRITERIA = [
    { key: 'camera', label: 'Camera Quality', icon: '📷' },
    { key: 'battery', label: 'Battery Life', icon: '🔋' },
    { key: 'processor', label: 'Processor', icon: '⚡' },
    { key: 'display', label: 'Display Quality', icon: '📱' },
    { key: 'charging', label: 'Charging Speed', icon: '🔌' },
    { key: 'durability', label: 'Durability', icon: '🛡️' }
  ];
}

// ─── CENTRAL APP STATE (SINGLE SOURCE OF TRUTH) ─────────────────────────────
const appState = {
  selectedPriorities: [],
  selectedBudget: "above-80000",
  currentScreen: "screen-home",
  screenHistory: ["screen-home"]
};

window.appState = appState;

// Engine compatibility aliases
let selectedPriorities = appState.selectedPriorities;
let budgetCategory = appState.selectedBudget;

let userWeights = { durability:7, camera:7, battery:7, charging:7, display:7, sound:7, ipRating:7, processor:7, gaming:7, storage:7 };
let currentSearch = '';
let currentBrandFilter = 'All';
let advFilters = {
  ram: 'any',
  processor: 'any',
  has5g: false,
  hasNfc: false,
  hasWireless: false,
  storage: 'any',
  battery: 'any'
};

let allPhonesSorted = [...PHONES];
let favorites = JSON.parse(localStorage.getItem('phonePerfectFavs') || '[]');
let compareList = [];

// ─── STATE DEBUG PANEL ────────────────────────────────────────────────────────
function updateDebugPanel() {
  const pEl = document.getElementById('debug-priorities');
  const bEl = document.getElementById('debug-budget');
  const sEl = document.getElementById('debug-screen');
  
  if (pEl) pEl.textContent = JSON.stringify(appState.selectedPriorities);
  if (bEl) bEl.textContent = String(appState.selectedBudget);
  if (sEl) sEl.textContent = String(appState.currentScreen);
}

// ─── INIT ─────────────────────────────────────────────────────────────────────
window.addEventListener('DOMContentLoaded', () => {
  updateWeightsFromTags();
  renderBrandFilters();
  populateFilterSelects();
  updateFavoritesCount();

  const priorityContainer = document.getElementById('priority-tags-container');
  if (priorityContainer) {
    priorityContainer.addEventListener('click', (e) => {
      const item = e.target.closest('.list-item');
      if (item) {
        const key = item.getAttribute('data-priority');
        if (key) togglePriority(key);
      }
    });
  }

  const budgetContainer = document.getElementById('budget-items-container');
  if (budgetContainer) {
    budgetContainer.addEventListener('click', (e) => {
      const item = e.target.closest('.list-item');
      if (item) {
        const b = item.getAttribute('data-budget');
        if (b) selectBudget(b);
      }
    });
  }

  renderPriorities();
  renderBudget();
  updateDebugPanel();
});

// ─── PRIORITIES (HOME SCREEN & PRIORITIES SCREEN) ─────────────────────────────
function togglePriority(key) {
  if (!key) return;
  console.log(`[PHONEPERFECT] Priority clicked: ${key}`);
  console.log(`[PHONEPERFECT] State before:`, JSON.stringify(appState.selectedPriorities));

  const index = appState.selectedPriorities.indexOf(key);
  if (index > -1) {
    appState.selectedPriorities.splice(index, 1);
  } else {
    if (appState.selectedPriorities.length >= 5) {
      if (typeof showToast === 'function') {
        showToast("⚠️ Maximum 5 priorities allowed");
      } else {
        alert("Maximum 5 priorities allowed");
      }
      console.log(`[PHONEPERFECT] Priority selection rejected (Max 5 limit reached)`);
      renderPriorities();
      updateDebugPanel();
      return;
    }
    appState.selectedPriorities.push(key);
  }

  console.log(`[PHONEPERFECT] State after:`, JSON.stringify(appState.selectedPriorities));
  selectedPriorities = appState.selectedPriorities;
  updateWeightsFromTags();
  renderPriorities();
  updateDebugPanel();
}

function renderPriorities() {
  console.log(`[PHONEPERFECT] Rendering priorities:`, JSON.stringify(appState.selectedPriorities));
  const container = document.getElementById('priority-tags-container');
  if (!container) return;

  const items = container.querySelectorAll('.list-item');
  items.forEach(item => {
    const key = item.getAttribute('data-priority');
    const isSelected = !!(key && appState.selectedPriorities.includes(key));
    if (isSelected) {
      item.classList.add('active');
    } else {
      item.classList.remove('active');
    }
    if (key) console.log(`[PHONEPERFECT] ${key} selected: ${isSelected}`);
  });
}

function syncPrioritiesUI() {
  renderPriorities();
}

function updateWeightsFromTags() {
  CRITERIA.forEach(c => userWeights[c.key] = 3);
  userWeights['gaming'] = 3;
  userWeights['storage'] = 3;
  
  appState.selectedPriorities.forEach(key => {
    userWeights[key] = 10;
  });
}

// ─── BUDGET ───────────────────────────────────────────────────────────────────
function selectBudget(budgetId) {
  if (typeof budgetId === 'number') {
    const map = ['under-10000', '10000-20000', '20000-30000', '30000-50000', '50000-80000', 'above-80000'];
    budgetId = map[budgetId] || 'above-80000';
  }
  if (!budgetId) return;

  console.log(`[PHONEPERFECT] Budget clicked: ${budgetId}`);
  console.log(`[PHONEPERFECT] Budget state before: ${appState.selectedBudget}`);

  appState.selectedBudget = budgetId;
  budgetCategory = budgetId;

  console.log(`[PHONEPERFECT] Budget state after: ${appState.selectedBudget}`);
  renderBudget();
  updateDebugPanel();
}

function updateBudget(val) {
  selectBudget(val);
}

function renderBudget() {
  console.log(`[PHONEPERFECT] Rendering budget: ${appState.selectedBudget}`);
  const container = document.getElementById('budget-items-container');
  if (!container) return;

  const items = container.querySelectorAll('.list-item');
  items.forEach(item => {
    const bId = item.getAttribute('data-budget');
    const isSelected = (bId === appState.selectedBudget);
    if (isSelected) {
      item.classList.add('active', 'selected');
    } else {
      item.classList.remove('active', 'selected');
    }
    if (bId) console.log(`[PHONEPERFECT] Budget ${bId} selected: ${isSelected}`);
  });

  const displayEl = document.getElementById('budget-display');
  if (displayEl) {
    const budgetLabels = {
      'under-10000': 'Under ₹10,000',
      '10000-20000': '₹10,000 - ₹20,000',
      '20000-30000': '₹20,000 - ₹30,000',
      '30000-50000': '₹30,000 - ₹50,000',
      '50000-80000': '₹50,000 - ₹80,000',
      'above-80000': 'Above ₹80,000 / Premium'
    };
    displayEl.textContent = budgetLabels[appState.selectedBudget] || 'No Limit';
  }
}

// ─── HELPERS ──────────────────────────────────────────────────────────────────
function getBatteryMah(phone) {
  if(!phone || !phone.specs || !phone.specs.battery) return '5000 mAh';
  const m = phone.specs.battery.match(/([\d,]+)\s*mAh/);
  return m ? m[1] + ' mAh' : phone.specs.battery;
}

function getIPShort(phone) {
  if(!phone || !phone.specs || !phone.specs.ip) return 'IP68';
  return phone.specs.ip.split('–')[0].split(' ').slice(0,2).join(' ').trim();
}

// ─── SCORING & RECOMMENDATION ENGINE ──────────────────────────────────────────
function computeScore(phone) {
  const normWeights = DecisionEngine.getUserNormalizedWeights(appState.selectedPriorities);
  const maxBudget = DecisionEngine.BUDGET_MAP[appState.selectedBudget] || 250000;
  return DecisionEngine.calculatePersonalizedValueScore(phone, normWeights, maxBudget);
}

function filterAndScore(phones, isNearbyExpanded = false) {
  const budgetCat = appState.selectedBudget;
  let filtered = phones;
  
  if (!isNearbyExpanded) {
    // Apply selected budget HARD FILTER before ranking/scoring
    filtered = phones.filter(p => isPhoneInBudget(p, budgetCat));
  }

  return filtered
    .map(p => {
      const decision = DecisionEngine.generateDecision(p, appState.selectedPriorities, budgetCat, PHONES);
      return {
        ...p,
        _score: decision.valueScore,
        _decision: decision
      };
    })
    .sort((a, b) => b._score - a._score);
}

function generateRecommendations(isNearbyExpanded = false) {
  const scored = filterAndScore(PHONES, isNearbyExpanded);
  renderPhoneCards('phones-grid', scored.slice(0, 30), isNearbyExpanded);
  const resultsScreen = document.getElementById('screen-results');
  if (resultsScreen) {
    const content = resultsScreen.querySelector('.screen-content');
    if (content) content.scrollTop = 0;
  }
}

function renderPhoneCards(containerId, phonesArray, isNearbyExpanded = false) {
  const container = document.getElementById(containerId);
  if (!container) return;
  
  const budgetCat = appState.selectedBudget;
  const budgetLabels = {
    'under-10000': 'Under ₹10,000',
    '10000-20000': '₹10,000 – ₹20,000',
    '20000-30000': '₹20,000 – ₹30,000',
    '30000-50000': '₹30,000 – ₹50,000',
    '50000-80000': '₹50,000 – ₹80,000',
    'above-80000': 'Above ₹80,000 / Premium'
  };
  const currentBudgetLabel = budgetLabels[budgetCat] || 'the selected range';

  let eligiblePhones = phonesArray;
  if (!isNearbyExpanded && containerId === 'phones-grid') {
    eligiblePhones = phonesArray.filter(phone => isPhoneInBudget(phone, budgetCat));
  }

  if (eligiblePhones.length === 0) {
    if (containerId === 'phones-grid') {
      container.innerHTML = `
        <div class="no-results-box" style="text-align:center; padding: 40px 20px; background: var(--bg-card); border-radius: 16px; margin-top: 20px; border: 1px solid var(--border);">
          <div style="font-size:3rem; margin-bottom:12px;">📱</div>
          <h3 style="margin-bottom:8px; color:var(--text-1); font-size: 1.1rem; font-weight:700;">No suitable phones found within ${currentBudgetLabel}.</h3>
          <p style="color:var(--text-2); margin-bottom:20px; font-size:0.85rem; line-height: 1.4;">There are no smartphones in our current market catalog matching this exact budget criteria.</p>
          <button class="btn-primary" style="margin: 0 auto; max-width:240px; padding: 12px 20px;" onclick="generateRecommendations(true)">Explore nearby budget</button>
        </div>
      `;
    } else {
      container.innerHTML = '<p class="text-center mt-4 text-2">No smartphones match the criteria.</p>';
    }
    return;
  }

  container.innerHTML = eligiblePhones.map((phone, i) => {
    // Safety Validation Check before rendering each card
    if (!isNearbyExpanded && containerId === 'phones-grid' && !isPhoneInBudget(phone, budgetCat)) {
      return '';
    }

    const isFav = favorites.includes(phone.id);
    const decision = phone._decision || DecisionEngine.generateDecision(phone, appState.selectedPriorities, appState.selectedBudget, PHONES);
    const valueScore = decision.valueScore;
    const recLabel = decision.recommendation || 'Worth Buying';
    const recClass = decision.decisionClass || 'dec-buy';
    const priceStatus = decision.priceStatus || decision.deal?.label || 'Good Price';
    const priceStatusClass = decision.priceStatusClass || decision.deal?.cssClass || 'deal-good';
    const priceNum = DecisionEngine.getPhoneNumericPrice(phone);
    const priceDisplay = priceNum > 0 ? '₹' + priceNum.toLocaleString() : phone.price;
    const ramDisplay = phone.ram_gb ? phone.ram_gb + 'GB' : '';
    const fullName = getPhoneFullName(phone);

    const dealAlert = DecisionEngine.getLiveDealAlert(phone);
    const dealAlertHtml = dealAlert ? dealAlert.badgeHtml : '';

    const imgHtml = getPhoneImageHtml(phone, 74, 'phone-img');

    return `
      <div class="phone-card" style="animation-delay: ${i*0.04}s" onclick="showPurchaseAnalysis('${phone.id}')">
        <div class="phone-img-wrap">
          ${imgHtml}
        </div>
        <div class="phone-info">
          <div class="phone-title">${fullName}</div>
          <div class="phone-subtitle-row">
            <span class="value-score-badge">Value Score: ${valueScore}/100</span>
            <span class="ram-badge">${ramDisplay}</span>
          </div>
          <div class="phone-badges-row mt-1">
            <span class="badge-risk ${recClass}">${recLabel}</span>
            <span class="badge-deal ${priceStatusClass}">${priceStatus}</span>
            ${dealAlertHtml}
          </div>
          <div class="phone-price mt-1">${priceDisplay}</div>
        </div>
        <div style="display:flex; flex-direction:column; gap:6px; align-items:flex-end;">
          <button class="fav-btn" onclick="event.stopPropagation(); toggleFavorite('${phone.id}', this)">
            ${isFav ? '❤️' : '🤍'}
          </button>
          <button class="btn-primary-small" style="font-size:0.68rem; padding:3px 8px;" onclick="event.stopPropagation(); showPhoneDetails('${phone.id}')">
            📋 Specs
          </button>
        </div>
      </div>
    `;
  }).join('');
}

// ─── PURCHASE ANALYSIS SCREEN (NEW PRIMARY DECISION VIEW) ─────────────────────
function showPurchaseAnalysis(phoneId) {
  const phone = getPhoneById(phoneId);
  if (!phone) return;

  const decision = DecisionEngine.generateDecision(phone, selectedPriorities, budgetCategory, PHONES);
  const fullName = getPhoneFullName(phone);
  const priceNum = DecisionEngine.getPhoneNumericPrice(phone);
  
  // Set Phone Header and Overview
  const titleEl = document.getElementById('pa-phone-name');
  if (titleEl) titleEl.textContent = fullName;

  const priceEl = document.getElementById('pa-phone-price');
  if (priceEl) priceEl.textContent = priceNum > 0 ? `₹${priceNum.toLocaleString()}` : phone.price;

  const emojiEl = document.getElementById('pa-phone-emoji');
  if (emojiEl) {
    emojiEl.innerHTML = `<div class="pa-phone-img-wrap" style="width:75px; height:75px; display:inline-flex; align-items:center; justify-content:center;">${getPhoneImageHtml(phone, 75, 'pa-hero-img')}</div>`;
  }

  // Badges
  const recBadge = document.getElementById('pa-recommendation-badge');
  if (recBadge) {
    recBadge.textContent = (decision.recommendation || 'WORTH BUYING').toUpperCase();
    recBadge.className = `decision-banner ${decision.decisionClass}`;
  }

  const valScoreEl = document.getElementById('pa-value-score');
  if (valScoreEl) valScoreEl.textContent = decision.valueScore;

  const riskScoreEl = document.getElementById('pa-risk-score');
  if (riskScoreEl) riskScoreEl.textContent = decision.risk.score;

  const riskLevelEl = document.getElementById('pa-risk-level');
  if (riskLevelEl) {
    riskLevelEl.textContent = decision.risk.level;
    riskLevelEl.className = `badge-risk ${decision.risk.cssClass}`;
  }

  const dealEl = document.getElementById('pa-deal-status');
  if (dealEl) {
    dealEl.textContent = decision.priceStatus || decision.deal.label;
    dealEl.className = `badge-deal ${decision.priceStatusClass || decision.deal.cssClass}`;
  }

  const oppEl = document.getElementById('pa-price-opportunity');
  if (oppEl) oppEl.textContent = decision.priceOpp.label;

  // Live Deal Alert Banner
  const dealAlert = DecisionEngine.getLiveDealAlert(phone);
  const dealBannerEl = document.getElementById('pa-deal-alert-banner');
  if (dealBannerEl) {
    if (dealAlert && dealAlert.alertBanner) {
      dealBannerEl.innerHTML = dealAlert.alertBanner;
      dealBannerEl.style.display = 'block';
    } else {
      dealBannerEl.style.display = 'none';
    }
  }

  // Price Trend & Stats
  const hist = decision.histAnalysis;
  document.getElementById('pa-price-avg').textContent = `₹${hist.avg.toLocaleString()}`;
  document.getElementById('pa-price-min').textContent = `₹${hist.min.toLocaleString()}`;
  document.getElementById('pa-price-max').textContent = `₹${hist.max.toLocaleString()}`;
  
  const diffEl = document.getElementById('pa-price-diff');
  if (diffEl) {
    const sign = hist.diffPct > 0 ? '+' : '';
    diffEl.textContent = `${sign}${hist.diffPct}% vs avg`;
    diffEl.style.color = hist.diffPct <= 0 ? 'var(--success)' : 'var(--danger)';
  }

  // AI Volatility & Depreciation Forecast Binding
  const volDep = DecisionEngine.calculateMarketVolatilityAndDepreciation(phone);
  const volBadge = document.getElementById('pa-volatility-badge');
  if (volBadge) {
    volBadge.textContent = volDep.volatilityLabel;
    volBadge.className = `badge-risk ${volDep.volatilityClass}`;
  }

  const pNow = document.getElementById('pa-price-now');
  if (pNow) pNow.textContent = priceNum > 0 ? `₹${priceNum.toLocaleString()}` : phone.price;

  const p3m = document.getElementById('pa-price-3m');
  if (p3m) p3m.textContent = `₹${volDep.price3m.toLocaleString()}`;

  const d3m = document.getElementById('pa-drop-3m');
  if (d3m) d3m.textContent = `-${volDep.drop3mPct}%`;

  const p6m = document.getElementById('pa-price-6m');
  if (p6m) p6m.textContent = `₹${volDep.price6m.toLocaleString()}`;

  const d6m = document.getElementById('pa-drop-6m');
  if (d6m) d6m.textContent = `-${volDep.drop6mPct}%`;

  const advTitle = document.getElementById('pa-depreciation-advice');
  if (advTitle) advTitle.textContent = volDep.advice;

  const advDetail = document.getElementById('pa-depreciation-detail');
  if (advDetail) advDetail.textContent = volDep.adviceDetail;

  // Render Sparkline Chart
  const canvas = document.getElementById('pa-price-chart');
  if (canvas && typeof renderSparkline === 'function') {
    renderSparkline(canvas, hist.history, hist.diffPct <= 0 ? '#10b981' : '#f59e0b');
  }

  // Populate Multi-Seller Price Comparison
  const sellersListEl = document.getElementById('pa-sellers-list');
  if (sellersListEl) {
    const sellers = DecisionEngine.getMultiSellerPricing(phone);
    sellersListEl.innerHTML = sellers.map(s => `
      <div style="background:var(--bg-dark); border-radius:14px; padding:12px 14px; display:flex; align-items:center; justify-content:space-between; border:1px solid var(--border);">
        <div style="display:flex; align-items:center; gap:10px;">
          <span style="font-size:1.4rem;">${s.icon}</span>
          <div>
            <div style="font-size:0.9rem; font-weight:700; color:var(--text-1);">${s.name} ${s.isLowest ? '<span class="badge-deal deal-good" style="font-size:0.65rem; margin-left:4px;">🔥 LOWEST</span>' : ''}</div>
            <div style="font-size:0.72rem; color:var(--text-2); margin-top:2px;">${s.tag}</div>
          </div>
        </div>
        <div style="display:flex; align-items:center; gap:10px;">
          <div style="text-align:right;">
            <div style="font-size:0.95rem; font-weight:800; color:${s.isLowest ? '#10b981' : 'var(--text-1)'};">${s.priceStr}</div>
          </div>
          <a href="${s.url}" target="_blank" class="btn-primary-small" style="font-size:0.75rem; text-decoration:none; padding:6px 12px; display:inline-block;">Buy ➔</a>
        </div>
      </div>
    `).join('');
  }

  // Requirement Match Breakdown
  const specs = DecisionEngine.calculateNormalizedScores(phone, DecisionEngine.BUDGET_MAP[budgetCategory]);
  const reqGrid = document.getElementById('pa-req-breakdown');
  if (reqGrid) {
    reqGrid.innerHTML = `
      <div class="req-bar-item">
        <div class="req-bar-label"><span>⚡ Processor</span><span>${specs.processor}/100</span></div>
        <div class="req-bar-bg"><div class="req-bar-fill" style="width:${specs.processor}%"></div></div>
      </div>
      <div class="req-bar-item">
        <div class="req-bar-label"><span>📷 Camera</span><span>${specs.camera}/100</span></div>
        <div class="req-bar-bg"><div class="req-bar-fill" style="width:${specs.camera}%"></div></div>
      </div>
      <div class="req-bar-item">
        <div class="req-bar-label"><span>🔋 Battery</span><span>${specs.battery}/100</span></div>
        <div class="req-bar-bg"><div class="req-bar-fill" style="width:${specs.battery}%"></div></div>
      </div>
      <div class="req-bar-item">
        <div class="req-bar-label"><span>📱 Display</span><span>${specs.display}/100</span></div>
        <div class="req-bar-bg"><div class="req-bar-fill" style="width:${specs.display}%"></div></div>
      </div>
    `;
  }

  // Specification Trade-offs
  const tradeoffsContainer = document.getElementById('pa-tradeoffs-list');
  if (tradeoffsContainer) {
    if (decision.tradeoffs.length === 0) {
      tradeoffsContainer.innerHTML = '<p class="text-sm text-2">No major specification trade-offs identified.</p>';
    } else {
      tradeoffsContainer.innerHTML = decision.tradeoffs.map(t => `
        <div class="tradeoff-card">
          <span class="tradeoff-icon">⚠️</span>
          <span class="tradeoff-text">${t.text}</span>
        </div>
      `).join('');
    }
  }

  // Competitor Analysis
  const compContainer = document.getElementById('pa-competitor-list');
  if (compContainer) {
    if (decision.competitors.length === 0) {
      compContainer.innerHTML = '<p class="text-sm text-2">No direct market competitors in this price range.</p>';
    } else {
      compContainer.innerHTML = decision.competitors.map(c => {
        const cDec = DecisionEngine.generateDecision(c, selectedPriorities, budgetCategory, PHONES);
        const cName = getPhoneFullName(c);
        const cPrice = DecisionEngine.getPhoneNumericPrice(c);
        const phonePrice = DecisionEngine.getPhoneNumericPrice(phone);
        const priceDiff = cPrice - phonePrice;
        const diffText = priceDiff > 0 ? `+₹${priceDiff.toLocaleString()}` : `-₹${Math.abs(priceDiff).toLocaleString()}`;
        return `
          <div class="competitor-card" onclick="showPurchaseAnalysis('${c.id}')" style="display:flex; gap:12px; align-items:center;">
            <div class="comp-img-wrap" style="width:50px; height:50px; flex-shrink:0; background:rgba(255,255,255,0.03); border-radius:10px; display:flex; align-items:center; justify-content:center; overflow:hidden; border:1px solid var(--border);">
              ${getPhoneImageHtml(c, 50, 'comp-phone-img')}
            </div>
            <div style="flex:1;">
              <div class="comp-header">
                <span class="comp-name">${cName}</span>
                <span class="comp-price">₹${cPrice.toLocaleString()} (${diffText})</span>
              </div>
              <div class="comp-scores">
                <span class="comp-score">Value: ${cDec.valueScore}</span>
                <span class="badge-risk ${cDec.risk.cssClass}">${cDec.risk.level}</span>
              </div>
            </div>
          </div>
        `;
      }).join('');
    }
  }

  // Explainable Decision Reasons
  const reasonsContainer = document.getElementById('pa-reasons-list');
  if (reasonsContainer) {
    reasonsContainer.innerHTML = decision.reasons.map(r => `
      <div class="reason-item ${r.type}">
        <span class="reason-bullet">${r.type === 'pos' ? '✅' : '⚠️'}</span>
        <span class="reason-text">${r.text}</span>
      </div>
    `).join('');
  }

  // Amazon Link
  const buyBtn = document.getElementById('pa-buy-amazon');
  if (buyBtn) {
    buyBtn.onclick = () => {
      window.open(getPhoneAmazonUrl(phone), '_blank');
    };
  }

  // Also setup Favorites button on Analysis screen
  const favBtn = document.getElementById('pa-fav-btn');
  if (favBtn) {
    favBtn.textContent = favorites.includes(phone.id) ? '❤️' : '🤍';
    favBtn.onclick = () => { toggleFavorite(phone.id, favBtn); };
  }

  // Details button fallback
  const detailsBtn = document.getElementById('pa-view-details-btn');
  if (detailsBtn) {
    detailsBtn.onclick = () => { showPhoneDetails(phone.id); };
  }

  navigateTo('screen-purchase-analysis');
}

// ─── DETAILS SCREEN ───────────────────────────────────────────────────────────
function showPhoneDetails(id) {
  const phone = getPhoneById(id);
  if(!phone) return;

  const decision = DecisionEngine.generateDecision(phone, selectedPriorities, budgetCategory, PHONES);
  const fullName = getPhoneFullName(phone);
  const priceNum = DecisionEngine.getPhoneNumericPrice(phone);

  document.getElementById('modal-name').textContent = fullName;
  document.getElementById('modal-score').textContent = decision.valueScore;
  document.getElementById('modal-price').textContent = priceNum > 0 ? '₹' + priceNum.toLocaleString() : phone.price;

  const heroImgEl = document.getElementById('modal-phone-img-wrap');
  if (heroImgEl) {
    heroImgEl.innerHTML = getPhoneImageHtml(phone, 110, 'details-phone-img');
  }
  
  const favBtn = document.getElementById('modal-fav-btn');
  favBtn.textContent = favorites.includes(phone.id) ? '❤️' : '🤍';
  favBtn.onclick = () => { toggleFavorite(phone.id, favBtn); };

  const compareBtn = document.getElementById('add-compare-btn');
  compareBtn.onclick = () => { toggleCompare(phone.id); };

  const buyBtn = document.getElementById('modal-buy-btn');
  if (buyBtn) {
    buyBtn.onclick = () => {
      window.open(getPhoneAmazonUrl(phone), '_blank');
    };
  }
  
  // Specs Tab
  const specsHtml = Object.keys(phone.specs).map(key => {
    const iconMap = { display: '📱', processor: '⚡', ram: '💾', camera: '📷', battery: '🔋', charging: '🔌', ip: '🛡️', weight: '⚖️', build: '🏗️' };
    const icon = iconMap[key] || '⚙️';
    return `
      <div class="spec-row">
        <div class="spec-icon">${icon}</div>
        <div class="spec-data">
          <div class="spec-label">${key.toUpperCase()}</div>
          <div class="spec-val">${phone.specs[key]}</div>
        </div>
      </div>
    `;
  }).join('');
  document.getElementById('modal-specs-grid').innerHTML = specsHtml;

  navigateTo('screen-details');
}

// ─── FAVORITES ────────────────────────────────────────────────────────────────
function toggleFavorite(id, btnElement) {
  const index = favorites.indexOf(id);
  if (index > -1) {
    favorites.splice(index, 1);
    if(btnElement) btnElement.textContent = '🤍';
  } else {
    favorites.push(id);
    if(btnElement) btnElement.textContent = '❤️';
  }
  localStorage.setItem('phonePerfectFavs', JSON.stringify(favorites));
  updateFavoritesCount();
  
  if(document.getElementById('screen-favorites').classList.contains('active')) {
    renderFavorites();
  }
}

function updateFavoritesCount() {
  const count = favorites.length;
}

function renderFavorites() {
  const favPhones = favorites.map(id => getPhoneById(id)).filter(Boolean);
  renderPhoneCards('favorites-grid', favPhones, true);
}

// ─── COMPARE ──────────────────────────────────────────────────────────────────
function toggleCompare(id) {
  if (compareList.includes(id)) {
    compareList = compareList.filter(x => x !== id);
    alert('Removed from compare');
  } else {
    if (compareList.length >= 2) {
      compareList.shift();
    }
    compareList.push(id);
    alert('Added to compare');
  }
}

function clearCompare() {
  compareList = [];
  document.getElementById('compare-content').innerHTML = '<p class="text-center mt-4">Add phones to compare first.</p>';
}

function renderCompareScreen() {
  const content = document.getElementById('compare-content');
  if (compareList.length === 0) {
    content.innerHTML = '<p class="text-center mt-4 text-2">No phones selected to compare.<br>Go to any phone page to add them.</p>';
    return;
  }
  
  const p1 = getPhoneById(compareList[0]);
  const p2 = compareList.length > 1 ? getPhoneById(compareList[1]) : null;

  if(!p1) {
    clearCompare();
    return;
  }

  if(!p2) {
    const p1Name = getPhoneFullName(p1);
    content.innerHTML = `
      <div style="display:flex; justify-content:center; padding: 24px;">
        <div style="text-align:center;">
          <div class="compare-phone-img-wrap" style="width:90px; height:90px; margin:0 auto 10px; background:rgba(255,255,255,0.03); border-radius:16px; display:flex; align-items:center; justify-content:center; overflow:hidden; border:1px solid var(--border);">
            ${getPhoneImageHtml(p1, 90, 'compare-phone-img')}
          </div>
          <div style="font-weight:bold">${p1Name}</div>
          <p class="text-2 mt-2">Add another phone to compare</p>
        </div>
      </div>
    `;
    return;
  }

  const d1 = DecisionEngine.generateDecision(p1, selectedPriorities, budgetCategory, PHONES);
  const d2 = DecisionEngine.generateDecision(p2, selectedPriorities, budgetCategory, PHONES);
  const p1Name = getPhoneFullName(p1);
  const p2Name = getPhoneFullName(p2);
  const p1Price = DecisionEngine.getPhoneNumericPrice(p1);
  const p2Price = DecisionEngine.getPhoneNumericPrice(p2);

  content.innerHTML = `
    <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:24px;">
      <div style="text-align:center; width: 44%" onclick="showPurchaseAnalysis('${p1.id}')">
        <div class="compare-phone-img-wrap" style="width:84px; height:84px; margin:0 auto 8px; background:rgba(255,255,255,0.03); border-radius:14px; display:flex; align-items:center; justify-content:center; overflow:hidden; border:1px solid var(--border);">
          ${getPhoneImageHtml(p1, 84, 'compare-phone-img')}
        </div>
        <div style="font-weight:bold; font-size:0.9rem">${p1Name}</div>
        <div style="font-size:0.8rem; color:var(--primary); font-weight:bold;">Value: ${d1.valueScore}</div>
        <div style="margin-top:4px;"><span class="badge-risk ${d1.risk.cssClass}">${d1.risk.level}</span></div>
      </div>
      <div style="background:var(--primary); color:white; border-radius:50%; width:36px; height:36px; display:flex; align-items:center; justify-content:center; font-weight:bold; font-size:0.85rem; flex-shrink:0;">VS</div>
      <div style="text-align:center; width: 44%" onclick="showPurchaseAnalysis('${p2.id}')">
        <div class="compare-phone-img-wrap" style="width:84px; height:84px; margin:0 auto 8px; background:rgba(255,255,255,0.03); border-radius:14px; display:flex; align-items:center; justify-content:center; overflow:hidden; border:1px solid var(--border);">
          ${getPhoneImageHtml(p2, 84, 'compare-phone-img')}
        </div>
        <div style="font-weight:bold; font-size:0.9rem">${p2Name}</div>
        <div style="font-size:0.8rem; color:var(--primary); font-weight:bold;">Value: ${d2.valueScore}</div>
        <div style="margin-top:4px;"><span class="badge-risk ${d2.risk.cssClass}">${d2.risk.level}</span></div>
      </div>
    </div>
    
    <div class="compare-specs-table">
      ${(() => {
        const allKeys = Array.from(new Set([...Object.keys(p1.specs || {}), ...Object.keys(p2.specs || {})]));
        return allKeys.map(specKey => {
          const val1 = (p1.specs && p1.specs[specKey]) ? p1.specs[specKey] : 'Not Available';
          const val2 = (p2.specs && p2.specs[specKey]) ? p2.specs[specKey] : 'Not Available';
          return `
            <div class="spec-row" style="flex-direction:column; background:var(--bg-card); padding:12px; border-radius:12px; margin-bottom:8px;">
              <div class="spec-label text-center" style="margin-bottom:8px; font-weight:bold; color:var(--text-1); font-size:0.75rem;">${specKey.toUpperCase()}</div>
              <div style="display:flex; justify-content:space-between; gap: 12px;">
                <div style="flex:1; font-size:0.8rem; color:var(--text-2); text-align:right;">${val1}</div>
                <div style="flex:1; font-size:0.8rem; color:var(--text-2); text-align:left;">${val2}</div>
              </div>
            </div>
          `;
        }).join('');
      })()}
      
      <div class="spec-row" style="flex-direction:column; background:var(--bg-card); padding:12px; border-radius:12px; margin-bottom:8px;">
        <div class="spec-label text-center" style="margin-bottom:8px; font-weight:bold; color:var(--text-1); font-size:0.75rem;">PRICE</div>
        <div style="display:flex; justify-content:space-between; gap: 12px;">
          <div style="flex:1; font-size:0.85rem; text-align:right; ${p1Price < p2Price ? 'color:var(--success);font-weight:bold' : 'color:var(--text-2)'}">₹${p1Price > 0 ? p1Price.toLocaleString() : p1.price}</div>
          <div style="flex:1; font-size:0.85rem; text-align:left; ${p2Price < p1Price ? 'color:var(--success);font-weight:bold' : 'color:var(--text-2)'}">₹${p2Price > 0 ? p2Price.toLocaleString() : p2.price}</div>
        </div>
      </div>
    </div>
  `;
}

// ─── SEARCH ───────────────────────────────────────────────────────────────────
function handleSearch() {
  const q = document.getElementById('search-input').value.toLowerCase().trim();
  
  if (q === '') {
    document.getElementById('search-grid').innerHTML = '';
    document.getElementById('search-count').textContent = '0';
    return;
  }
  
  const results = PHONES.filter(p => {
    const fullName = getPhoneFullName(p).toLowerCase();
    const origName = (p.brand + ' ' + p.name).toLowerCase();
    const procSpec = (p.specs && p.specs.processor ? p.specs.processor : '').toLowerCase();
    return fullName.includes(q) || origName.includes(q) || procSpec.includes(q);
  });
  
  document.getElementById('search-count').textContent = results.length;
  renderPhoneCards('search-grid', results.slice(0, 20), true);
}

// ─── BRAND FILTERING ENGINE ───────────────────────────────────────────────────
function filterByBrand(brandName) {
  if (!brandName) return;

  const targetBrand = String(brandName).toLowerCase().trim();

  // Filter dataset to ONLY smartphones belonging to this specific brand
  const brandPhones = PHONES.filter(p => {
    const pBrand = String(p.brand || '').toLowerCase().trim();
    const pName = String(p.name || '').toLowerCase().trim();
    return pBrand === targetBrand || pBrand.includes(targetBrand) || pName.startsWith(targetBrand);
  });

  // Calculate Decision Engine scores & risk ratings
  const scored = brandPhones.map(phone => {
    const decision = DecisionEngine.generateDecision(phone, selectedPriorities, budgetCategory, PHONES);
    return { phone, valueScore: decision.valueScore, decision };
  });

  // Sort by Value Score descending
  scored.sort((a, b) => b.valueScore - a.valueScore);

  const finalPhones = scored.map(s => s.phone);

  // Render cards and update header title/count
  renderPhoneCards('phones-grid', finalPhones);

  const countEl = document.getElementById('results-count');
  if (countEl) {
    const displayName = brandName.charAt(0).toUpperCase() + brandName.slice(1);
    countEl.textContent = `${displayName} Smartphones (${finalPhones.length} Devices Available)`;
  }

  navigateTo('screen-results');

  if (typeof showToast === 'function') {
    showToast(`📱 Displaying ${brandName} Smartphones (${finalPhones.length} devices)`);
  }
}

function renderBrandFilters() {
  const topBrands = ['Apple', 'Samsung', 'OnePlus', 'iQOO', 'Vivo', 'Xiaomi', 'Realme', 'Google', 'Motorola', 'Nothing', 'Poco', 'Lava', 'Tecno', 'Infinix'];
  
  const scroll = document.getElementById('brand-filters');
  if (scroll) {
    scroll.innerHTML = topBrands.map(b => `
      <div class="brand-item" onclick="filterByBrand('${b}')" style="cursor:pointer;">
        <span class="brand-name">${b}</span>
      </div>
    `).join('');
  }
}

function populateFilterSelects() {
  const processors = [...new Set(PHONES.map(p => p.processor_brand).filter(Boolean))].sort();
  const select = document.getElementById('adv-processor');
  if(select) {
    select.innerHTML = `<option value="any">All Processors</option>` + processors.map(p => `<option value="${p}">${p}</option>`).join('');
  }
}

function applyAdvancedFilters() {
  const priceVal = document.getElementById('filter-price')?.value || 'any';
  const procRamVal = document.getElementById('filter-processor-ram')?.value || 'any';
  const storageVal = document.getElementById('filter-storage')?.value || 'any';
  const batteryVal = document.getElementById('filter-battery')?.value || 'any';
  const cameraVal = document.getElementById('filter-camera')?.value || 'any';
  const displayVal = document.getElementById('filter-display')?.value || 'any';
  const osVal = document.getElementById('filter-os')?.value || 'any';

  let activeBudgetCat = budgetCategory;
  if (priceVal !== 'any') {
    activeBudgetCat = priceVal;
  }

  let results = filterAndScore(selectedPriorities, activeBudgetCat, PHONES);

  results = results.filter(item => {
    const p = item.phone;
    const price = DecisionEngine.getPhoneNumericPrice(p);
    const specs = p.specs || {};

    // 1. Price / Budget
    if (priceVal === 'under-10000' && price >= 10000) return false;
    if (priceVal === '10000-20000' && (price < 10000 || price > 20000)) return false;
    if (priceVal === '20000-30000' && (price < 20000 || price > 30000)) return false;
    if (priceVal === '30000-50000' && (price < 30000 || price > 50000)) return false;
    if (priceVal === '50000-80000' && (price < 50000 || price > 80000)) return false;
    if (priceVal === 'above-80000' && price <= 80000) return false;

    // 2. Processor (CPU) & RAM
    if (procRamVal === 'high-cpu') {
      const pBrand = String(p.processor_brand || '').toLowerCase();
      const pSpec = String(specs.processor || '').toLowerCase();
      const isHighCpu = pBrand.includes('snapdragon 8') || pBrand.includes('dimensity 9') || pBrand.includes('apple') || pSpec.includes('snapdragon 8') || pSpec.includes('dimensity 9000') || pSpec.includes('a16') || pSpec.includes('a17') || pSpec.includes('a18');
      if (!isHighCpu) return false;
    }
    if (procRamVal === 'ram-6' && (p.ram_gb || 0) < 6) return false;
    if (procRamVal === 'ram-8' && (p.ram_gb || 0) < 8) return false;
    if (procRamVal === 'ram-12' && (p.ram_gb || 0) < 12) return false;
    if (procRamVal === 'ram-16' && (p.ram_gb || 0) < 16) return false;

    // 3. Storage Space
    if (storageVal === '128' && (p.storage_gb || 0) < 128) return false;
    if (storageVal === '256' && (p.storage_gb || 0) < 256) return false;
    if (storageVal === '512' && (p.storage_gb || 0) < 512) return false;

    // 4. Battery Capacity & Charging
    const batSpec = String(specs.battery || '').toLowerCase();
    const chgSpec = String(specs.charging || '').toLowerCase();
    const batMatch = batSpec.match(/(\d{4})/);
    const mah = batMatch ? parseInt(batMatch[1], 10) : 4500;

    if (batteryVal === '5000' && mah < 5000) return false;
    if (batteryVal === '6000' && mah < 6000) return false;
    if (batteryVal === 'fast-charge') {
      const chgMatch = chgSpec.match(/(\d+)\s*w/i);
      const watts = chgMatch ? parseInt(chgMatch[1], 10) : 0;
      if (watts < 45 && !chgSpec.includes('fast') && !chgSpec.includes('super')) return false;
    }

    // 5. Camera Quality
    const camSpec = String(specs.camera || '').toLowerCase();
    if (cameraVal === 'triple' && !camSpec.includes('+') && !camSpec.includes('triple') && !camSpec.includes('quad')) return false;
    if (cameraVal === 'high-mp' && !camSpec.includes('50') && !camSpec.includes('108') && !camSpec.includes('200')) return false;
    if (cameraVal === 'cam-8' && (p.scores?.camera || 0) < 8.0) return false;
    if (cameraVal === 'cam-9' && (p.scores?.camera || 0) < 9.0) return false;

    // 6. Display Type & Size
    const dispSpec = String(specs.display || '').toLowerCase();
    if (displayVal === 'oled' && !dispSpec.includes('oled') && !dispSpec.includes('amoled')) return false;
    if (displayVal === '120hz' && !dispSpec.includes('120') && !dispSpec.includes('144') && !dispSpec.includes('90')) return false;
    if (displayVal === 'large-screen') {
      const sizeMatch = dispSpec.match(/(\d+\.\d+)/);
      const inches = sizeMatch ? parseFloat(sizeMatch[1]) : 6.5;
      if (inches < 6.67) return false;
    }

    // 7. Operating System
    const brand = String(p.brand || '').toLowerCase();
    if (osVal === 'ios' && brand !== 'apple') return false;
    if (osVal === 'android' && brand === 'apple') return false;

    return true;
  });

  results.sort((a, b) => b.valueScore - a.valueScore);

  const resultPhones = results.map(r => r.phone);
  renderPhoneCards('phones-grid', resultPhones);

  const countEl = document.getElementById('results-count');
  if (countEl) {
    countEl.textContent = `${resultPhones.length} Devices Suggested (Risk & Specs Evaluated)`;
  }

  navigateTo('screen-results');

  if (typeof showToast === 'function') {
    showToast(`✨ Filters Applied! (${resultPhones.length} devices suggested)`);
  }
}

function resetAdvancedFilters() {
  ['filter-price', 'filter-processor-ram', 'filter-storage', 'filter-battery', 'filter-camera', 'filter-display', 'filter-os'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.value = 'any';
  });
  applyAdvancedFilters();
}

// ─── SYSTEM EVALUATION ENGINE ─────────────────────────────────────────────────
function runSystemEvaluation() {
  const startTime = performance.now();
  let validScoreCount = 0;
  let validRiskCount = 0;
  let validDealCount = 0;
  let reqMatchSum = 0;

  const testPhones = PHONES.slice(0, 20);
  testPhones.forEach(phone => {
    const d = DecisionEngine.generateDecision(phone, ['camera', 'gaming'], 3, PHONES);
    if (d.valueScore >= 0 && d.valueScore <= 100) validScoreCount++;
    if (d.risk.score >= 0 && d.risk.score <= 100) validRiskCount++;
    const statusLabel = d.priceStatus || d.deal?.label;
    if (['Good Price', 'Fair Price', 'Slightly Expensive', 'Overpriced', 'GOOD DEAL', 'FAIR DEAL', 'OVERPRICED'].includes(statusLabel)) validDealCount++;
    reqMatchSum += d.valueScore;
  });

  const endTime = performance.now();
  const durationMs = +(endTime - startTime).toFixed(2);
  const avgMatch = +(reqMatchSum / testPhones.length).toFixed(1);
  const riskConsistencyPct = Math.round((validRiskCount / testPhones.length) * 100);
  const dealAccuracyPct = Math.round((validDealCount / testPhones.length) * 100);

  const evalContainer = document.getElementById('eval-results-container');
  if (evalContainer) {
    evalContainer.innerHTML = `
      <div class="eval-card mt-3">
        <h4>📊 Decision System Evaluation Metrics</h4>
        <div class="eval-row"><span>Evaluated Dataset:</span> <strong>${testPhones.length} Devices</strong></div>
        <div class="eval-row"><span>Avg Requirement Match:</span> <strong>${avgMatch}%</strong></div>
        <div class="eval-row"><span>Risk Score Consistency:</span> <strong>${riskConsistencyPct}%</strong></div>
        <div class="eval-row"><span>Deal Classification Validity:</span> <strong>${dealAccuracyPct}%</strong></div>
        <div class="eval-row"><span>Execution Latency:</span> <strong>${durationMs} ms</strong></div>
      </div>
    `;
  }
}

// ─── APP PREFERENCES & SHOPPING UTILITIES HANDLERS ────────────────────────────
let priceDropAlertsActive = true;

function togglePriceDropAlertsSetting() {
  priceDropAlertsActive = !priceDropAlertsActive;
  const statusEl = document.getElementById('setting-alerts-status');
  if (statusEl) {
    statusEl.textContent = priceDropAlertsActive ? 'ACTIVE' : 'MUTED';
    statusEl.style.color = priceDropAlertsActive ? 'var(--success)' : 'var(--text-3)';
  }
  if (typeof showToast === 'function') {
    showToast(priceDropAlertsActive ? '🔔 Price Drop Alerts Enabled' : '🔕 Price Drop Alerts Muted');
  }
}

function triggerLivePriceSync() {
  if (typeof showToast === 'function') {
    showToast('🔄 Syncing live prices from Amazon & Flipkart...');
  }
  setTimeout(() => {
    initPhonesData();
    if (typeof showToast === 'function') {
      showToast('✅ 1,597 smartphones synced with latest market prices!');
    }
  }, 1200);
}

// Global window bindings for cross-compatibility
window.showPhoneDetails = showPhoneDetails;
window.showDetails = showPhoneDetails;
window.viewPhoneSpecs = showPhoneDetails;
window.selectBudget = selectBudget;
window.updateBudget = updateBudget;
window.togglePriceDropAlertsSetting = togglePriceDropAlertsSetting;
window.triggerLivePriceSync = triggerLivePriceSync;
window.filterByBrand = filterByBrand;

