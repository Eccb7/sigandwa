'use client';

import { useEffect, useRef, useState } from 'react';
import { Network } from 'vis-network';
import { Download, Search, Filter, Maximize2, ZoomIn, ZoomOut } from 'lucide-react';

interface Node {
  id: number;
  label: string;
  type: 'event' | 'pattern' | 'prophecy';
  group?: string;
  title?: string;
}

interface Edge {
  from: number;
  to: number;
  label?: string;
  type?: string;
}

interface VisNetworkProps {
  nodes: Node[];
  edges: Edge[];
}

export default function VisNetwork({ nodes, edges }: VisNetworkProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const networkRef = useRef<Network | null>(null);
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterType, setFilterType] = useState<string>('');
  const [stats, setStats] = useState({ nodes: 0, edges: 0, clusters: 0 });

  useEffect(() => {
    if (!containerRef.current || !nodes.length) return;

    // Filter nodes and edges based on search and filter
    let filteredNodes = nodes;
    let filteredEdges = edges;

    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      filteredNodes = nodes.filter(n => 
        n.label.toLowerCase().includes(query) ||
        n.title?.toLowerCase().includes(query)
      );
      const nodeIds = new Set(filteredNodes.map(n => n.id));
      filteredEdges = edges.filter(e => nodeIds.has(e.from) && nodeIds.has(e.to));
    }

    if (filterType) {
      filteredNodes = filteredNodes.filter(n => n.type === filterType);
      const nodeIds = new Set(filteredNodes.map(n => n.id));
      filteredEdges = filteredEdges.filter(e => nodeIds.has(e.from) && nodeIds.has(e.to));
    }

    // Create vis.js data arrays (plain arrays work better with TypeScript)
    const nodesArray = filteredNodes.map(node => ({
      id: node.id,
      label: node.label,
      title: node.title || node.label,
      group: node.type,
      shape: node.type === 'event' ? 'dot' : node.type === 'pattern' ? 'diamond' : 'star',
      size: node.type === 'event' ? 15 : 25,
      font: { size: 12, face: 'Inter, sans-serif' },
      color: {
        background: node.type === 'event' ? '#3b82f6' : 
                   node.type === 'pattern' ? '#10b981' : '#8b5cf6',
        border: node.type === 'event' ? '#1e40af' : 
                node.type === 'pattern' ? '#047857' : '#6d28d9',
        highlight: {
          background: node.type === 'event' ? '#60a5fa' : 
                     node.type === 'pattern' ? '#34d399' : '#a78bfa',
          border: node.type === 'event' ? '#1e40af' : 
                  node.type === 'pattern' ? '#047857' : '#6d28d9'
        }
      }
    }));

    const edgesArray = filteredEdges.map(edge => ({
      from: edge.from,
      to: edge.to,
      label: edge.label,
      arrows: 'to',
      color: {
        color: edge.type === 'MATCHES_PATTERN' ? '#10b981' :
               edge.type === 'FULFILLED_BY' ? '#8b5cf6' :
               '#94a3b8',
        highlight: '#475569'
      },
      font: { size: 10, align: 'middle' },
      smooth: {
        enabled: true,
        type: 'continuous',
        roundness: 0.5
      }
    }));

    // Network options
    const options = {
      nodes: {
        borderWidth: 2,
        borderWidthSelected: 4,
        shadow: {
          enabled: true,
          color: 'rgba(0,0,0,0.1)',
          size: 10,
          x: 2,
          y: 2
        }
      },
      edges: {
        width: 2,
        shadow: {
          enabled: true,
          color: 'rgba(0,0,0,0.05)',
          size: 5,
          x: 1,
          y: 1
        }
      },
      physics: {
        enabled: true,
        barnesHut: {
          gravitationalConstant: -2000,
          centralGravity: 0.3,
          springLength: 150,
          springConstant: 0.04,
          damping: 0.09,
          avoidOverlap: 0.5
        },
        stabilization: {
          enabled: true,
          iterations: 1000,
          updateInterval: 25
        }
      },
      interaction: {
        hover: true,
        tooltipDelay: 100,
        navigationButtons: false,
        keyboard: {
          enabled: true,
          speed: { x: 10, y: 10, zoom: 0.02 },
          bindToWindow: false
        },
        zoomView: true,
        dragView: true
      },
      layout: {
        improvedLayout: true,
        hierarchical: false
      }
    };

    // Create network
    const network = new Network(
      containerRef.current,
      { nodes: nodesArray, edges: edgesArray },
      options
    );

    networkRef.current = network;

    // Event handlers
    network.on('click', (params) => {
      if (params.nodes.length > 0) {
        const nodeId = params.nodes[0];
        const node = filteredNodes.find(n => n.id === nodeId);
        if (node) {
          setSelectedNode(node);
        }
      } else {
        setSelectedNode(null);
      }
    });

    network.on('stabilizationProgress', (params) => {
      const progress = Math.round((params.iterations / params.total) * 100);
      console.log(`Stabilizing network: ${progress}%`);
    });

    network.on('stabilizationIterationsDone', () => {
      console.log('Network stabilized');
    });

    // Update stats
    setStats({
      nodes: filteredNodes.length,
      edges: filteredEdges.length,
      clusters: new Set(filteredNodes.map(n => n.type)).size
    });

    return () => {
      network.destroy();
    };
  }, [nodes, edges, searchQuery, filterType]);

  const handleZoomIn = () => {
    if (networkRef.current) {
      const scale = networkRef.current.getScale();
      networkRef.current.moveTo({ scale: scale * 1.2 });
    }
  };

  const handleZoomOut = () => {
    if (networkRef.current) {
      const scale = networkRef.current.getScale();
      networkRef.current.moveTo({ scale: scale * 0.8 });
    }
  };

  const handleFit = () => {
    if (networkRef.current) {
      networkRef.current.fit({
        animation: {
          duration: 500,
          easingFunction: 'easeInOutQuad'
        }
      });
    }
  };

  const handleExport = () => {
    if (!containerRef.current) return;
    
    // Get canvas from vis.js
    const canvas = containerRef.current.querySelector('canvas');
    if (!canvas) return;

    canvas.toBlob((blob) => {
      if (!blob) return;
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'network-graph.png';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    });
  };

  const handleStabilize = () => {
    if (networkRef.current) {
      networkRef.current.stabilize();
    }
  };

  return (
    <div className="space-y-4">
      {/* Controls */}
      <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div className="md:col-span-2">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Search nodes..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
          
          <div>
            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">All Types</option>
              <option value="event">Events Only</option>
              <option value="pattern">Patterns Only</option>
              <option value="prophecy">Prophecies Only</option>
            </select>
          </div>
        </div>

        <div className="flex flex-wrap gap-2 items-center justify-between">
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
              onClick={handleFit}
              className="p-2 bg-slate-50 hover:bg-slate-100 text-slate-600 rounded-lg transition-colors"
              title="Fit to Screen"
            >
              <Maximize2 className="w-5 h-5" />
            </button>
            <button
              onClick={handleStabilize}
              className="px-4 py-2 bg-purple-50 hover:bg-purple-100 text-purple-700 rounded-lg transition-colors text-sm font-medium"
            >
              Stabilize
            </button>
          </div>

          <div className="flex gap-2 items-center">
            <div className="text-sm text-slate-600">
              <span className="font-semibold">{stats.nodes}</span> nodes • 
              <span className="font-semibold ml-1">{stats.edges}</span> edges
            </div>
            <button
              onClick={handleExport}
              className="flex items-center gap-2 px-4 py-2 bg-green-50 hover:bg-green-100 text-green-700 rounded-lg transition-colors"
            >
              <Download className="w-4 h-4" />
              <span className="text-sm font-medium">Export PNG</span>
            </button>
          </div>
        </div>
      </div>

      {/* Legend */}
      <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-4">
        <h3 className="text-sm font-semibold text-slate-700 mb-3">Legend</h3>
        <div className="flex flex-wrap gap-4">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded-full bg-blue-500 border-2 border-blue-800"></div>
            <span className="text-sm text-slate-600">Events</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-green-500 border-2 border-green-800 transform rotate-45"></div>
            <span className="text-sm text-slate-600">Patterns</span>
          </div>
          <div className="flex items-center gap-2">
            <svg className="w-4 h-4" viewBox="0 0 24 24">
              <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z" fill="#8b5cf6" stroke="#6d28d9" strokeWidth="2"/>
            </svg>
            <span className="text-sm text-slate-600">Prophecies</span>
          </div>
        </div>
      </div>

      {/* Network Container */}
      <div className="bg-white rounded-lg shadow-lg border border-slate-200 overflow-hidden">
        <div 
          ref={containerRef} 
          className="w-full bg-gradient-to-br from-slate-50 to-slate-100"
          style={{ height: '700px' }}
        />
      </div>

      {/* Node Details Modal */}
      {selectedNode && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
          onClick={() => setSelectedNode(null)}
        >
          <div 
            className="bg-white rounded-lg shadow-2xl max-w-lg w-full"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="p-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-2xl font-bold text-slate-900">{selectedNode.label}</h3>
                  <span className={`inline-block mt-2 px-3 py-1 rounded-full text-sm font-medium ${
                    selectedNode.type === 'event' ? 'bg-blue-100 text-blue-800' :
                    selectedNode.type === 'pattern' ? 'bg-green-100 text-green-800' :
                    'bg-purple-100 text-purple-800'
                  }`}>
                    {selectedNode.type.charAt(0).toUpperCase() + selectedNode.type.slice(1)}
                  </span>
                </div>
                <button
                  onClick={() => setSelectedNode(null)}
                  className="text-slate-400 hover:text-slate-600 text-2xl"
                >
                  ×
                </button>
              </div>
              
              {selectedNode.title && (
                <div className="mt-4">
                  <span className="text-sm font-medium text-slate-500">Details:</span>
                  <p className="text-slate-700 mt-1">{selectedNode.title}</p>
                </div>
              )}

              <div className="mt-6 pt-4 border-t border-slate-200">
                <p className="text-sm text-slate-500">
                  Node ID: <span className="font-mono text-slate-700">{selectedNode.id}</span>
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Instructions */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <p className="text-sm text-blue-800">
          <strong>Tip:</strong> Drag nodes to rearrange • Click nodes for details • Scroll to zoom • Drag background to pan
        </p>
      </div>
    </div>
  );
}
