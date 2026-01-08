'use client';

import { useQuery } from '@tanstack/react-query';
import { simulationAPI } from '@/lib/api';
import { WorldIndicator } from '@/lib/types';
import { TrendingUp, TrendingDown, AlertTriangle, DollarSign, Users, Home, Zap, Activity } from 'lucide-react';
import { useState } from 'react';

function getCategoryIcon(category: string) {
  switch (category.toLowerCase()) {
    case 'economic': return DollarSign;
    case 'social': return Users;
    case 'political': return Home;
    case 'environmental': return Zap;
    default: return Activity;
  }
}

function getTrendIcon(trend: string) {
  switch (trend) {
    case 'increasing': return TrendingUp;
    case 'decreasing': return TrendingDown;
    default: return Activity;
  }
}

function getTrendColor(trend: string) {
  switch (trend) {
    case 'increasing': return 'text-red-500';
    case 'decreasing': return 'text-green-500';
    default: return 'text-slate-500';
  }
}

interface IndicatorCardProps {
  indicator: WorldIndicator;
}

function IndicatorCard({ indicator }: IndicatorCardProps) {
  const Icon = getCategoryIcon(indicator.category);
  const TrendIcon = getTrendIcon(indicator.trend);
  const trendColor = getTrendColor(indicator.trend);

  return (
    <div className="bg-white rounded-lg shadow-md p-6 border border-slate-200">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center">
          <div className="bg-blue-100 rounded-lg p-3 mr-3">
            <Icon className="w-5 h-5 text-blue-600" />
          </div>
          <div>
            <h3 className="text-sm font-medium text-slate-900">{indicator.name}</h3>
            <span className="text-xs text-slate-500 capitalize">{indicator.category}</span>
          </div>
        </div>
        <TrendIcon className={`w-5 h-5 ${trendColor}`} />
      </div>
      
      <div className="mb-2">
        <span className="text-2xl font-bold text-slate-900">{indicator.value}</span>
        {indicator.unit && <span className="text-slate-600 ml-1">{indicator.unit}</span>}
      </div>
      
      <div className="flex items-center justify-between text-xs text-slate-500">
        <span>Source: {indicator.source}</span>
        <span>{new Date(indicator.last_updated).toLocaleDateString()}</span>
      </div>
    </div>
  );
}

interface RiskLevelProps {
  level: string;
  score: number;
}

