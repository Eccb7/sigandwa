'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Search, X, Calendar, Activity, BookOpen, ExternalLink } from 'lucide-react';
import { chronologyAPI, patternAPI, prophecyAPI } from '@/lib/api';
import { multiFieldSearch } from '@/lib/utils';
import Link from 'next/link';

export default function GlobalSearch() {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState('');

  const { data: events } = useQuery({
    queryKey: ['all-events'],
    queryFn: async () => {
      const response = await chronologyAPI.getEvents();
      return response.data;
    },
    enabled: isOpen,
  });

  const { data: patterns } = useQuery({
    queryKey: ['all-patterns'],
    queryFn: async () => {
      const response = await patternAPI.getPatterns();
      return response.data;
    },
    enabled: isOpen,
  });

  const { data: prophecies } = useQuery({
    queryKey: ['all-prophecies'],
    queryFn: async () => {
      const response = await prophecyAPI.getProphecies();
      return response.data;
    },
    enabled: isOpen,
  });

  // Search across all data
  const searchResults = {
    events: events?.filter((e: any) => 
      multiFieldSearch(query, e, ['name', 'description', 'key_actors', 'era', 'event_type'])
    ).slice(0, 5) || [],
    patterns: patterns?.filter((p: any) => 
      multiFieldSearch(query, p, ['name', 'description', 'pattern_type'])
    ).slice(0, 5) || [],
    prophecies: prophecies?.filter((p: any) => 
      multiFieldSearch(query, p, ['reference', 'text', 'category'])
    ).slice(0, 5) || [],
  };

  const totalResults = searchResults.events.length + 
                       searchResults.patterns.length + 
                       searchResults.prophecies.length;

  return (
    <>
      {/* Search Button */}
      <button
        onClick={() => setIsOpen(true)}
        className="flex items-center gap-2 px-4 py-2 bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors text-slate-700"
      >
        <Search className="w-4 h-4" />
        <span className="text-sm font-medium">Search...</span>
        <kbd className="hidden sm:inline-flex px-2 py-1 text-xs font-semibold text-slate-500 bg-white border border-slate-300 rounded">
          ⌘K
        </kbd>
      </button>

      {/* Search Modal */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-start justify-center pt-20 px-4"
          onClick={() => setIsOpen(false)}
        >
          <div 
            className="bg-white rounded-xl shadow-2xl max-w-3xl w-full max-h-[600px] flex flex-col"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Search Input */}
            <div className="p-4 border-b border-slate-200">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 w-5 h-5" />
                <input
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Search events, patterns, prophecies..."
                  className="w-full pl-10 pr-10 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-lg"
                  autoFocus
                />
                <button
                  onClick={() => setIsOpen(false)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-slate-400 hover:text-slate-600"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
            </div>

            {/* Results */}
            <div className="flex-1 overflow-y-auto p-4">
              {!query ? (
                <div className="text-center py-12">
                  <Search className="w-12 h-12 text-slate-300 mx-auto mb-4" />
                  <p className="text-slate-500">Type to search across all data</p>
                  <p className="text-sm text-slate-400 mt-2">
                    Events • Patterns • Prophecies
                  </p>
                </div>
              ) : totalResults === 0 ? (
                <div className="text-center py-12">
                  <p className="text-slate-500">No results found for "{query}"</p>
                </div>
              ) : (
                <div className="space-y-6">
                  {/* Events */}
                  {searchResults.events.length > 0 && (
                    <div>
                      <div className="flex items-center gap-2 mb-3">
                        <Calendar className="w-4 h-4 text-blue-500" />
                        <h3 className="font-semibold text-slate-900">Events ({searchResults.events.length})</h3>
                      </div>
                      <div className="space-y-2">
                        {searchResults.events.map((event: any) => (
                          <Link
                            key={event.id}
                            href="/timeline"
                            onClick={() => setIsOpen(false)}
                            className="block p-3 bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors"
                          >
                            <div className="flex items-start justify-between">
                              <div className="flex-1">
                                <h4 className="font-medium text-slate-900">{event.name}</h4>
                                <p className="text-sm text-slate-600 mt-1 line-clamp-2">
                                  {event.description}
                                </p>
                                <div className="flex gap-2 mt-2">
                                  <span className="text-xs px-2 py-1 bg-white rounded text-slate-600">
                                    {event.year_start}
                                  </span>
                                  <span className="text-xs px-2 py-1 bg-white rounded text-slate-600">
                                    {event.era}
                                  </span>
                                </div>
                              </div>
                              <ExternalLink className="w-4 h-4 text-blue-500 flex-shrink-0 ml-2" />
                            </div>
                          </Link>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Patterns */}
                  {searchResults.patterns.length > 0 && (
                    <div>
                      <div className="flex items-center gap-2 mb-3">
                        <Activity className="w-4 h-4 text-green-500" />
                        <h3 className="font-semibold text-slate-900">Patterns ({searchResults.patterns.length})</h3>
                      </div>
                      <div className="space-y-2">
                        {searchResults.patterns.map((pattern: any) => (
                          <Link
                            key={pattern.id}
                            href="/patterns"
                            onClick={() => setIsOpen(false)}
                            className="block p-3 bg-green-50 hover:bg-green-100 rounded-lg transition-colors"
                          >
                            <div className="flex items-start justify-between">
                              <div className="flex-1">
                                <h4 className="font-medium text-slate-900">{pattern.name}</h4>
                                <p className="text-sm text-slate-600 mt-1 line-clamp-2">
                                  {pattern.description}
                                </p>
                                <div className="flex gap-2 mt-2">
                                  <span className="text-xs px-2 py-1 bg-white rounded text-slate-600">
                                    {pattern.pattern_type}
                                  </span>
                                  <span className="text-xs px-2 py-1 bg-white rounded text-slate-600">
                                    {pattern.historical_instances?.length || 0} instances
                                  </span>
                                </div>
                              </div>
                              <ExternalLink className="w-4 h-4 text-green-500 flex-shrink-0 ml-2" />
                            </div>
                          </Link>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Prophecies */}
                  {searchResults.prophecies.length > 0 && (
                    <div>
                      <div className="flex items-center gap-2 mb-3">
                        <BookOpen className="w-4 h-4 text-purple-500" />
                        <h3 className="font-semibold text-slate-900">Prophecies ({searchResults.prophecies.length})</h3>
                      </div>
                      <div className="space-y-2">
                        {searchResults.prophecies.map((prophecy: any) => (
                          <Link
                            key={prophecy.id}
                            href="/prophecies"
                            onClick={() => setIsOpen(false)}
                            className="block p-3 bg-purple-50 hover:bg-purple-100 rounded-lg transition-colors"
                          >
                            <div className="flex items-start justify-between">
                              <div className="flex-1">
                                <h4 className="font-medium text-slate-900">{prophecy.reference}</h4>
                                <p className="text-sm text-slate-600 mt-1 line-clamp-2">
                                  {prophecy.text}
                                </p>
                                <div className="flex gap-2 mt-2">
                                  <span className="text-xs px-2 py-1 bg-white rounded text-slate-600">
                                    {prophecy.category}
                                  </span>
                                  <span className="text-xs px-2 py-1 bg-white rounded text-slate-600">
                                    {prophecy.fulfillment_type}
                                  </span>
                                </div>
                              </div>
                              <ExternalLink className="w-4 h-4 text-purple-500 flex-shrink-0 ml-2" />
                            </div>
                          </Link>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Footer */}
            <div className="p-4 border-t border-slate-200 bg-slate-50">
              <div className="flex items-center justify-between text-xs text-slate-500">
                <span>
                  {totalResults > 0 && `${totalResults} results found`}
                </span>
                <div className="flex gap-2">
                  <kbd className="px-2 py-1 bg-white border border-slate-300 rounded">↑↓</kbd>
                  <span>Navigate</span>
                  <kbd className="px-2 py-1 bg-white border border-slate-300 rounded">Enter</kbd>
                  <span>Select</span>
                  <kbd className="px-2 py-1 bg-white border border-slate-300 rounded">Esc</kbd>
                  <span>Close</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
