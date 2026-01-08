'use client';

import { useQuery } from '@tanstack/react-query';
import { prophecyAPI, graphAPI } from '@/lib/api';
import { Prophecy, ProphecyFulfillment } from '@/lib/types';
import { BookOpen, Calendar, User, Globe, CheckCircle, Clock, Network } from 'lucide-react';
import { useState } from 'react';

interface ProphecyCardProps {
  prophecy: Prophecy;
  onClick: () => void;
}

function ProphecyCard({ prophecy, onClick }: ProphecyCardProps) {
  return (
    <div 
      onClick={onClick}
      className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow cursor-pointer border border-slate-200"
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center">
          <div className="bg-purple-100 rounded-lg p-3 mr-3">
            <BookOpen className="w-6 h-6 text-purple-600" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-slate-900">{prophecy.reference}</h3>
            <span className="text-sm text-slate-500 capitalize">{prophecy.prophecy_type}</span>
          </div>
        </div>
      </div>
      
      <p className="text-slate-600 text-sm mb-4 line-clamp-3 italic">"{prophecy.text}"</p>
      
      <div className="flex flex-wrap gap-2 mb-4">
        {prophecy.keywords && prophecy.keywords.length > 0 ? (
          <>
            {prophecy.keywords.slice(0, 3).map((keyword, idx) => (
              <span key={idx} className="bg-slate-100 text-slate-700 text-xs px-2 py-1 rounded">
                {keyword}
              </span>
            ))}
            {prophecy.keywords.length > 3 && (
              <span className="text-slate-500 text-xs px-2 py-1">
                +{prophecy.keywords.length - 3} more
              </span>
            )}
          </>
        ) : (
          <span className="text-slate-500 text-xs">No keywords</span>
        )}
      </div>
      
      <div className="flex items-center justify-between text-sm">
        <div className="flex items-center text-slate-500">
          <User className="w-4 h-4 mr-1" />
          <span>{prophecy.prophet}</span>
        </div>
        <button className="text-purple-600 hover:text-purple-700 font-medium">
          View Details →
        </button>
      </div>
    </div>
  );
}

interface ProphecyDetailProps {
  prophecy: Prophecy;
  onClose: () => void;
}

