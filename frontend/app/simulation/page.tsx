'use client';

import { useQuery } from '@tanstack/react-query';
import { simulationAPI } from '@/lib/api';
import { 
  TrendingUp, 
  TrendingDown, 
  AlertTriangle, 
  DollarSign, 
  Users, 
  Home, 
  Zap, 
  Activity, 
  Shield, 
  Swords,
  ChevronLeft,
  ChevronRight,
  Maximize2,
  Target,
  BarChart3
} from 'lucide-react';
import { useState, useMemo } from 'react';

// Category Icons
function getCategoryIcon(category: string) {
  switch (category.toLowerCase()) {
    case 'economic': return DollarSign;
    case 'social': return Users;
    case 'political': return Home;
    case 'environmental': return Zap;
    case 'military': return Swords;
    case 'religious': return Shield;
    default: return Activity;
  }
}

// Number formatting for large values
function formatLargeNumber(num: number): string {
  if (num >= 1e12) return `${(num / 1e12).toFixed(2)}T`;
  if (num >= 1e9) return `${(num / 1e9).toFixed(2)}B`;
  if (num >= 1e6) return `${(num / 1e6).toFixed(2)}M`;
  if (num >= 1e3) return `${(num / 1e3).toFixed(1)}K`;
  return num.toFixed(1);
}

// Severity color based on value
function getSeverityColor(value: number, maxValue: number = 10): string {
  const ratio = value / maxValue;
  if (ratio >= 0.8) return 'text-red-600 bg-red-100 border-red-300';
  if (ratio >= 0.6) return 'text-orange-600 bg-orange-100 border-orange-300';
  if (ratio >= 0.4) return 'text-yellow-600 bg-yellow-100 border-yellow-300';
  return 'text-green-600 bg-green-100 border-green-300';
}

interface SlideIndicatorProps {
  indicator: any;
  isExpanded?: boolean;
}

function SlideIndicator({ indicator, isExpanded = false }: SlideIndicatorProps) {
  const Icon = getCategoryIcon(indicator.name.includes('Christian') || indicator.name.includes('Religious') || indicator.name.includes('Secularization') || indicator.name.includes('Apostasy') || indicator.name.includes('Prophetic') ? 'religious' : 'social');
  const formattedValue = indicator.value >= 100 ? formatLargeNumber(indicator.value) : indicator.value.toFixed(2);
  const severityClass = indicator.value <= 10 ? getSeverityColor(indicator.value, 10) : 'text-slate-700 bg-slate-100 border-slate-300';

  return (
    <div className={`bg-white rounded-xl border-2 shadow-lg transition-all duration-300 ${isExpanded ? 'p-8' : 'p-6'} hover:shadow-2xl`}>
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-4">
          <div className={`p-4 rounded-xl ${severityClass}`}>
            <Icon className="w-8 h-8" />
          </div>
          <div>
            <h3 className={`font-bold text-slate-900 ${isExpanded ? 'text-2xl' : 'text-lg'}`}>
              {indicator.name}
            </h3>
            <p className="text-sm text-slate-500 mt-1">{indicator.description}</p>
          </div>
        </div>
      </div>
      
      <div className="flex items-baseline gap-3 mb-4">
        <span className={`font-bold ${isExpanded ? 'text-5xl' : 'text-4xl'} text-slate-900`}>
          {formattedValue}
        </span>
        {indicator.value <= 10 && (
          <span className="text-lg text-slate-500">/ 10</span>
        )}
      </div>

      <div className="flex items-center justify-between text-sm text-slate-600">
        <span className="flex items-center gap-2">
          <BarChart3 className="w-4 h-4" />
          {new Date(indicator.timestamp).toLocaleDateString()}
        </span>
        {indicator.value <= 10 && (
          <span className={`px-3 py-1 rounded-full font-semibold text-xs ${severityClass}`}>
            {indicator.value >= 8 ? 'CRITICAL' : indicator.value >= 6 ? 'HIGH' : indicator.value >= 4 ? 'MODERATE' : 'LOW'}
          </span>
        )}
      </div>
    </div>
  );
}

interface CategorySlideProps {
  category: string;
  indicators: any[];
  onIndicatorClick: (indicator: any) => void;
}

