'use client';

import { ChronologyEvent } from '@/lib/types';
import { Calendar, MapPin, Users, BookOpen, Clock, Tag } from 'lucide-react';

interface EventCardProps {
  event: ChronologyEvent;
  onClick?: () => void;
  detailed?: boolean;
}

export default function EventCard({ event, onClick, detailed = false }: EventCardProps) {
  const yearDisplay = event.year_end 
    ? `${Math.abs(event.year_start)} ${event.year_start < 0 ? 'BC' : 'AD'} - ${Math.abs(event.year_end)} ${event.year_end < 0 ? 'BC' : 'AD'}`
    : `${Math.abs(event.year_start)} ${event.year_start < 0 ? 'BC' : 'AD'}`;

  const getEraColor = (era: string) => {
    const colors: Record<string, string> = {
      'creation_to_flood': 'bg-purple-100 text-purple-800 border-purple-200',
      'flood_to_abraham': 'bg-blue-100 text-blue-800 border-blue-200',
      'patriarchs': 'bg-indigo-100 text-indigo-800 border-indigo-200',
      'egyptian_bondage': 'bg-amber-100 text-amber-800 border-amber-200',
      'exodus_to_judges': 'bg-green-100 text-green-800 border-green-200',
      'united_monarchy': 'bg-yellow-100 text-yellow-800 border-yellow-200',
      'divided_kingdom': 'bg-orange-100 text-orange-800 border-orange-200',
      'exile': 'bg-red-100 text-red-800 border-red-200',
      'post_exile': 'bg-teal-100 text-teal-800 border-teal-200',
      'intertestamental': 'bg-cyan-100 text-cyan-800 border-cyan-200',
      'new_testament': 'bg-rose-100 text-rose-800 border-rose-200',
    };
    return colors[era] || 'bg-gray-100 text-gray-800 border-gray-200';
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'religious': return <BookOpen className="w-4 h-4" />;
      case 'military': return <Tag className="w-4 h-4" />;
      case 'political': return <Users className="w-4 h-4" />;
      case 'social': return <Users className="w-4 h-4" />;
      default: return <Calendar className="w-4 h-4" />;
    }
  };

  const keyActors = event.extra_data?.key_actors || [];
  const sourceRefs = event.extra_data?.source_references || [];

  return (
    <div 
      className={`bg-white rounded-lg shadow-md hover:shadow-xl transition-all duration-300 border border-slate-200 ${onClick ? 'cursor-pointer' : ''}`}
      onClick={onClick}
    >
      <div className="p-6">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <h3 className="text-xl font-bold text-slate-900 mb-2">{event.name}</h3>
            <div className="flex items-center gap-2 text-slate-600">
              <Calendar className="w-4 h-4" />
              <span className="font-semibold">{yearDisplay}</span>
            </div>
          </div>
          <div className={`px-3 py-1 rounded-full text-sm font-medium border ${getEraColor(event.era)}`}>
            {event.era.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
          </div>
        </div>

        {/* Description */}
        <p className="text-slate-700 mb-4 leading-relaxed">
          {detailed ? event.description : event.description?.substring(0, 200) + '...'}
        </p>

        {/* Metadata Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          {/* Biblical Source */}
          {event.biblical_source && (
            <div className="flex items-start gap-2">
              <BookOpen className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
              <div>
                <div className="text-xs font-semibold text-slate-500 uppercase">Biblical Reference</div>
                <div className="text-sm text-slate-700">{event.biblical_source}</div>
              </div>
            </div>
          )}

          {/* Event Type */}
          <div className="flex items-start gap-2">
            <div className="text-slate-700 mt-0.5">{getTypeIcon(event.event_type)}</div>
            <div>
              <div className="text-xs font-semibold text-slate-500 uppercase">Event Type</div>
              <div className="text-sm text-slate-700 capitalize">{event.event_type}</div>
            </div>
          </div>

          {/* Key Actors */}
          {keyActors.length > 0 && (
            <div className="flex items-start gap-2">
              <Users className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
              <div>
                <div className="text-xs font-semibold text-slate-500 uppercase">Key Actors</div>
                <div className="text-sm text-slate-700">{keyActors.slice(0, 3).join(', ')}</div>
              </div>
            </div>
          )}

          {/* Uncertainty */}
          {(event.year_start_min || event.year_start_max) && (
            <div className="flex items-start gap-2">
              <Clock className="w-5 h-5 text-orange-600 flex-shrink-0 mt-0.5" />
              <div>
                <div className="text-xs font-semibold text-slate-500 uppercase">Date Range</div>
                <div className="text-sm text-slate-700">
                  {event.year_start_min && `${Math.abs(event.year_start_min)} ${event.year_start_min < 0 ? 'BC' : 'AD'}`}
                  {event.year_start_min && event.year_start_max && ' - '}
                  {event.year_start_max && `${Math.abs(event.year_start_max)} ${event.year_start_max < 0 ? 'BC' : 'AD'}`}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Source References */}
        {detailed && sourceRefs.length > 0 && (
          <div className="border-t border-slate-200 pt-4 mt-4">
            <div className="text-xs font-semibold text-slate-500 uppercase mb-2">Historical Sources</div>
            <div className="space-y-1">
              {sourceRefs.map((ref: string, idx: number) => (
                <div key={idx} className="text-sm text-slate-600 italic">• {ref}</div>
              ))}
            </div>
          </div>
        )}

        {/* Extra Data Keys */}
        {detailed && event.extra_data && (
          <div className="border-t border-slate-200 pt-4 mt-4">
            <div className="text-xs font-semibold text-slate-500 uppercase mb-2">Additional Information</div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              {Object.entries(event.extra_data).map(([key, value]) => {
                if (key === 'key_actors' || key === 'source_references') return null;
                return (
                  <div key={key} className="text-sm">
                    <span className="font-medium text-slate-700 capitalize">{key.replace(/_/g, ' ')}: </span>
                    <span className="text-slate-600">{String(value)}</span>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
