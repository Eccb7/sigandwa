'use client';

import { useQuery } from '@tanstack/react-query';
import { 
  Calendar, 
  Activity, 
  BookOpen, 
  Clock,
  CheckCircle2,
  Search,
  Filter,
  ChevronDown,
  ChevronUp,
  Info
} from 'lucide-react';
import { chronologyAPI, patternAPI, prophecyAPI } from '@/lib/api';
import EventCard from '@/components/EventCard';
import { useState, useMemo } from 'react';
import type { ChronologyEvent } from '@/lib/types';

function StatCard({ 
  title, 
  value, 
  icon: Icon, 
  description
}: { 
  title: string; 
  value: string | number; 
  icon: any;
  description?: string;
}) {
  return (
    <div className="bg-white overflow-hidden shadow rounded-lg hover:shadow-lg transition-shadow">
      <div className="p-5">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <Icon className="h-6 w-6 text-blue-600" />
          </div>
          <div className="ml-5 w-0 flex-1">
            <dl>
              <dt className="text-sm font-medium text-slate-500 truncate">
                {title}
              </dt>
              <dd className="flex items-baseline">
                <div className="text-2xl font-semibold text-slate-900">
                  {value}
                </div>
              </dd>
              {description && (
                <dd className="mt-1 text-sm text-slate-600">
                  {description}
                </dd>
              )}
            </dl>
          </div>
        </div>
      </div>
    </div>
  );
}

interface EventModalProps {
  event: ChronologyEvent;
  onClose: () => void;
}

function EventModal({ event, onClose }: EventModalProps) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50" onClick={onClose}>
      <div className="bg-white rounded-lg shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
        <div className="sticky top-0 bg-white border-b border-slate-200 p-6 flex items-center justify-between">
          <h2 className="text-2xl font-bold text-slate-900">{event.name}</h2>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-600 transition-colors"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div className="p-6">
          <EventCard event={event} detailed />
        </div>
      </div>
    </div>
  );
}

