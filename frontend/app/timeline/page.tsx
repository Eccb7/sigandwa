'use client';

import { useQuery } from '@tanstack/react-query';
import { chronologyAPI } from '@/lib/api';
import type { ChronologyEvent } from '@/lib/types';
import { Calendar, ChevronRight } from 'lucide-react';

function TimelineEvent({ event }: { event: ChronologyEvent }) {
  const yearDisplay = event.year_end 
    ? `${event.year_start} to ${event.year_end}`
    : event.year_start;

  return (
    <div className="relative pb-8">
      <span className="absolute top-5 left-5 -ml-px h-full w-0.5 bg-slate-200" aria-hidden="true" />
      <div className="relative flex items-start space-x-3">
        <div>
          <div className="relative px-1">
            <div className="h-8 w-8 bg-blue-500 rounded-full ring-8 ring-white flex items-center justify-center">
              <Calendar className="h-5 w-5 text-white" />
            </div>
          </div>
        </div>
        <div className="min-w-0 flex-1 py-0">
          <div className="text-md text-slate-500">
            <span className="font-medium text-slate-900">{event.name}</span>
            {' • '}
            <span className="whitespace-nowrap">{yearDisplay}</span>
          </div>
          <div className="mt-2 text-sm text-slate-700">
            <p>{event.description}</p>
          </div>
          <div className="mt-2 flex items-center space-x-2">
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-100 text-slate-800">
              {event.era}
            </span>
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
              {event.event_type}
            </span>
            {event.is_pivotal && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                Pivotal
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default function TimelinePage() {
  const { data: events, isLoading, error } = useQuery({
    queryKey: ['timeline-events'],
    queryFn: async () => {
      const response = await chronologyAPI.getEvents();
      return response.data as ChronologyEvent[];
    },
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-slate-900"></div>
          <p className="mt-2 text-sm text-slate-600">Loading timeline...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <p className="text-red-800">Error loading timeline data. Please ensure the backend is running.</p>
      </div>
    );
  }

  // Sort events by year (oldest first)
  const sortedEvents = events?.sort((a, b) => a.year_start - b.year_start) || [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="border-b border-slate-200 pb-5">
        <h1 className="text-3xl font-bold leading-tight text-slate-900">
          Historical Timeline
        </h1>
        <p className="mt-2 text-sm text-slate-600">
          Complete chronology from Creation ({sortedEvents[0]?.year_start}) to Present ({sortedEvents[sortedEvents.length - 1]?.year_start})
        </p>
      </div>

      {/* Stats */}
      <div className="bg-white shadow rounded-lg p-6">
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-3">
          <div>
            <dt className="text-sm font-medium text-slate-500">Total Events</dt>
            <dd className="mt-1 text-3xl font-semibold text-slate-900">{sortedEvents.length}</dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-slate-500">Time Span</dt>
            <dd className="mt-1 text-3xl font-semibold text-slate-900">
              {Math.abs(sortedEvents[0]?.year_start || 0) + (sortedEvents[sortedEvents.length - 1]?.year_start || 0)} years
            </dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-slate-500">Pivotal Events</dt>
            <dd className="mt-1 text-3xl font-semibold text-slate-900">
              {sortedEvents.filter(e => e.is_pivotal).length}
            </dd>
          </div>
        </div>
      </div>

      {/* Timeline */}
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-lg font-medium text-slate-900 mb-6">
          Chronological Events
        </h2>
        <div className="flow-root">
          <ul className="-mb-8">
            {sortedEvents.map((event, idx) => (
              <li key={event.id}>
                <TimelineEvent event={event} />
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
