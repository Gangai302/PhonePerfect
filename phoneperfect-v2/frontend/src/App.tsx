import React, { useState } from 'react';
import { Navbar } from './components/layout/Navbar';
import { HomeDashboard } from './pages/HomeDashboard';
import { RequirementsWizard } from './pages/RequirementsWizard';
import { RecommendationResults } from './pages/RecommendationResults';
import { DiscoveryCatalog } from './pages/DiscoveryCatalog';
import { PhoneProfile } from './pages/PhoneProfile';
import { SideBySideCompare } from './pages/SideBySideCompare';
import { RecommendationResponse } from './types';

export const App: React.FC = () => {
  const [currentScreen, setCurrentScreen] = useState<string>('dashboard');
  const [isDark, setIsDark] = useState<boolean>(true);
  
  // App state
  const [recommendationResults, setRecommendationResults] = useState<RecommendationResponse | null>(null);
  const [selectedPhoneId, setSelectedPhoneId] = useState<string | null>(null);
  const [compareIds, setCompareIds] = useState<string[]>([]);
  const [savedPhoneIds, setSavedPhoneIds] = useState<string[]>([]);

  const handleToggleTheme = () => {
    setIsDark(!isDark);
    if (!isDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  };

  const handleSelectPhone = (phoneId: string) => {
    setSelectedPhoneId(phoneId);
    setCurrentScreen('profile');
  };

  const handleAddToCompare = (phoneId: string) => {
    if (!compareIds.includes(phoneId)) {
      if (compareIds.length >= 4) {
        alert('You can compare a maximum of 4 smartphones simultaneously.');
        return;
      }
      setCompareIds([...compareIds, phoneId]);
    }
    setCurrentScreen('compare');
  };

  const handleRemoveFromCompare = (phoneId: string) => {
    setCompareIds(compareIds.filter(id => id !== phoneId));
  };

  const handleClearCompare = () => {
    setCompareIds([]);
  };

  return (
    <div className={`min-h-screen ${isDark ? 'bg-slate-950 text-slate-100' : 'bg-slate-50 text-slate-900'}`}>
      <Navbar
        currentScreen={currentScreen}
        onNavigate={(screen) => setCurrentScreen(screen)}
        isDark={isDark}
        onToggleTheme={handleToggleTheme}
        savedCount={savedPhoneIds.length}
      />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8">
        {currentScreen === 'dashboard' && (
          <HomeDashboard
            onStartWizard={() => setCurrentScreen('wizard')}
            onExploreCatalog={() => setCurrentScreen('discovery')}
            onCompare={() => setCurrentScreen('compare')}
          />
        )}

        {currentScreen === 'wizard' && (
          <RequirementsWizard
            onResultsGenerated={(results) => {
              setRecommendationResults(results);
              setCurrentScreen('results');
            }}
            onCancel={() => setCurrentScreen('dashboard')}
          />
        )}

        {currentScreen === 'results' && recommendationResults && (
          <RecommendationResults
            results={recommendationResults}
            onSelectPhone={handleSelectPhone}
            onAddToCompare={handleAddToCompare}
            onBackToWizard={() => setCurrentScreen('wizard')}
          />
        )}

        {currentScreen === 'discovery' && (
          <DiscoveryCatalog
            onSelectPhone={handleSelectPhone}
            onAddToCompare={handleAddToCompare}
          />
        )}

        {currentScreen === 'profile' && selectedPhoneId && (
          <PhoneProfile
            phoneId={selectedPhoneId}
            onBack={() => setCurrentScreen(recommendationResults ? 'results' : 'discovery')}
            onAddToCompare={handleAddToCompare}
          />
        )}

        {currentScreen === 'compare' && (
          <SideBySideCompare
            compareIds={compareIds}
            onRemoveFromCompare={handleRemoveFromCompare}
            onClearCompare={handleClearCompare}
            onBack={() => setCurrentScreen('discovery')}
          />
        )}
      </main>
    </div>
  );
};

export default App;
