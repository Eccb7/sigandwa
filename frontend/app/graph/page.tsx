'use client';

import { useQuery } from '@tanstack/react-query';
import { graphAPI } from '@/lib/api';
import { Network, GitBranch, TrendingUp, Search, RefreshCw, Database } from 'lucide-react';
import { useState } from 'react';

interface StatCardProps {
  title: string;
  value: number;
  icon: React.ReactNode;
  color: string;
}

function StatCard({ title, value, icon, color }: StatCardProps) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 border border-slate-200">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-slate-600 text-sm mb-1">{title}</p>
          <p className="text-3xl font-bold text-slate-900">{value}</p>
        </div>
        <div className={`${color} rounded-lg p-3`}>
          {icon}
        </div>
      </div>
    </div>
  );
}

export default function GraphPage() {
  const [showSync, setShowSync] = useState(false);
  const [selectedChainLength, setSelectedChainLength] = useState(3);
  const [searchNodeId, setSearchNodeId] = useState('');
  const [searchResult, setSearchResult] = useState<any>(null);

  const { data: stats, isLoading, refetch } = useQuery({
    queryKey: ['graph-stats'],
    queryFn: async () => {
      const response = await graphAPI.getStats();
      return response.data;
    },
  });

  const { data: influentialEvents } = useQuery({
    queryKey: ['influential-events'],
    queryFn: async () => {
      const response = await graphAPI.getInfluentialEvents(10);
      return response.data;
    },
  });

  const { data: eventChains } = useQuery({
    queryKey: ['event-chains', selectedChainLength],
    queryFn: async () => {
      const response = await graphAPI.getEventChains(selectedChainLength);
      return response.data;
    },
  });

  const { data: prophecyNetworks } = useQuery({
    queryKey: ['prophecy-networks'],
    queryFn: async () => {
      const response = await graphAPI.getProphecyNetworks();
      return response.data;
    },
  });

  const handleSync = async () => {
    setShowSync(true);
    try {
      await graphAPI.sync();
      await refetch();
      setTimeout(() => setShowSync(false), 2000);
    } catch (error) {
      console.error('Sync failed:', error);
      setShowSync(false);
    }
  };

  const handleSearch = async () => {
    if (!searchNodeId.trim()) return;
    try {
      const response = await graphAPI.getShortestPath(searchNodeId, 'any');
      setSearchResult(response.data);
    } catch (error) {
      console.error('Search failed:', error);
      setSearchResult(null);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-slate-600">Loading graph data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8 flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 mb-2">Graph Network Analysis</h1>
          <p className="text-slate-600">
            Neo4j knowledge graph connecting events, patterns, and prophecies.
            {stats && ` ${stats.total_events + stats.total_patterns + stats.total_prophecies} nodes with ${stats.total_relationships} relationships.`}
          </p>
        </div>
        <button
          onClick={handleSync}
          disabled={showSync}
          className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
        >
          <RefreshCw className={`w-4 h-4 ${showSync ? 'animate-spin' : ''}`} />
          {showSync ? 'Syncing...' : 'Sync Graph'}
        </button>
      </div>

      {stats && (
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            title="Total Events"
            value={stats.total_events}
            icon={<Network className="w-6 h-6 text-blue-600" />}
            color="bg-blue-100"
          />
          <StatCard
            title="Total Patterns"
            value={stats.total_patterns}
            icon={<GitBranch className="w-6 h-6 text-green-600" />}
            color="bg-green-100"
          />
          <StatCard
            title="Total Prophecies"
            value={stats.total_prophecies}
            icon={<TrendingUp className="w-6 h-6 text-purple-600" />}
            color="bg-purple-100"
          />
          <StatCard
            title="Relationships"
            value={stats.total_relationships}
            icon={<Database className="w-6 h-6 text-orange-600" />}
            color="bg-orange-100"
          />
        </div>
      )}

      {stats && (
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-6 mb-8 border border-blue-200">
          <h2 className="text-xl font-semibold text-slate-900 mb-4">Network Statistics</h2>
          <div className="grid md:grid-cols-3 gap-4">
            <div className="bg-white rounded-lg p-4">
              <p className="text-slate-600 text-sm">Average Connections</p>
              <p className="text-2xl font-bold text-blue-600">{stats.avg_connections_per_event?.toFixed(2) || 0}</p>
              <p className="text-xs text-slate-500 mt-1">per event node</p>
            </div>
            <div className="bg-white rounded-lg p-4">
              <p className="text-slate-600 text-sm">Total Actors</p>
              <p className="text-2xl font-bold text-green-600">{stats.total_actors || 0}</p>
              <p className="text-xs text-slate-500 mt-1">historical figures</p>
            </div>
            <div className="bg-white rounded-lg p-4">
              <p className="text-slate-600 text-sm">Graph Density</p>
              <p className="text-2xl font-bold text-purple-600">
                {stats.total_relationships && stats.total_events 
                  ? ((stats.total_relationships / stats.total_events) * 100).toFixed(1)
                  : 0}%
              </p>
              <p className="text-xs text-slate-500 mt-1">connectivity ratio</p>
            </div>
          </div>
        </div>
      )}

      <div className="grid lg:grid-cols-2 gap-8 mb-8">
        <div className="bg-white rounded-lg shadow-md p-6 border border-slate-200">
          <h2 className="text-xl font-semibold text-slate-900 mb-4">Most Influential Events</h2>
          {influentialEvents && influentialEvents.length > 0 ? (
            <div className="space-y-3">
              {influentialEvents.map((event: any, idx: number) => (
                <div key={idx} className="bg-slate-50 rounded-lg p-4 border border-slate-200">
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <h3 className="font-semibold text-slate-900">{event.event_name}</h3>
                      <p className="text-sm text-slate-500">Year {event.year}</p>
                    </div>
                    <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-1 rounded">
                      {event.connection_count} connections
                    </span>
                  </div>
                  <div className="flex gap-4 text-xs text-slate-600">
                    <span>Patterns: {event.pattern_connections}</span>
                    <span>Prophecies: {event.prophecy_connections}</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-slate-500">No influential events found.</p>
          )}
        </div>

        <div className="bg-white rounded-lg shadow-md p-6 border border-slate-200">
          <h2 className="text-xl font-semibold text-slate-900 mb-4">Prophecy Networks</h2>
          {prophecyNetworks && prophecyNetworks.length > 0 ? (
            <div className="space-y-3">
              {prophecyNetworks.slice(0, 5).map((network: any, idx: number) => (
                <div key={idx} className="bg-purple-50 rounded-lg p-4 border border-purple-200">
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex-1">
                      <p className="text-sm font-semibold text-purple-900">
                        {network.prophecy1?.reference}
                      </p>
                      <p className="text-xs text-purple-600 mt-1">↓ connected via ↓</p>
                      <p className="text-sm font-medium text-slate-700 mt-1">
                        {network.shared_event?.name}
                      </p>
                      {network.prophecy2 && (
                        <>
                          <p className="text-xs text-purple-600 mt-1">↓ to ↓</p>
                          <p className="text-sm font-semibold text-purple-900 mt-1">
                            {network.prophecy2.reference}
                          </p>
                        </>
                      )}
                    </div>
                    <span className="bg-purple-100 text-purple-800 text-xs px-2 py-1 rounded">
                      {network.event_year}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-slate-500">No prophecy networks found.</p>
          )}
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6 border border-slate-200 mb-8">
        <h2 className="text-xl font-semibold text-slate-900 mb-4">Event Chains</h2>
        <div className="mb-4">
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Chain Length: {selectedChainLength} events
          </label>
          <input
            type="range"
            min="2"
            max="5"
            value={selectedChainLength}
            onChange={(e) => setSelectedChainLength(parseInt(e.target.value))}
            className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer"
          />
        </div>
        {eventChains && eventChains.length > 0 ? (
          <div className="space-y-4">
            {eventChains.slice(0, 3).map((chain: any, idx: number) => (
              <div key={idx} className="bg-slate-50 rounded-lg p-4 border border-slate-200">
                <div className="flex items-center gap-2 overflow-x-auto pb-2">
                  {chain.chain?.map((event: any, eventIdx: number) => (
                    <div key={eventIdx} className="flex items-center">
                      <div className="bg-white rounded-lg p-3 border-2 border-blue-300 min-w-[200px]">
                        <p className="font-semibold text-sm text-slate-900">{event.name}</p>
                        <p className="text-xs text-slate-500">Year {event.year_start || 'Unknown'}</p>
                      </div>
                      {eventIdx < chain.chain.length - 1 && (
                        <span className="text-blue-500 mx-2">→</span>
                      )}
                    </div>
                  ))}
                </div>
                <p className="text-xs text-slate-500 mt-2">
                  Chain length: {chain.chain_length} events
                </p>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-slate-500">No event chains found for this length.</p>
        )}
      </div>

      <div className="bg-white rounded-lg shadow-md p-6 border border-slate-200">
        <h2 className="text-xl font-semibold text-slate-900 mb-4">Path Finder</h2>
        <p className="text-slate-600 text-sm mb-4">
          Find the shortest path between nodes in the knowledge graph.
        </p>
        <div className="flex gap-2 mb-4">
          <input
            type="text"
            value={searchNodeId}
            onChange={(e) => setSearchNodeId(e.target.value)}
            placeholder="Enter node ID or name..."
            className="flex-1 px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={handleSearch}
            className="flex items-center gap-2 bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Search className="w-4 h-4" />
            Find Path
          </button>
        </div>
        {searchResult && (
          <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
            <p className="text-sm font-semibold text-blue-900 mb-2">
              Path found: {searchResult.path_length} nodes
            </p>
            <div className="flex flex-wrap gap-2">
              {searchResult.path_nodes?.map((node: any, idx: number) => (
                <span key={idx} className="bg-white text-blue-700 px-3 py-1 rounded-full text-sm border border-blue-300">
                  {node.name || node.reference || `Node ${idx + 1}`}
                </span>
              ))}
            </div>
            {searchResult.relationship_types && searchResult.relationship_types.length > 0 && (
              <div className="mt-3">
                <p className="text-xs text-blue-700 mb-1">Relationships:</p>
                <div className="flex flex-wrap gap-1">
                  {searchResult.relationship_types.map((rel: string, idx: number) => (
                    <span key={idx} className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">
                      {rel}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
