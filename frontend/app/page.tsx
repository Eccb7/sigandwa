'use client';

import { useQuery } from '@tanstack/react-query';
import { 
  Calendar, 
  Activity, 
  BookOpen, 
  TrendingUp, 
  Network,
  AlertCircle,
  CheckCircle2
} from 'lucide-react';
import { chronologyAPI, patternAPI, prophecyAPI, simulationAPI, graphAPI } from '@/lib/api';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  AreaChart,
  Area
} from 'recharts';

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
    <div className="bg-white overflow-hidden shadow rounded-lg">
      <div className="p-5">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <Icon className="h-6 w-6 text-slate-400" />
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

function RiskIndicator({ level, score }: { level: string; score: number }) {
  const getLevelColor = (level: string) => {
    switch (level.toUpperCase()) {
      case 'LOW': return 'bg-green-100 text-green-800 border-green-200';
      case 'MODERATE': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'HIGH': return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'CRITICAL': return 'bg-red-100 text-red-800 border-red-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  return (
    <div className="bg-white overflow-hidden shadow rounded-lg">
      <div className="p-5">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-medium text-slate-900">
              Civilization Risk Assessment
            </h3>
            <p className="mt-1 text-sm text-slate-500">
              Based on 25 world indicators and 6 pattern templates
            </p>
          </div>
          <AlertCircle className="h-8 w-8 text-slate-400" />
        </div>
        <div className="mt-4">
          <div className="flex items-center justify-between">
            <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border ${getLevelColor(level)}`}>
              {level}
            </span>
            <span className="text-3xl font-bold text-slate-900">
              {(score * 100).toFixed(1)}%
            </span>
          </div>
          <div className="mt-3 w-full bg-slate-200 rounded-full h-2">
            <div 
              className={`h-2 rounded-full ${
                score < 0.3 ? 'bg-green-500' :
                score < 0.5 ? 'bg-yellow-500' :
                score < 0.7 ? 'bg-orange-500' :
                'bg-red-500'
              }`}
              style={{ width: `${score * 100}%` }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export default function DashboardPage() {
  const { data: chronologyStats, isLoading: loadingChronology } = useQuery({
    queryKey: ['chronology-stats'],
    queryFn: async () => {
      const response = await chronologyAPI.getStats();
      return response.data;
    },
  });

  const { data: events } = useQuery({
    queryKey: ['all-events'],
    queryFn: async () => {
      const response = await chronologyAPI.getEvents();
      return response.data;
    },
  });

  const { data: patterns, isLoading: loadingPatterns } = useQuery({
    queryKey: ['patterns'],
    queryFn: async () => {
      const response = await patternAPI.getPatterns();
      return response.data;
    },
  });

  const { data: prophecies, isLoading: loadingProphecies } = useQuery({
    queryKey: ['prophecies'],
    queryFn: async () => {
      const response = await prophecyAPI.getProphecies();
      return response.data;
    },
  });

  const { data: riskAssessment, isLoading: loadingRisk } = useQuery({
    queryKey: ['risk-assessment'],
    queryFn: async () => {
      const response = await simulationAPI.getRiskAssessment();
      return response.data;
    },
  });

  const { data: graphStats, isLoading: loadingGraph } = useQuery({
    queryKey: ['graph-stats'],
    queryFn: async () => {
      const response = await graphAPI.getStats();
      return response.data;
    },
  });

  const isLoading = loadingChronology || loadingPatterns || loadingProphecies || loadingRisk || loadingGraph;

  // Prepare data for charts
  const eventsByEra = events?.reduce((acc: any, event: any) => {
    acc[event.era] = (acc[event.era] || 0) + 1;
    return acc;
  }, {});

  const eraChartData = eventsByEra ? Object.entries(eventsByEra).map(([era, count]) => ({
    era: era.replace(/_/g, ' '),
    count
  })) : [];

  const eventsByType = events?.reduce((acc: any, event: any) => {
    acc[event.event_type] = (acc[event.event_type] || 0) + 1;
    return acc;
  }, {});

  const typeChartData = eventsByType ? Object.entries(eventsByType).map(([type, count]) => ({
    name: type,
    value: count
  })) : [];

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#06b6d4', '#14b8a6'];

  // Timeline distribution
  const timelineData = events?.reduce((acc: any[], event: any) => {
    const century = Math.floor(event.year_start / 100) * 100;
    const existing = acc.find(item => item.century === century);
    if (existing) {
      existing.events += 1;
    } else {
      acc.push({ century, events: 1 });
    }
    return acc;
  }, []).sort((a: any, b: any) => a.century - b.century) || [];

  // Pattern instances data
  const patternData = patterns?.map((pattern: any) => ({
    name: pattern.name.substring(0, 20),
    duration: pattern.typical_duration_years || 0
  })) || [];

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-slate-900"></div>
          <p className="mt-2 text-sm text-slate-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4 sm:space-y-6">
      <div className="border-b border-slate-200 pb-4 sm:pb-5">
        <h1 className="text-2xl sm:text-3xl font-bold leading-tight text-slate-900">
          Dashboard
        </h1>
        <p className="mt-2 text-xs sm:text-sm text-slate-600">
          Biblical Cliodynamics Analysis System
        </p>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4 sm:gap-5">
        <StatCard
          title="Historical Events"
          value={chronologyStats?.total_events || 0}
          icon={Calendar}
          description="From Creation to Present"
        />
        <StatCard
          title="Pattern Templates"
          value={patterns?.length || 0}
          icon={Activity}
          description="Recurring cycles"
        />
        <StatCard
          title="Tracked Prophecies"
          value={prophecies?.length || 0}
          icon={BookOpen}
          description="With fulfillment analysis"
        />
        <StatCard
          title="Graph Relationships"
          value={graphStats?.total_relationships || 0}
          icon={Network}
          description={`${graphStats?.total_events || 0} nodes`}
        />
      </div>

      {riskAssessment && (
        <RiskIndicator
          level={riskAssessment.risk_level}
          score={riskAssessment.overall_risk}
        />
      )}

      {/* Recharts Visualizations */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
        {/* Events by Era */}
        <div className="bg-white shadow rounded-lg p-4 sm:p-6">
          <h3 className="text-base sm:text-lg font-medium text-slate-900 mb-3 sm:mb-4">
            Events by Era
          </h3>
          <div className="w-full overflow-x-auto">
            <ResponsiveContainer width="100%" height={250} minWidth={300}>
              <BarChart data={eraChartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis 
                  dataKey="era" 
                  angle={-45} 
                  textAnchor="end" 
                  height={100}
                  tick={{ fontSize: 9 }}
                />
                <YAxis tick={{ fontSize: 10 }} />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#fff', 
                    border: '1px solid #e2e8f0',
                    borderRadius: '8px',
                    fontSize: '12px'
                  }}
                />
                <Bar dataKey="count" fill="#3b82f6" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Events by Type */}
        <div className="bg-white shadow rounded-lg p-4 sm:p-6">
          <h3 className="text-base sm:text-lg font-medium text-slate-900 mb-3 sm:mb-4">
            Event Types Distribution
          </h3>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={typeChartData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={(entry) => entry.name}
                outerRadius={70}
                fill="#8884d8"
                dataKey="value"
              >
                {typeChartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip contentStyle={{ fontSize: '12px' }} />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Timeline Distribution */}
        <div className="bg-white shadow rounded-lg p-4 sm:p-6">
          <h3 className="text-base sm:text-lg font-medium text-slate-900 mb-3 sm:mb-4">
            Historical Timeline Distribution
          </h3>
          <div className="w-full overflow-x-auto">
            <ResponsiveContainer width="100%" height={250} minWidth={300}>
              <AreaChart data={timelineData}>
                <defs>
                  <linearGradient id="colorEvents" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis 
                  dataKey="century" 
                  tickFormatter={(value) => value < 0 ? `${Math.abs(value)} BC` : `${value} AD`}
                  tick={{ fontSize: 9 }}
                />
                <YAxis tick={{ fontSize: 10 }} />
                <Tooltip 
                  labelFormatter={(value) => value < 0 ? `${Math.abs(value)} BC` : `${value} AD`}
                  contentStyle={{ 
                    backgroundColor: '#fff', 
                    border: '1px solid #e2e8f0',
                    borderRadius: '8px',
                    fontSize: '12px'
                  }}
                />
                <Area 
                  type="monotone" 
                  dataKey="events" 
                  stroke="#3b82f6" 
                  fillOpacity={1} 
                  fill="url(#colorEvents)" 
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Pattern Analysis */}
        <div className="bg-white shadow rounded-lg p-4 sm:p-6">
          <h3 className="text-base sm:text-lg font-medium text-slate-900 mb-3 sm:mb-4">
            Pattern Duration Analysis
          </h3>
          <div className="w-full overflow-x-auto">
            <ResponsiveContainer width="100%" height={250} minWidth={300}>
              <LineChart data={patternData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis 
                  dataKey="name" 
                  angle={-45} 
                  textAnchor="end" 
                  height={100}
                  tick={{ fontSize: 9 }}
                />
                <YAxis tick={{ fontSize: 10 }} />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#fff', 
                    border: '1px solid #e2e8f0',
                    borderRadius: '8px',
                    fontSize: '12px'
                  }}
                />
                <Legend wrapperStyle={{ fontSize: '12px' }} />
                <Line 
                  type="monotone" 
                  dataKey="duration" 
                  stroke="#10b981" 
                  strokeWidth={2}
                  dot={{ fill: '#10b981', r: 3 }}
                  name="Duration (years)"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="bg-white shadow rounded-lg p-4 sm:p-6">
        <h3 className="text-base sm:text-lg font-medium text-slate-900 mb-3 sm:mb-4">
          System Status
        </h3>
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs sm:text-sm text-slate-600">PostgreSQL Database</span>
            <CheckCircle2 className="h-5 w-5 text-green-500" />
          </div>
          <div className="flex items-center justify-between">
            <span className="text-xs sm:text-sm text-slate-600">Neo4j Graph Database</span>
            <CheckCircle2 className="h-5 w-5 text-green-500" />
          </div>
          <div className="flex items-center justify-between">
            <span className="text-xs sm:text-sm text-slate-600">FastAPI Backend</span>
            <CheckCircle2 className="h-5 w-5 text-green-500" />
          </div>
        </div>
      </div>
    </div>
  );
}
