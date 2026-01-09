'use client';

import { useQuery } from '@tanstack/react-query';
import { prophecyAPI, graphAPI } from '@/lib/api';
import { Prophecy, ProphecyFulfillment } from '@/lib/types';
import { BookOpen, Calendar, User, Globe, CheckCircle, Clock, Network, BookOpenText, Scroll } from 'lucide-react';
import { useState } from 'react';
import ProphecyTimeline from '@/components/ProphecyTimeline';
import DanielBeasts from '@/components/DanielBeasts';

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
  const [activeTab, setActiveTab] = useState<'overview' | 'timeline' | 'beasts' | 'database'>('overview');
  
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
          <p className="text-slate-600">Loading Biblical prophecy interpretation...</p>
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
      {/* Hero Header */}
      <div className="bg-gradient-to-r from-purple-600 via-blue-600 to-indigo-600 text-white rounded-lg shadow-lg p-8 mb-8">
        <div className="flex items-center mb-4">
          <Scroll className="w-12 h-12 mr-4" />
          <div>
            <h1 className="text-4xl font-bold mb-2">Biblical Prophecy: The Historicist Interpretation</h1>
            <p className="text-lg text-purple-100">
              The Definitive Guide to Understanding Fulfilled and Future Prophecy
            </p>
          </div>
        </div>
        <div className="bg-white bg-opacity-10 rounded-lg p-4 mt-4">
          <p className="text-sm text-purple-100 leading-relaxed">
            <strong>Based on:</strong> Gems from Daniel by Robert J. Wieland & Donald K. Short, and Gems from Revelation - 
            The historicist school of prophetic interpretation used by the Protestant Reformers, recognizing fulfilled prophecies 
            throughout history from Daniel's time to the present day.
          </p>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="mb-8">
        <div className="border-b border-slate-200">
          <nav className="flex gap-6">
            <button
              onClick={() => setActiveTab('overview')}
              className={`pb-4 px-2 font-semibold text-sm transition-colors border-b-2 ${
                activeTab === 'overview'
                  ? 'border-purple-600 text-purple-600'
                  : 'border-transparent text-slate-600 hover:text-slate-900'
              }`}
            >
              <div className="flex items-center gap-2">
                <BookOpenText className="w-5 h-5" />
                <span>Overview & Principles</span>
              </div>
            </button>
            <button
              onClick={() => setActiveTab('timeline')}
              className={`pb-4 px-2 font-semibold text-sm transition-colors border-b-2 ${
                activeTab === 'timeline'
                  ? 'border-purple-600 text-purple-600'
                  : 'border-transparent text-slate-600 hover:text-slate-900'
              }`}
            >
              <div className="flex items-center gap-2">
                <Clock className="w-5 h-5" />
                <span>Prophetic Timeline</span>
              </div>
            </button>
            <button
              onClick={() => setActiveTab('beasts')}
              className={`pb-4 px-2 font-semibold text-sm transition-colors border-b-2 ${
                activeTab === 'beasts'
                  ? 'border-purple-600 text-purple-600'
                  : 'border-transparent text-slate-600 hover:text-slate-900'
              }`}
            >
              <div className="flex items-center gap-2">
                <Globe className="w-5 h-5" />
                <span>Daniel's Kingdoms</span>
              </div>
            </button>
            <button
              onClick={() => setActiveTab('database')}
              className={`pb-4 px-2 font-semibold text-sm transition-colors border-b-2 ${
                activeTab === 'database'
                  ? 'border-purple-600 text-purple-600'
                  : 'border-transparent text-slate-600 hover:text-slate-900'
              }`}
            >
              <div className="flex items-center gap-2">
                <BookOpen className="w-5 h-5" />
                <span>Prophecy Database</span>
              </div>
            </button>
          </nav>
        </div>
      </div>

      {/* Tab Content */}
      {activeTab === 'overview' && (
        <div className="space-y-8">
          {/* Introduction */}
          <div className="bg-white rounded-lg shadow-md p-8">
            <h2 className="text-2xl font-bold text-slate-900 mb-4">The Historicist Method of Prophetic Interpretation</h2>
            <div className="prose max-w-none text-slate-700 space-y-4">
              <p className="text-lg leading-relaxed">
                The historicist approach to Bible prophecy sees prophetic fulfillment as a <strong>continuous historical process</strong>, 
                spanning from the prophet's time through the present and into the future. This method was championed by the 
                Protestant Reformers including Martin Luther, John Calvin, and later by William Miller and the Advent movement.
              </p>
              
              <div className="bg-blue-50 border-l-4 border-blue-500 p-6 my-6">
                <h3 className="text-lg font-bold text-blue-900 mb-2">Core Principles</h3>
                <ul className="space-y-2 text-slate-700">
                  <li className="flex items-start">
                    <span className="text-blue-500 mr-2 mt-1">1.</span>
                    <span><strong>Year-Day Principle:</strong> One prophetic day equals one literal year (Numbers 14:34, Ezekiel 4:6)</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-blue-500 mr-2 mt-1">2.</span>
                    <span><strong>Continuous Fulfillment:</strong> Prophecies unfold throughout history, not just at the end times</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-blue-500 mr-2 mt-1">3.</span>
                    <span><strong>Symbolic Interpretation:</strong> Beasts represent kingdoms, horns represent powers, women represent churches</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-blue-500 mr-2 mt-1">4.</span>
                    <span><strong>Historical Validation:</strong> Fulfilled prophecies confirm the divine inspiration of Scripture</span>
                  </li>
                </ul>
              </div>

              <h3 className="text-xl font-bold text-slate-900 mt-8 mb-3">Key Prophetic Periods</h3>
              <div className="grid md:grid-cols-2 gap-6">
                <div className="bg-red-50 border border-red-200 rounded-lg p-5">
                  <h4 className="font-bold text-red-900 mb-2">1260 Days/Years</h4>
                  <p className="text-sm text-slate-700 mb-3">
                    Mentioned <strong>seven times</strong> in Daniel and Revelation (Daniel 7:25, 12:7; Revelation 11:2-3, 12:6, 12:14, 13:5).
                    Historicists identify this as 538-1798 AD - the period of papal supremacy from the fall of the Ostrogoths to 
                    the capture of Pope Pius VI by French General Berthier.
                  </p>
                  <div className="bg-white rounded p-3 text-xs">
                    <strong>Biblical forms:</strong> "time, times, and half a time" (3.5 years), "forty-two months", "1260 days"
                  </div>
                </div>

                <div className="bg-blue-50 border border-blue-200 rounded-lg p-5">
                  <h4 className="font-bold text-blue-900 mb-2">2300 Days/Years</h4>
                  <p className="text-sm text-slate-700 mb-3">
                    From Daniel 8:14: "Unto two thousand and three hundred days; then shall the sanctuary be cleansed."
                    Starting from the decree to rebuild Jerusalem (457 BC), this period extends to 1844 AD, marking the 
                    beginning of the investigative judgment in heaven's sanctuary.
                  </p>
                  <div className="bg-white rounded p-3 text-xs">
                    <strong>William Miller:</strong> Sparked the Second Advent Movement by calculating this timeline
                  </div>
                </div>

                <div className="bg-purple-50 border border-purple-200 rounded-lg p-5">
                  <h4 className="font-bold text-purple-900 mb-2">Seventy Weeks (490 Years)</h4>
                  <p className="text-sm text-slate-700 mb-3">
                    Daniel 9:24-27 prophesies 70 weeks (490 years) determined for Israel. The 69 weeks (483 years) 
                    reach to Messiah the Prince. Jesus began His ministry in 27 AD and was crucified in 31 AD, 
                    exactly fulfilling this timeline.
                  </p>
                  <div className="bg-white rounded p-3 text-xs">
                    <strong>Fulfillment:</strong> 457 BC (decree) + 483 years = 27 AD (Jesus' baptism)
                  </div>
                </div>

                <div className="bg-green-50 border border-green-200 rounded-lg p-5">
                  <h4 className="font-bold text-green-900 mb-2">1290 & 1335 Days/Years</h4>
                  <p className="text-sm text-slate-700 mb-3">
                    Daniel 12:11-12 mentions two additional time periods. The 1290 days may extend from 508 AD 
                    (Clovis' conversion establishing papal infrastructure) to 1798 AD. The 1335 days reach approximately 
                    to 1843-1844, the time of great prophetic awakening.
                  </p>
                  <div className="bg-white rounded p-3 text-xs">
                    <strong>Note:</strong> "Blessed is he that waiteth, and cometh to the 1335 days" (Daniel 12:12)
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Timeline Summary if available */}
          {timeline && (
            <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg p-6 border border-purple-200">
              <h2 className="text-xl font-semibold text-slate-900 mb-4">System Prophecy Statistics</h2>
              <div className="grid md:grid-cols-3 gap-4">
                <div className="bg-white rounded-lg p-4 shadow">
                  <p className="text-slate-600 text-sm">Total Prophecies Tracked</p>
                  <p className="text-3xl font-bold text-purple-600">{timeline.total_prophecies}</p>
                </div>
                <div className="bg-white rounded-lg p-4 shadow">
                  <p className="text-slate-600 text-sm">Historical Fulfillments</p>
                  <p className="text-3xl font-bold text-green-600">{timeline.total_fulfillments}</p>
                </div>
                <div className="bg-white rounded-lg p-4 shadow">
                  <p className="text-slate-600 text-sm">Time Span Covered</p>
                  <p className="text-3xl font-bold text-blue-600">{timeline.time_span_years} years</p>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {activeTab === 'timeline' && <ProphecyTimeline />}
      
      {activeTab === 'beasts' && <DanielBeasts />}
      
      {activeTab === 'database' && (
        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-bold text-slate-900 mb-2">Prophecy Database</h2>
            <p className="text-slate-600 mb-6">
              Biblical prophecies tracked in the system with their historical fulfillments. 
              {prophecies && ` Currently tracking ${prophecies.length} prophecies.`}
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {prophecies && prophecies.map((prophecy: Prophecy) => (
              <ProphecyCard 
                key={prophecy.id} 
                prophecy={prophecy}
                onClick={() => setSelectedProphecy(prophecy)}
              />
            ))}
          </div>

          {(!prophecies || prophecies.length === 0) && (
            <div className="bg-slate-50 rounded-lg p-12 text-center">
              <BookOpen className="w-16 h-16 text-slate-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-slate-700 mb-2">No prophecies in database yet</h3>
              <p className="text-slate-500">
                Prophecy data will be imported from the prophecy library in the backend.
              </p>
            </div>
          )}
        </div>
      )}

      {selectedProphecy && (
        <ProphecyDetail 
          prophecy={selectedProphecy}
          onClose={() => setSelectedProphecy(null)}
        />
      )}
    </div>
  );
}
