import React from 'react';
import { Smartphone, Compass, Sparkles, Scale, Bookmark, Settings, Sun, Moon } from 'lucide-react';

interface NavbarProps {
  currentScreen: string;
  onNavigate: (screen: string) => void;
  isDark: boolean;
  onToggleTheme: () => void;
  savedCount: number;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentScreen,
  onNavigate,
  isDark,
  onToggleTheme,
  savedCount
}) => {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: Smartphone },
    { id: 'discovery', label: 'Catalog', icon: Compass },
    { id: 'wizard', label: 'Match Wizard', icon: Sparkles },
    { id: 'compare', label: 'Compare', icon: Scale },
    { id: 'saved', label: 'Saved', icon: Bookmark, badge: savedCount > 0 ? savedCount : null },
  ];

  return (
    <header className="sticky top-0 z-50 glass-panel border-b border-slate-800 bg-slate-950/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand Logo */}
        <div 
          onClick={() => onNavigate('dashboard')} 
          className="flex items-center space-x-3 cursor-pointer group"
        >
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center text-white font-bold shadow-lg shadow-sky-500/20 group-hover:scale-105 transition-transform">
            P2
          </div>
          <div>
            <div className="font-extrabold text-lg tracking-tight bg-gradient-to-r from-white via-slate-100 to-slate-400 bg-clip-text text-transparent">
              PhonePerfect <span className="text-sky-400 font-semibold text-xs ml-1 px-1.5 py-0.5 rounded-full bg-sky-950/80 border border-sky-800">2.0</span>
            </div>
            <div className="text-[10px] text-slate-400 font-medium tracking-wide">Intelligent Decision Engine</div>
          </div>
        </div>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex items-center space-x-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentScreen === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onNavigate(item.id)}
                className={`flex items-center space-x-2 px-3.5 py-2 rounded-lg text-sm font-medium transition-all relative ${
                  isActive 
                    ? 'bg-sky-500/10 text-sky-400 border border-sky-500/30 shadow-sm'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-sky-400' : 'text-slate-400'}`} />
                <span>{item.label}</span>
                {item.badge && (
                  <span className="ml-1 px-1.5 py-0.2 text-[10px] font-bold bg-sky-500 text-slate-950 rounded-full">
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>

        {/* Right Actions */}
        <div className="flex items-center space-x-2">
          <button
            onClick={() => onNavigate('settings')}
            className={`p-2 rounded-lg transition-colors ${
              currentScreen === 'settings' 
                ? 'bg-slate-800 text-sky-400' 
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
            }`}
            title="Settings & Preferences"
          >
            <Settings className="w-5 h-5" />
          </button>
          <button
            onClick={onToggleTheme}
            className="p-2 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800/60 transition-colors"
            title="Toggle Theme"
          >
            {isDark ? <Sun className="w-5 h-5 text-amber-400" /> : <Moon className="w-5 h-5" />}
          </button>
        </div>
      </div>
    </header>
  );
};