function CategorySlide({ category, indicators, onIndicatorClick }: CategorySlideProps) {
  const Icon = getCategoryIcon(category);
  const avgValue = indicators.reduce((sum, ind) => sum + (ind.value <= 10 ? ind.value : 0), 0) / indicators.filter(ind => ind.value <= 10).length;
  const severity = avgValue >= 7 ? 'CRITICAL' : avgValue >= 5 ? 'HIGH' : avgValue >= 3 ? 'MODERATE' : 'LOW';
  const severityColor = avgValue >= 7 ? 'bg-red-600' : avgValue >= 5 ? 'bg-orange-600' : avgValue >= 3 ? 'bg-yellow-600' : 'bg-green-600';

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-100 p-8">
      {/* Category Header */}
      <div className="max-w-7xl mx-auto mb-12">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-6">
            <div className={`p-6 rounded-2xl ${severityColor} shadow-2xl`}>
              <Icon className="w-16 h-16 text-white" />
            </div>
            <div>
              <h1 className="text-5xl font-bold text-slate-900 mb-2 capitalize">
                {category} Indicators
              </h1>
              <p className="text-xl text-slate-600">
                {indicators.length} key metrics &bull; Average Severity: {severity}
              </p>
            </div>
          </div>
          <div className={`px-8 py-4 rounded-2xl ${severityColor} text-white shadow-xl`}>
            <div className="text-sm font-semibold uppercase tracking-wider mb-1">Avg Score</div>
            <div className="text-4xl font-bold">{avgValue.toFixed(1)}</div>
          </div>
        </div>
      </div>

      {/* Indicators Grid */}
      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-6">
        {indicators.map((indicator, idx) => (
          <div key={idx} onClick={() => onIndicatorClick(indicator)} className="cursor-pointer">
            <SlideIndicator indicator={indicator} />
          </div>
        ))}
      </div>
    </div>
  );
}