function RiskLevel({ level, score }: RiskLevelProps) {
  const colors = {
    'LOW': 'bg-green-100 text-green-800 border-green-300',
    'MODERATE': 'bg-yellow-100 text-yellow-800 border-yellow-300',
    'HIGH': 'bg-orange-100 text-orange-800 border-orange-300',
    'CRITICAL': 'bg-red-100 text-red-800 border-red-300'
  };

  return (
    <div className={`rounded-lg p-4 border-2 ${colors[level as keyof typeof colors] || colors.MODERATE}`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium">Risk Level</p>
          <p className="text-2xl font-bold">{level}</p>
        </div>
        <div className="text-right">
          <p className="text-sm font-medium">Score</p>
          <p className="text-2xl font-bold">{(score * 100).toFixed(1)}%</p>
        </div>
      </div>
    </div>
  );
}

export default function SimulationPage() {
  const [selectedCategory, setSelectedCategory] = useState<string>('all');

  const { data: indicators, isLoading: indicatorsLoading } = useQuery({
    queryKey: ['world-indicators'],
    queryFn: async () => {
      const response = await simulationAPI.getIndicators();
      return response.data;
    },
  });

  const { data: riskAssessment, isLoading: riskLoading } = useQuery({
    queryKey: ['risk-assessment'],
    queryFn: async () => {
      const response = await simulationAPI.getRiskAssessment();
      return response.data;
    },
  });

  const { data: preconditions } = useQuery({
    queryKey: ['pattern-preconditions'],
    queryFn: async () => {
      const response = await simulationAPI.getPreconditions();
      return response.data;
    },
  });

  const filteredIndicators = indicators?.filter((ind: WorldIndicator) => 
    selectedCategory === 'all' || ind.category === selectedCategory
  );

  const categories = ['all', ...Array.from(new Set(indicators?.map((ind: WorldIndicator) => ind.category) || []))];

  if (indicatorsLoading || riskLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-slate-600">Loading simulation data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900 mb-2">World Simulation Dashboard</h1>
        <p className="text-slate-600">
          Real-time monitoring of global indicators and civilizational risk assessment.
          {indicators && ` Tracking ${indicators.length} indicators across multiple categories.`}
        </p>
      </div>

      {riskAssessment && (
        <div className="mb-8">
          <RiskLevel level={riskAssessment.risk_level} score={riskAssessment.overall_risk} />
        </div>
      )}

      {riskAssessment && riskAssessment.pattern_assessments && riskAssessment.pattern_assessments.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-8 border border-slate-200">
          <h2 className="text-xl font-semibold text-slate-900 mb-4 flex items-center">
            <AlertTriangle className="w-5 h-5 mr-2 text-orange-500" />
            Pattern Risk Assessment
          </h2>
          <div className="space-y-3">
            {riskAssessment.pattern_assessments.map((assessment: any, idx: number) => (
              <div key={idx} className="bg-slate-50 rounded-lg p-4 border border-slate-200">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h3 className="font-semibold text-slate-900">{assessment.pattern_name}</h3>
                    <p className="text-sm text-slate-600 mt-1">{assessment.assessment}</p>
                  </div>
                  <div className="flex flex-col items-end gap-1">
                    <span className={`text-xs font-medium px-2.5 py-1 rounded ${
                      assessment.risk_level === 'HIGH' ? 'bg-red-100 text-red-800' :
                      assessment.risk_level === 'MODERATE' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-green-100 text-green-800'
                    }`}>
                      {assessment.risk_level}
                    </span>
                    <span className="text-xs bg-blue-100 text-blue-800 px-2.5 py-1 rounded">
                      {Math.round(assessment.match_score * 100)}% match
                    </span>
                  </div>
                </div>
                {assessment.matched_preconditions && assessment.matched_preconditions.length > 0 && (
                  <div className="mt-3">
                    <p className="text-xs text-slate-500 mb-2">Matched Preconditions:</p>
                    <div className="flex flex-wrap gap-1">
                      {assessment.matched_preconditions.map((precond: string, i: number) => (
                        <span key={i} className="bg-orange-100 text-orange-700 text-xs px-2 py-1 rounded">
                          {precond}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {riskAssessment && riskAssessment.indicator_summary && (
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-6 mb-8 border border-blue-200">
          <h2 className="text-xl font-semibold text-slate-900 mb-4">Indicator Summary</h2>
          <div className="grid md:grid-cols-4 gap-4">
            <div className="bg-white rounded-lg p-4">
              <p className="text-slate-600 text-sm">Total Indicators</p>
              <p className="text-2xl font-bold text-blue-600">{riskAssessment.indicator_summary.total_indicators}</p>
            </div>
            <div className="bg-white rounded-lg p-4">
              <p className="text-slate-600 text-sm">Critical</p>
              <p className="text-2xl font-bold text-red-600">{riskAssessment.indicator_summary.critical_count}</p>
            </div>
            <div className="bg-white rounded-lg p-4">
              <p className="text-slate-600 text-sm">Warning</p>
              <p className="text-2xl font-bold text-orange-600">{riskAssessment.indicator_summary.warning_count}</p>
            </div>
            <div className="bg-white rounded-lg p-4">
              <p className="text-slate-600 text-sm">Normal</p>
              <p className="text-2xl font-bold text-green-600">{riskAssessment.indicator_summary.normal_count}</p>
            </div>
          </div>
        </div>
      )}

      <div className="mb-6">
        <div className="flex flex-wrap gap-2">
          {categories.map((category) => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                selectedCategory === category
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-slate-700 border border-slate-300 hover:bg-slate-50'
              }`}
            >
              {category === 'all' ? 'All Categories' : category.charAt(0).toUpperCase() + category.slice(1)}
            </button>
          ))}
        </div>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredIndicators && filteredIndicators.map((indicator: WorldIndicator) => (
          <IndicatorCard key={indicator.id} indicator={indicator} />
        ))}
      </div>

      {preconditions && preconditions.length > 0 && (
        <div className="mt-8 bg-white rounded-lg shadow-md p-6 border border-slate-200">
          <h2 className="text-xl font-semibold text-slate-900 mb-4">Active Pattern Preconditions</h2>
          <div className="grid md:grid-cols-2 gap-4">
            {preconditions.slice(0, 6).map((precondition: any, idx: number) => (
              <div key={idx} className="bg-slate-50 rounded-lg p-4 border border-slate-200">
                <h3 className="font-semibold text-slate-900 mb-2">{precondition.pattern_name}</h3>
                <div className="space-y-2">
                  {precondition.matched_conditions?.map((condition: string, i: number) => (
                    <div key={i} className="flex items-start">
                      <span className="text-green-500 mr-2">✓</span>
                      <span className="text-sm text-slate-600">{condition}</span>
                    </div>
                  ))}
                </div>
                <div className="mt-3 pt-3 border-t border-slate-200">
                  <span className="text-xs text-slate-500">
                    {precondition.matched_count || 0} / {precondition.total_conditions || 0} conditions met
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
