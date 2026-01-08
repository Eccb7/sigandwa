'use client';

import { useQuery } from '@tanstack/react-query';
import { patternAPI, graphAPI } from '@/lib/api';
import { Pattern, PatternInstance } from '@/lib/types';
import { Activity, Clock, AlertCircle, TrendingUp, CheckCircle } from 'lucide-react';
import { useState } from 'react';

interface PatternCardProps {
  pattern: Pattern;
  onClick: () => void;
}

function PatternCard({ pattern, onClick }: PatternCardProps) {
  return (
    <div 
      onClick={onClick}
      className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow cursor-pointer border border-slate-200"
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center">
          <div className="bg-blue-100 rounded-lg p-3 mr-3">
            <Activity className="w-6 h-6 text-blue-600" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-slate-900">{pattern.name}</h3>
            <span className="text-sm text-slate-500 capitalize">{pattern.pattern_type}</span>
          </div>
        </div>
      </div>
      
      <p className="text-slate-600 text-sm mb-4 line-clamp-2">{pattern.description}</p>
      
      <div className="flex items-center justify-between text-sm">
        <div className="flex items-center text-slate-500">
          <Clock className="w-4 h-4 mr-1" />
          <span>{pattern.typical_duration_years} years</span>
        </div>
        <button className="text-blue-600 hover:text-blue-700 font-medium">
          View Details →
        </button>
      </div>
    </div>
  );
}

interface PatternDetailProps {
  pattern: Pattern;
  onClose: () => void;
}

function PatternDetail({ pattern, onClose }: PatternDetailProps) {
  const { data: instances, isLoading } = useQuery({
    queryKey: ['pattern-instances', pattern.id],
    queryFn: async () => {
      const response = await patternAPI.getInstances(pattern.id);
      return response.data;
    },
  });

  const { data: evolution } = useQuery({
    queryKey: ['pattern-evolution', pattern.id],
    queryFn: async () => {
      const response = await graphAPI.getPatternEvolution(pattern.id);
      return response.data;
    },
  });

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-white border-b border-slate-200 p-6 flex justify-between items-start">
          <div>
            <h2 className="text-2xl font-bold text-slate-900">{pattern.name}</h2>
            <p className="text-slate-600 capitalize mt-1">{pattern.pattern_type} Pattern</p>
          </div>
          <button 
            onClick={onClose}
            className="text-slate-400 hover:text-slate-600 text-2xl"
          >
            ×
          </button>
        </div>
        
        <div className="p-6">
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-slate-900 mb-2">Description</h3>
            <p className="text-slate-600">{pattern.description}</p>
          </div>
          
          <div className="grid md:grid-cols-2 gap-6 mb-6">
            <div>
              <h3 className="text-lg font-semibold text-slate-900 mb-3 flex items-center">
                <AlertCircle className="w-5 h-5 mr-2 text-orange-500" />
                Preconditions
              </h3>
              <ul className="space-y-2">
                {pattern.preconditions?.map((precondition, idx) => (
                  <li key={idx} className="flex items-start">
                    <span className="text-orange-500 mr-2">•</span>
                    <span className="text-slate-600">{precondition}</span>
                  </li>
                )) || <li className="text-slate-500">No preconditions specified</li>}
              </ul>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-slate-900 mb-3 flex items-center">
                <TrendingUp className="w-5 h-5 mr-2 text-blue-500" />
                Key Indicators
              </h3>
              <ul className="space-y-2">
                {pattern.indicators?.map((indicator, idx) => (
                  <li key={idx} className="flex items-start">
                    <span className="text-blue-500 mr-2">•</span>
                    <span className="text-slate-600">{indicator}</span>
                  </li>
                )) || <li className="text-slate-500">No indicators specified</li>}
              </ul>
            </div>
          </div>
          
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-slate-900 mb-3 flex items-center">
              <CheckCircle className="w-5 h-5 mr-2 text-green-500" />
              Typical Outcomes
            </h3>
            <ul className="space-y-2">
              {pattern.outcomes?.map((outcome, idx) => (
                <li key={idx} className="flex items-start">
                  <span className="text-green-500 mr-2">•</span>
                  <span className="text-slate-600">{outcome}</span>
                </li>
              )) || <li className="text-slate-500">No outcomes specified</li>}
            </ul>
          </div>
          
          <div className="bg-slate-50 rounded-lg p-4 mb-6">
            <div className="flex items-center justify-between">
              <span className="text-slate-600">Typical Duration:</span>
              <span className="text-lg font-semibold text-slate-900">{pattern.typical_duration_years || 'N/A'} {pattern.typical_duration_years && 'years'}</span>
            </div>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold text-slate-900 mb-3">Historical Instances</h3>
            {isLoading ? (
              <p className="text-slate-500">Loading instances...</p>
            ) : instances && instances.length > 0 ? (
              <div className="space-y-3">
                {instances.map((instance: PatternInstance, idx: number) => (
                  <div key={idx} className="bg-slate-50 rounded-lg p-4 border border-slate-200">
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <h4 className="font-semibold text-slate-900">{instance.event_name}</h4>
                        <p className="text-sm text-slate-500">Year {instance.year}</p>
                      </div>
                      <div className="flex items-center">
                        <div className="bg-green-100 text-green-800 text-xs font-medium px-2.5 py-1 rounded">
                          {Math.round(instance.confidence * 100)}% confidence
                        </div>
                      </div>
                    </div>
                    <p className="text-sm text-slate-600">
                      Identified: {instance.identified_date ? new Date(instance.identified_date).toLocaleDateString() : 'Unknown'}
                    </p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-slate-500">No historical instances found.</p>
            )}
          </div>

          {evolution && evolution.event_chain && evolution.event_chain.length > 0 && (
            <div className="mt-6">
              <h3 className="text-lg font-semibold text-slate-900 mb-3">Pattern Evolution</h3>
              <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
                <p className="text-sm text-blue-800 mb-2">
                  This pattern has evolved through {evolution.event_chain.length} connected events
                </p>
                <div className="flex flex-wrap gap-2">
                  {evolution.event_chain.slice(0, 5).map((event: any, idx: number) => (
                    <span key={idx} className="bg-white text-blue-700 text-xs px-3 py-1 rounded-full border border-blue-300">
                      {event.name}
                    </span>
                  ))}
                  {evolution.event_chain.length > 5 && (
                    <span className="text-blue-600 text-xs px-3 py-1">
                      +{evolution.event_chain.length - 5} more
                    </span>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function PatternsPage() {
  const [selectedPattern, setSelectedPattern] = useState<Pattern | null>(null);
  
  const { data: patterns, isLoading, error } = useQuery({
    queryKey: ['patterns'],
    queryFn: async () => {
      const response = await patternAPI.getPatterns();
      return response.data;
    },
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-slate-600">Loading patterns...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center text-red-600">
          <p>Error loading patterns. Please ensure the backend is running.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900 mb-2">Pattern Analysis</h1>
        <p className="text-slate-600">
          Recurring civilizational patterns identified throughout history. 
          {patterns && ` Currently tracking ${patterns.length} pattern templates.`}
        </p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {patterns && patterns.map((pattern: Pattern) => (
          <PatternCard 
            key={pattern.id} 
            pattern={pattern}
            onClick={() => setSelectedPattern(pattern)}
          />
        ))}
      </div>

      {selectedPattern && (
        <PatternDetail 
          pattern={selectedPattern}
          onClose={() => setSelectedPattern(null)}
        />
      )}
    </div>
  );
}