function RiskAssessmentSlide({ riskData }: { riskData: any }) {
  const riskLevel = riskData.risk_level.toUpperCase();
  const riskScore = (riskData.overall_risk_score * 100).toFixed(1);
  const riskColor = riskLevel === 'CRITICAL' ? 'bg-red-600' : riskLevel === 'HIGH' ? 'bg-orange-600' : riskLevel === 'MODERATE' ? 'bg-yellow-600' : 'bg-green-600';
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-indigo-900 to-slate-900 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Main Risk Display */}
        <div className="text-center mb-16">
          <h1 className="text-6xl font-bold text-white mb-8">
            Civilizational Risk Assessment
          </h1>
          <div className={`inline-block px-16 py-12 rounded-3xl ${riskColor} shadow-2xl`}>
            <div className="text-3xl font-bold text-white uppercase tracking-wider mb-4">
              {riskLevel} RISK
            </div>
            <div className="text-8xl font-bold text-white mb-4">
              {riskScore}%
            </div>
            <div className="text-xl text-white opacity-90">
              Overall Risk Score
            </div>
          </div>
        </div>

        {/* Top Pattern Risks */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
          {riskData.top_risks.slice(0, 3).map((risk: any, idx: number) => (
            <div key={idx} className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border-2 border-white/20">
              <div className="flex items-center justify-between mb-6">
                <AlertTriangle className="w-12 h-12 text-yellow-400" />
                <span className="text-5xl font-bold text-white opacity-50">
                  #{idx + 1}
                </span>
              </div>
              <h3 className="text-2xl font-bold text-white mb-4">
                {risk.pattern_name}
              </h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-white/70">Match Score</span>
                  <span className="text-2xl font-bold text-white">{(risk.match_score * 100).toFixed(0)}%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-white/70">Weighted Risk</span>
                  <span className="text-2xl font-bold text-yellow-400">{(risk.weighted_risk * 100).toFixed(0)}%</span>
                </div>
              </div>
              <div className="mt-6">
                <div className="text-white/70 text-sm mb-2">Matched Preconditions:</div>
                <div className="flex flex-wrap gap-2">
                  {risk.matched_preconditions.map((cond: string, i: number) => (
                    <span key={i} className="bg-yellow-500/20 text-yellow-200 px-3 py-1 rounded-full text-xs font-medium border border-yellow-500/30">
                      {cond.replace(/_/g, ' ')}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-6">
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20 text-center">
            <div className="text-4xl font-bold text-white mb-2">{riskData.total_patterns_assessed}</div>
            <div className="text-white/70">Patterns Assessed</div>
          </div>
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20 text-center">
            <div className="text-4xl font-bold text-white mb-2">{riskData.patterns_with_matches}</div>
            <div className="text-white/70">Patterns with Matches</div>
          </div>
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20 text-center">
            <div className="text-4xl font-bold text-white mb-2">{riskData.top_risks.length}</div>
            <div className="text-white/70">High Risk Patterns</div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function SimulationPage() {
  const [currentSlide, setCurrentSlide] = useState(0);
  const [selectedIndicator, setSelectedIndicator] = useState<any>(null);

  const { data: indicatorsData, isLoading: indicatorsLoading, error: indicatorsError } = useQuery({
    queryKey: ['world-indicators'],
    queryFn: async () => {
      const response = await simulationAPI.getIndicators();
      return response.data;
    },
  });

  const { data: riskData, isLoading: riskLoading, error: riskError } = useQuery({
    queryKey: ['risk-assessment'],
    queryFn: async () => {
      const response = await simulationAPI.getRiskAssessment();
      return response.data;
    },
  });

  // Organize indicators by category
  const categorizedIndicators = useMemo(() => {
    if (!indicatorsData?.by_category) return [];
    return Object.entries(indicatorsData.by_category).map(([category, indicators]) => ({
      category,
      indicators: indicators as any[]
    }));
  }, [indicatorsData]);

  const totalSlides = categorizedIndicators.length + (riskData ? 1 : 0);

  const goToNextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % totalSlides);
    setSelectedIndicator(null);
  };

  const goToPrevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + totalSlides) % totalSlides);
    setSelectedIndicator(null);
  };

  if (indicatorsLoading || riskLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-slate-900 to-slate-800">
        <div className="text-center">
          <div className="animate-spin rounded-full h-20 w-20 border-t-4 border-b-4 border-blue-500 mx-auto mb-6"></div>
          <p className="text-2xl text-white font-semibold">Loading World Simulation...</p>
          <p className="text-slate-400 mt-2">Analyzing civilizational indicators</p>
        </div>
      </div>
    );
  }

  if (indicatorsError || riskError) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-red-900 to-slate-900">
        <div className="text-center max-w-2xl px-8">
          <AlertTriangle className="w-20 h-20 text-red-400 mx-auto mb-6" />
          <h1 className="text-4xl font-bold text-white mb-4">Simulation Data Unavailable</h1>
          <p className="text-xl text-slate-300 mb-6">
            Unable to load world simulation data. The backend service may be unavailable.
          </p>
          <button 
            onClick={() => window.location.reload()}
            className="px-8 py-4 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-semibold transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="relative min-h-screen bg-slate-50">
      {/* Slide Content */}
      <div className="relative">
        {/* Risk Assessment Slide (First Slide) */}
        {currentSlide === 0 && riskData && (
          <RiskAssessmentSlide riskData={riskData} />
        )}

        {/* Category Slides */}
        {currentSlide > 0 && categorizedIndicators[currentSlide - 1] && (
          <CategorySlide 
            category={categorizedIndicators[currentSlide - 1].category}
            indicators={categorizedIndicators[currentSlide - 1].indicators}
            onIndicatorClick={setSelectedIndicator}
          />
        )}
      </div>

      {/* Navigation Controls */}
      <div className="fixed bottom-8 left-1/2 transform -translate-x-1/2 z-50">
        <div className="bg-slate-900/90 backdrop-blur-lg rounded-full px-8 py-4 shadow-2xl border border-slate-700">
          <div className="flex items-center gap-6">
            <button
              onClick={goToPrevSlide}
              className="p-3 rounded-full bg-slate-800 hover:bg-slate-700 text-white transition-all hover:scale-110"
              aria-label="Previous slide"
            >
              <ChevronLeft className="w-6 h-6" />
            </button>
            
            <div className="flex items-center gap-4">
              <span className="text-white font-bold text-lg">
                {currentSlide + 1} / {totalSlides}
              </span>
              <div className="flex gap-2">
                {Array.from({ length: totalSlides }).map((_, idx) => (
                  <button
                    key={idx}
                    onClick={() => setCurrentSlide(idx)}
                    className={`h-2 rounded-full transition-all ${
                      idx === currentSlide 
                        ? 'w-8 bg-blue-500' 
                        : 'w-2 bg-slate-600 hover:bg-slate-500'
                    }`}
                    aria-label={`Go to slide ${idx + 1}`}
                  />
                ))}
              </div>
            </div>

            <button
              onClick={goToNextSlide}
              className="p-3 rounded-full bg-slate-800 hover:bg-slate-700 text-white transition-all hover:scale-110"
              aria-label="Next slide"
            >
              <ChevronRight className="w-6 h-6" />
            </button>
          </div>
        </div>
      </div>

      {/* Slide Counter (Top Right) */}
      <div className="fixed top-8 right-8 z-40">
        <div className="bg-slate-900/90 backdrop-blur-lg rounded-xl px-6 py-3 shadow-xl border border-slate-700">
          <div className="text-white text-sm font-medium">
            {currentSlide === 0 ? 'Risk Assessment' : categorizedIndicators[currentSlide - 1]?.category.toUpperCase()}
          </div>
        </div>
      </div>

      {/* Expanded Indicator Modal */}
      {selectedIndicator && (
        <div 
          className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-8"
          onClick={() => setSelectedIndicator(null)}
        >
          <div 
            className="max-w-4xl w-full"
            onClick={(e) => e.stopPropagation()}
          >
            <SlideIndicator indicator={selectedIndicator} isExpanded />
            <button
              onClick={() => setSelectedIndicator(null)}
              className="mt-6 w-full py-4 bg-slate-800 hover:bg-slate-700 text-white rounded-xl font-semibold transition-colors"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