function ProphecyDetail({ prophecy, onClose }: ProphecyDetailProps) {
  const { data: fulfillments, isLoading } = useQuery({
    queryKey: ['prophecy-fulfillments', prophecy.id],
    queryFn: async () => {
      const response = await prophecyAPI.getFulfillments(prophecy.id);
      return response.data;
    },
  });

  const { data: network } = useQuery({
    queryKey: ['prophecy-network', prophecy.id],
    queryFn: async () => {
      const response = await graphAPI.getProphecyNetworks();
      return response.data?.filter((n: any) => 
        n.prophecy1.id === prophecy.id || n.prophecy2?.id === prophecy.id
      ) || [];
    },
  });

  const getFulfillmentColor = (type: string) => {
    switch (type) {
      case 'complete': return 'bg-green-100 text-green-800';
      case 'partial': return 'bg-yellow-100 text-yellow-800';
      case 'pending': return 'bg-orange-100 text-orange-800';
      default: return 'bg-slate-100 text-slate-800';
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-white border-b border-slate-200 p-6 flex justify-between items-start">
          <div>
            <h2 className="text-2xl font-bold text-slate-900">{prophecy.reference}</h2>
            <div className="flex items-center gap-4 mt-2 text-sm text-slate-600">
              <span className="flex items-center">
                <User className="w-4 h-4 mr-1" />
                {prophecy.prophet}
              </span>
              <span className="flex items-center">
                <Calendar className="w-4 h-4 mr-1" />
                Year {prophecy.year_declared}
              </span>
              <span className="flex items-center">
                <Globe className="w-4 h-4 mr-1" />
                {prophecy.scope}
              </span>
            </div>
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
            <h3 className="text-lg font-semibold text-slate-900 mb-2">Prophecy Text</h3>
            <div className="bg-purple-50 border-l-4 border-purple-500 p-4 rounded">
              <p className="text-slate-700 italic">"{prophecy.text}"</p>
            </div>
          </div>
          
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-slate-900 mb-3">Classification</h3>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="bg-slate-50 rounded-lg p-4">
                <span className="text-slate-600 text-sm">Type:</span>
                <p className="font-semibold text-slate-900 capitalize">{prophecy.prophecy_type}</p>
              </div>
              <div className="bg-slate-50 rounded-lg p-4">
                <span className="text-slate-600 text-sm">Scope:</span>
                <p className="font-semibold text-slate-900 capitalize">{prophecy.scope}</p>
              </div>
            </div>
          </div>
          
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-slate-900 mb-3">Keywords</h3>
            <div className="flex flex-wrap gap-2">
              {prophecy.keywords && prophecy.keywords.length > 0 ? (
                prophecy.keywords.map((keyword, idx) => (
                  <span key={idx} className="bg-purple-100 text-purple-700 px-3 py-1 rounded-full text-sm">
                    {keyword}
                  </span>
                ))
              ) : (
                <span className="text-slate-500">No keywords specified</span>
              )}
            </div>
          </div>
          
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-slate-900 mb-3">Prophetic Elements</h3>
            <div className="grid md:grid-cols-2 gap-3">
              {prophecy.elements && prophecy.elements.length > 0 ? (
                prophecy.elements.map((element, idx) => (
                  <div key={idx} className="bg-slate-50 rounded-lg p-3 border border-slate-200">
                    <p className="text-slate-700">{element.text}</p>
                  </div>
                ))
              ) : (
                <p className="text-slate-500 col-span-2">No prophetic elements specified</p>
              )}
            </div>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold text-slate-900 mb-3 flex items-center">
              <CheckCircle className="w-5 h-5 mr-2 text-green-500" />
              Fulfillment Record
            </h3>
            {isLoading ? (
              <p className="text-slate-500">Loading fulfillments...</p>
            ) : fulfillments && fulfillments.length > 0 ? (
              <div className="space-y-3">
                {fulfillments.map((fulfillment: ProphecyFulfillment) => (
                  <div key={fulfillment.id} className="bg-white rounded-lg p-4 border border-slate-200 shadow-sm">
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <h4 className="font-semibold text-slate-900">{fulfillment.event_name}</h4>
                        <p className="text-sm text-slate-500">Year {fulfillment.event_year}</p>
                      </div>
                      <div className="flex flex-col items-end gap-2">
                        <span className={`text-xs font-medium px-2.5 py-1 rounded capitalize ${getFulfillmentColor(fulfillment.fulfillment_type)}`}>
                          {fulfillment.fulfillment_type}
                        </span>
                        <span className="text-xs bg-blue-100 text-blue-800 px-2.5 py-1 rounded">
                          {Math.round(fulfillment.confidence * 100)}% confidence
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="bg-slate-50 rounded-lg p-6 text-center">
                <Clock className="w-12 h-12 text-slate-400 mx-auto mb-2" />
                <p className="text-slate-600">No fulfillments recorded yet</p>
                <p className="text-slate-500 text-sm mt-1">This prophecy may be pending fulfillment</p>
              </div>
            )}
          </div>

          {network && network.length > 0 && (
            <div className="mt-6">
              <h3 className="text-lg font-semibold text-slate-900 mb-3 flex items-center">
                <Network className="w-5 h-5 mr-2 text-blue-500" />
                Connected Prophecies
              </h3>
              <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
                <p className="text-sm text-blue-800 mb-2">
                  This prophecy is connected to {network.length} other prophecies through shared events
                </p>
                <div className="space-y-2">
                  {network.slice(0, 3).map((connection: any, idx: number) => (
                    <div key={idx} className="bg-white rounded p-2 text-sm">
                      <span className="text-blue-700 font-medium">
                        {connection.prophecy2?.reference || connection.prophecy1.reference}
                      </span>
                      <span className="text-slate-600"> via </span>
                      <span className="text-slate-700">{connection.shared_event?.name}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function PropheciesPage() {
  const [selectedProphecy, setSelectedProphecy] = useState<Prophecy | null>(null);
  
  const { data: prophecies, isLoading, error } = useQuery({
    queryKey: ['prophecies'],
    queryFn: async () => {
      const response = await prophecyAPI.getProphecies();
      return response.data;
    },
  });

  const { data: timeline } = useQuery({
    queryKey: ['prophecy-timeline'],
    queryFn: async () => {
      const response = await prophecyAPI.getTimeline();
      return response.data;
    },
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto mb-4"></div>
          <p className="text-slate-600">Loading prophecies...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center text-red-600">
          <p>Error loading prophecies. Please ensure the backend is running.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900 mb-2">Prophecy Fulfillment Tracker</h1>
        <p className="text-slate-600">
          Biblical prophecies and their historical fulfillments. 
          {prophecies && ` Tracking ${prophecies.length} prophecies across history.`}
        </p>
      </div>

      {timeline && (
        <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg p-6 mb-8 border border-purple-200">
          <h2 className="text-xl font-semibold text-slate-900 mb-4">Timeline Summary</h2>
          <div className="grid md:grid-cols-3 gap-4">
            <div className="bg-white rounded-lg p-4">
              <p className="text-slate-600 text-sm">Total Prophecies</p>
              <p className="text-2xl font-bold text-purple-600">{timeline.total_prophecies}</p>
            </div>
            <div className="bg-white rounded-lg p-4">
              <p className="text-slate-600 text-sm">Total Fulfillments</p>
              <p className="text-2xl font-bold text-green-600">{timeline.total_fulfillments}</p>
            </div>
            <div className="bg-white rounded-lg p-4">
              <p className="text-slate-600 text-sm">Time Span</p>
              <p className="text-2xl font-bold text-blue-600">{timeline.time_span_years} years</p>
            </div>
          </div>
        </div>
      )}

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {prophecies && prophecies.map((prophecy: Prophecy) => (
          <ProphecyCard 
            key={prophecy.id} 
            prophecy={prophecy}
            onClick={() => setSelectedProphecy(prophecy)}
          />
        ))}
      </div>

      {selectedProphecy && (
        <ProphecyDetail 
          prophecy={selectedProphecy}
          onClose={() => setSelectedProphecy(null)}
        />
      )}
    </div>
  );
}