export default function Dashboard() {
  const [selectedEra, setSelectedEra] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedEvent, setSelectedEvent] = useState<ChronologyEvent | null>(null);
  const [showStats, setShowStats] = useState(true);
  const [displayLimit, setDisplayLimit] = useState(20);

  const { data: events, isLoading: eventsLoading } = useQuery({
    queryKey: ['events'],
    queryFn: async () => {
      const response = await chronologyAPI.getEvents();
      return response.data as ChronologyEvent[];
    },
  });

  const { data: patterns } = useQuery({
    queryKey: ['patterns'],
    queryFn: async () => {
      const response = await patternAPI.getPatterns();
      return response.data;
    },
  });

  const { data: prophecies } = useQuery({
    queryKey: ['prophecies'],
    queryFn: async () => {
      const response = await prophecyAPI.getProphecies();
      return response.data;
    },
  });

  const filteredEvents = useMemo(() => {
    if (!events) return [];
    let filtered = events;
    if (selectedEra !== 'all') filtered = filtered.filter(e => e.era === selectedEra);
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(e => 
        e.name.toLowerCase().includes(query) ||
        e.description?.toLowerCase().includes(query) ||
        e.biblical_source?.toLowerCase().includes(query)
      );
    }
    return filtered.sort((a, b) => a.year_start - b.year_start);
  }, [events, selectedEra, searchQuery]);

  const eraStats = useMemo(() => {
    if (!events) return [];
    const stats: Record<string, any> = {};
    const eraDisplayNames: Record<string, string> = {
      'creation_to_flood': 'Creation to Flood',
      'flood_to_abraham': 'Flood to Abraham',
      'patriarchs': 'Patriarchs',
      'egyptian_bondage': 'Egyptian Bondage',
      'exodus_to_judges': 'Exodus to Judges',
      'united_monarchy': 'United Monarchy',
      'divided_kingdom': 'Divided Kingdom',
      'exile': 'Exile',
      'post_exile': 'Post-Exile'
    };
    events.forEach(event => {
      if (!stats[event.era]) {
        stats[event.era] = { count: 0, yearRange: '', era: event.era, displayName: eraDisplayNames[event.era] || event.era };
      }
      stats[event.era].count++;
    });
    Object.keys(stats).forEach(era => {
      const eraEvents = events.filter(e => e.era === era);
      if (eraEvents.length > 0) {
        const minYear = Math.min(...eraEvents.map(e => e.year_start));
        const maxYear = Math.max(...eraEvents.map(e => e.year_end || e.year_start));
        stats[era].yearRange = `${Math.abs(minYear)} ${minYear < 0 ? 'BC' : 'AD'} - ${Math.abs(maxYear)} ${maxYear < 0 ? 'BC' : 'AD'}`;
      }
    });
    return Object.values(stats);
  }, [events]);

  const displayedEvents = filteredEvents.slice(0, displayLimit);

  if (eventsLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p className="mt-2 text-sm text-slate-600">Loading Biblical chronology...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-blue-600 to-indigo-700 rounded-lg shadow-lg p-8 text-white">
        <h1 className="text-4xl font-bold mb-2">Biblical Cliodynamics Analysis System</h1>
        <p className="text-lg text-blue-100 mb-4">The Definitive Source of Historical Truth from a Biblical Perspective</p>
        <p className="text-sm text-blue-50">Based on James Ussher's <em>Annals of the World</em> and authoritative Biblical commentary</p>
      </div>

      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard title="Historical Events" value={events?.length || 0} icon={Calendar} description="From Creation (4004 BC) to Present" />
        <StatCard title="Biblical Eras" value={eraStats.length} icon={Clock} description="Major chronological divisions" />
        <StatCard title="Pattern Templates" value={patterns?.length || 0} icon={Activity} description="Recurring civilizational cycles" />
        <StatCard title="Prophecies Tracked" value={prophecies?.length || 0} icon={BookOpen} description="With fulfillment analysis" />
      </div>

      <div className="bg-white rounded-lg shadow">
        <button onClick={() => setShowStats(!showStats)} className="w-full px-6 py-4 flex items-center justify-between text-left hover:bg-slate-50 transition-colors">
          <div className="flex items-center gap-2">
            <Info className="w-5 h-5 text-blue-600" />
            <h2 className="text-lg font-semibold text-slate-900">Era Overview & Statistics</h2>
          </div>
          {showStats ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
        </button>
        {showStats && (
          <div className="px-6 pb-6 border-t border-slate-200">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-4">
              {eraStats.map((era: any) => (
                <div key={era.era} className={`p-4 rounded-lg border-2 transition-all cursor-pointer ${selectedEra === era.era ? 'border-blue-500 bg-blue-50' : 'border-slate-200 hover:border-blue-300'}`}
                  onClick={() => setSelectedEra(selectedEra === era.era ? 'all' : era.era)}>
                  <h3 className="font-semibold text-slate-900 mb-1">{era.displayName}</h3>
                  <p className="text-sm text-slate-600 mb-2">{era.yearRange}</p>
                  <div className="flex items-center justify-between">
                    <span className="text-2xl font-bold text-blue-600">{era.count}</span>
                    <span className="text-xs text-slate-500">events</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 w-5 h-5" />
              <input type="text" placeholder="Search events, actors, or Biblical references..." value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500" />
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Filter className="w-5 h-5 text-slate-400" />
            <span className="text-sm text-slate-600">
              {selectedEra !== 'all' ? `Filtered: ${eraStats.find((e: any) => e.era === selectedEra)?.displayName}` : 'All Eras'}
            </span>
            {selectedEra !== 'all' && (
              <button onClick={() => setSelectedEra('all')} className="text-sm text-blue-600 hover:text-blue-700 font-medium">Clear</button>
            )}
          </div>
        </div>
        <div className="mt-4 flex items-center justify-between">
          <p className="text-sm text-slate-600">Showing <span className="font-semibold">{displayedEvents.length}</span> of <span className="font-semibold">{filteredEvents.length}</span> events</p>
          {filteredEvents.length > displayLimit && (
            <button onClick={() => setDisplayLimit(prev => prev + 20)} className="text-sm text-blue-600 hover:text-blue-700 font-medium">Load More</button>
          )}
        </div>
      </div>

      <div className="space-y-4">
        <h2 className="text-2xl font-bold text-slate-900">Historical Events</h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {displayedEvents.map((event) => (
            <EventCard key={event.id} event={event} onClick={() => setSelectedEvent(event)} />
          ))}
        </div>
        {displayedEvents.length === 0 && (
          <div className="text-center py-12 bg-white rounded-lg shadow">
            <Calendar className="w-16 h-16 text-slate-300 mx-auto mb-4" />
            <p className="text-slate-600">No events found matching your criteria</p>
          </div>
        )}
      </div>

      {selectedEvent && <EventModal event={selectedEvent} onClose={() => setSelectedEvent(null)} />}

      <div className="bg-slate-50 rounded-lg p-6 border border-slate-200">
        <h3 className="text-sm font-semibold text-slate-700 mb-3 flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-green-500" />System Status</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-slate-600">
          <div>Database: <span className="font-medium text-green-600">Online</span></div>
          <div>Events: <span className="font-medium">{events?.length || 0}</span></div>
          <div>Chronology: <span className="font-medium">Ussher-based</span></div>
          <div>Version: <span className="font-medium">0.6.0</span></div>
        </div>
      </div>
    </div>
  );
}
