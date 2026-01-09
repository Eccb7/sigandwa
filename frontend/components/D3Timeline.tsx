'use client';

import { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import type { ChronologyEvent } from '@/lib/types';
import { ZoomIn, ZoomOut, Download, Maximize2 } from 'lucide-react';

interface D3TimelineProps {
  events: ChronologyEvent[];
}

export default function D3Timeline({ events }: D3TimelineProps) {
  const svgRef = useRef<SVGSVGElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [selectedEvent, setSelectedEvent] = useState<ChronologyEvent | null>(null);
  const [dimensions, setDimensions] = useState({ width: 0, height: 600 });

  useEffect(() => {
    if (!containerRef.current) return;
    
    const updateDimensions = () => {
      const width = containerRef.current?.clientWidth || 0;
      setDimensions({ width, height: 600 });
    };
    
    updateDimensions();
    window.addEventListener('resize', updateDimensions);
    return () => window.removeEventListener('resize', updateDimensions);
  }, []);

  useEffect(() => {
    if (!svgRef.current || events.length === 0 || dimensions.width === 0) return;

    const margin = { top: 80, right: 40, bottom: 80, left: 80 };
    const width = dimensions.width - margin.left - margin.right;
    const height = dimensions.height - margin.top - margin.bottom;

    // Clear previous content
    d3.select(svgRef.current).selectAll('*').remove();

    const svg = d3.select(svgRef.current)
      .attr('width', dimensions.width)
      .attr('height', dimensions.height);

    // Create main group with margins
    const g = svg.append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Sort events by year
    const sortedEvents = [...events].sort((a, b) => a.year_start - b.year_start);

    // Create scales
    const xScale = d3.scaleLinear()
      .domain([
        d3.min(sortedEvents, d => d.year_start) || -4004,
        d3.max(sortedEvents, d => d.year_end || d.year_start) || 2025
      ])
      .range([0, width]);

    // Group events by era for y-positioning
    const eraGroups = d3.group(sortedEvents, d => d.era);
    const eras = Array.from(eraGroups.keys());
    const yScale = d3.scaleBand()
      .domain(eras)
      .range([0, height])
      .padding(0.3);

    // Create zoom behavior
    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.5, 20])
      .extent([[0, 0], [width, height]])
      .translateExtent([[0, 0], [width, height]])
      .on('zoom', (event) => {
        const newXScale = event.transform.rescaleX(xScale);
        
        // Update axis
        g.select<SVGGElement>('.x-axis')
          .call(d3.axisBottom(newXScale).tickFormat(d => {
            const year = d as number;
            return year < 0 ? `${Math.abs(year)} BC` : `${year} AD`;
          }));

        // Update events
        g.selectAll<SVGCircleElement, ChronologyEvent>('.event-circle')
          .attr('cx', d => newXScale(d.year_start));

        // Update event lines
        g.selectAll<SVGLineElement, ChronologyEvent>('.event-line')
          .attr('x1', d => newXScale(d.year_start))
          .attr('x2', d => newXScale(d.year_end || d.year_start));

        // Update labels
        g.selectAll<SVGTextElement, ChronologyEvent>('.event-label')
          .attr('x', d => newXScale(d.year_start));
      });

    svg.call(zoom);

    // Add gradient definitions
    const defs = svg.append('defs');
    
    const gradient = defs.append('linearGradient')
      .attr('id', 'timeline-gradient')
      .attr('x1', '0%')
      .attr('x2', '100%');
    
    gradient.append('stop')
      .attr('offset', '0%')
      .attr('stop-color', '#3b82f6')
      .attr('stop-opacity', 0.1);
    
    gradient.append('stop')
      .attr('offset', '100%')
      .attr('stop-color', '#8b5cf6')
      .attr('stop-opacity', 0.1);

    // Add background gradient
    g.append('rect')
      .attr('width', width)
      .attr('height', height)
      .attr('fill', 'url(#timeline-gradient)')
      .attr('rx', 8);

    // Add era bands
    eras.forEach(era => {
      g.append('rect')
        .attr('x', 0)
        .attr('y', yScale(era) || 0)
        .attr('width', width)
        .attr('height', yScale.bandwidth())
        .attr('fill', 'none')
        .attr('stroke', '#e2e8f0')
        .attr('stroke-width', 1)
        .attr('stroke-dasharray', '4,4');
    });

    // Add X axis
    const xAxis = g.append('g')
      .attr('class', 'x-axis')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(xScale).tickFormat(d => {
        const year = d as number;
        return year < 0 ? `${Math.abs(year)} BC` : `${year} AD`;
      }));

    xAxis.selectAll('text')
      .style('font-size', '12px')
      .style('fill', '#475569');

    xAxis.selectAll('line')
      .style('stroke', '#cbd5e1');

    xAxis.select('.domain')
      .style('stroke', '#cbd5e1');

    // Add Y axis (eras)
    const yAxis = g.append('g')
      .attr('class', 'y-axis')
      .call(d3.axisLeft(yScale));

    yAxis.selectAll('text')
      .style('font-size', '11px')
      .style('fill', '#64748b')
      .style('font-weight', '500');

    yAxis.select('.domain')
      .style('stroke', '#cbd5e1');

    yAxis.selectAll('line')
      .style('stroke', 'none');

    // Add grid lines
    g.append('g')
      .attr('class', 'grid')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(xScale)
        .tickSize(-height)
        .tickFormat(() => '')
      )
      .style('stroke-opacity', 0.1);

    // Color scale for event types
    const colorScale = d3.scaleOrdinal<string>()
      .domain(['CREATION', 'JUDGMENT', 'COVENANT', 'DELIVERANCE', 'CONQUEST', 
               'APOSTASY', 'PROPHECY', 'FULFILLMENT', 'RESTORATION', 'INSTITUTION'])
      .range(['#3b82f6', '#ef4444', '#8b5cf6', '#10b981', '#f59e0b',
              '#dc2626', '#6366f1', '#ec4899', '#14b8a6', '#06b6d4']);

    // Add event duration lines (for events with end dates)
    g.selectAll('.event-line')
      .data(sortedEvents.filter(e => e.year_end && e.year_end !== e.year_start))
      .join('line')
      .attr('class', 'event-line')
      .attr('x1', d => xScale(d.year_start))
      .attr('x2', d => xScale(d.year_end || d.year_start))
      .attr('y1', d => (yScale(d.era) || 0) + yScale.bandwidth() / 2)
      .attr('y2', d => (yScale(d.era) || 0) + yScale.bandwidth() / 2)
      .attr('stroke', d => colorScale(d.event_type))
      .attr('stroke-width', 3)
      .attr('opacity', 0.4);

    // Add event circles
    const circles = g.selectAll('.event-circle')
      .data(sortedEvents)
      .join('circle')
      .attr('class', 'event-circle')
      .attr('cx', d => xScale(d.year_start))
      .attr('cy', d => (yScale(d.era) || 0) + yScale.bandwidth() / 2)
      .attr('r', d => d.is_pivotal ? 8 : 5)
      .attr('fill', d => colorScale(d.event_type))
      .attr('stroke', '#fff')
      .attr('stroke-width', 2)
      .style('cursor', 'pointer')
      .on('mouseover', function(event, d) {
        d3.select(this)
          .transition()
          .duration(200)
          .attr('r', d.is_pivotal ? 12 : 8);

        // Show tooltip
        const tooltip = g.append('g')
          .attr('class', 'tooltip')
          .attr('transform', `translate(${xScale(d.year_start)},${(yScale(d.era) || 0) + yScale.bandwidth() / 2 - 40})`);

        tooltip.append('rect')
          .attr('x', -100)
          .attr('y', -30)
          .attr('width', 200)
          .attr('height', 60)
          .attr('fill', 'white')
          .attr('stroke', '#cbd5e1')
          .attr('stroke-width', 1)
          .attr('rx', 6)
          .style('filter', 'drop-shadow(0 4px 6px rgba(0, 0, 0, 0.1))');

        tooltip.append('text')
          .attr('text-anchor', 'middle')
          .attr('y', -12)
          .style('font-size', '12px')
          .style('font-weight', '600')
          .style('fill', '#1e293b')
          .text(d.name);

        tooltip.append('text')
          .attr('text-anchor', 'middle')
          .attr('y', 5)
          .style('font-size', '10px')
          .style('fill', '#64748b')
          .text(`${d.year_start}${d.year_end ? ` - ${d.year_end}` : ''}`);

        tooltip.append('text')
          .attr('text-anchor', 'middle')
          .attr('y', 20)
          .style('font-size', '10px')
          .style('fill', '#475569')
          .text(d.event_type);
      })
      .on('mouseout', function(event, d) {
        d3.select(this)
          .transition()
          .duration(200)
          .attr('r', d.is_pivotal ? 8 : 5);

        g.selectAll('.tooltip').remove();
      })
      .on('click', (event, d) => {
        setSelectedEvent(d);
      });

    // Add title
    svg.append('text')
      .attr('x', dimensions.width / 2)
      .attr('y', 30)
      .attr('text-anchor', 'middle')
      .style('font-size', '20px')
      .style('font-weight', '700')
      .style('fill', '#1e293b')
      .text('Interactive Biblical Timeline');

    svg.append('text')
      .attr('x', dimensions.width / 2)
      .attr('y', 52)
      .attr('text-anchor', 'middle')
      .style('font-size', '13px')
      .style('fill', '#64748b')
      .text('Scroll to zoom • Drag to pan • Click events for details');

  }, [events, dimensions]);

  const handleZoomIn = () => {
    d3.select(svgRef.current)
      .transition()
      .duration(300)
      .call(d3.zoom<SVGSVGElement, unknown>().scaleBy as any, 1.5);
  };

  const handleZoomOut = () => {
    d3.select(svgRef.current)
      .transition()
      .duration(300)
      .call(d3.zoom<SVGSVGElement, unknown>().scaleBy as any, 0.67);
  };

  const handleReset = () => {
    d3.select(svgRef.current)
      .transition()
      .duration(500)
      .call(d3.zoom<SVGSVGElement, unknown>().transform as any, d3.zoomIdentity);
  };

  const handleExport = () => {
    if (!svgRef.current) return;
    
    const svgData = new XMLSerializer().serializeToString(svgRef.current);
    const svgBlob = new Blob([svgData], { type: 'image/svg+xml;charset=utf-8' });
    const svgUrl = URL.createObjectURL(svgBlob);
    
    const downloadLink = document.createElement('a');
    downloadLink.href = svgUrl;
    downloadLink.download = 'timeline.svg';
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
    URL.revokeObjectURL(svgUrl);
  };

  return (
    <div className="space-y-4">
      {/* Controls */}
      <div className="flex justify-between items-center bg-white p-4 rounded-lg shadow-sm border border-slate-200">
        <div className="flex gap-2">
          <button
            onClick={handleZoomIn}
            className="p-2 bg-blue-50 hover:bg-blue-100 text-blue-600 rounded-lg transition-colors"
            title="Zoom In"
          >
            <ZoomIn className="w-5 h-5" />
          </button>
          <button
            onClick={handleZoomOut}
            className="p-2 bg-blue-50 hover:bg-blue-100 text-blue-600 rounded-lg transition-colors"
            title="Zoom Out"
          >
            <ZoomOut className="w-5 h-5" />
          </button>
          <button
            onClick={handleReset}
            className="p-2 bg-slate-50 hover:bg-slate-100 text-slate-600 rounded-lg transition-colors"
            title="Reset View"
          >
            <Maximize2 className="w-5 h-5" />
          </button>
        </div>
        <button
          onClick={handleExport}
          className="flex items-center gap-2 px-4 py-2 bg-green-50 hover:bg-green-100 text-green-700 rounded-lg transition-colors"
        >
          <Download className="w-4 h-4" />
          <span className="text-sm font-medium">Export SVG</span>
        </button>
      </div>

      {/* Timeline */}
      <div ref={containerRef} className="bg-white rounded-lg shadow-lg border border-slate-200 overflow-hidden">
        <svg ref={svgRef}></svg>
      </div>

      {/* Event Detail Modal */}
      {selectedEvent && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
          onClick={() => setSelectedEvent(null)}
        >
          <div 
            className="bg-white rounded-lg shadow-2xl max-w-2xl w-full max-h-[80vh] overflow-y-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="p-6">
              <div className="flex justify-between items-start mb-4">
                <h3 className="text-2xl font-bold text-slate-900">{selectedEvent.name}</h3>
                <button
                  onClick={() => setSelectedEvent(null)}
                  className="text-slate-400 hover:text-slate-600 text-2xl"
                >
                  ×
                </button>
              </div>
              
              <div className="space-y-4">
                <div>
                  <span className="text-sm font-medium text-slate-500">Date:</span>
                  <p className="text-slate-900">
                    {selectedEvent.year_start}
                    {selectedEvent.year_end && ` to ${selectedEvent.year_end}`}
                  </p>
                </div>
                
                <div>
                  <span className="text-sm font-medium text-slate-500">Description:</span>
                  <p className="text-slate-700 mt-1">{selectedEvent.description}</p>
                </div>
                
                <div className="flex gap-2">
                  <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-slate-100 text-slate-800">
                    {selectedEvent.era}
                  </span>
                  <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                    {selectedEvent.event_type}
                  </span>
                  {selectedEvent.is_pivotal && (
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-yellow-100 text-yellow-800">
                      Pivotal Event
                    </span>
                  )}
                </div>

                {selectedEvent.key_actors && selectedEvent.key_actors.length > 0 && (
                  <div>
                    <span className="text-sm font-medium text-slate-500">Key Actors:</span>
                    <p className="text-slate-700 mt-1">{selectedEvent.key_actors.join(', ')}</p>
                  </div>
                )}

                {selectedEvent.source_references && selectedEvent.source_references.length > 0 && (
                  <div>
                    <span className="text-sm font-medium text-slate-500">Sources:</span>
                    <p className="text-slate-700 mt-1">{selectedEvent.source_references.join(', ')}</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
