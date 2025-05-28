import React, { useMemo } from 'react';
import { Target, Navigation } from 'lucide-react';

interface Coordinate {
  point_number: number;
  x: number;
  y: number;
  label: string;
  description: string;
  monument?: string;
  bearing?: string;
  distance?: number;
  units?: string;
}

interface ClosureData {
  closure_distance: number;
  closure_bearing: string;
  precision_ratio: string;
  area_acres: number;
  area_sq_feet: number;
  perimeter_feet: number;
  is_closed: boolean;
  closure_error_ppm: number;
}

interface InteractivePlotProps {
  coordinates: Coordinate[];
  showGrid?: boolean;
  showLabels?: boolean;
  showBearings?: boolean;
  showDistances?: boolean;
  closure?: ClosureData;
}

const InteractivePlot: React.FC<InteractivePlotProps> = ({
  coordinates,
  showGrid = true,
  showLabels = true,
  showBearings = true,
  showDistances = true,
  closure
}) => {
  // Calculate plot dimensions and scale
  const plotData = useMemo(() => {
    if (!coordinates || coordinates.length === 0) {
      return { 
        scale: 1, 
        offsetX: 0, 
        offsetY: 0, 
        width: 800, 
        height: 600,
        bounds: { minX: 0, maxX: 0, minY: 0, maxY: 0 }
      };
    }

    const xs = coordinates.map(c => c.x);
    const ys = coordinates.map(c => c.y);
    
    const minX = Math.min(...xs);
    const maxX = Math.max(...xs);
    const minY = Math.min(...ys);
    const maxY = Math.max(...ys);
    
    const rangeX = maxX - minX;
    const rangeY = maxY - minY;
    
    // Add padding
    const padding = 50;
    const plotWidth = 800 - 2 * padding;
    const plotHeight = 600 - 2 * padding;
    
    // Calculate scale to fit both dimensions
    const scaleX = rangeX > 0 ? plotWidth / rangeX : 1;
    const scaleY = rangeY > 0 ? plotHeight / rangeY : 1;
    const scale = Math.min(scaleX, scaleY) * 0.9; // 90% for extra margin
    
    const offsetX = padding + (plotWidth - rangeX * scale) / 2 - minX * scale;
    const offsetY = padding + (plotHeight - rangeY * scale) / 2 - minY * scale;
    
    return {
      scale,
      offsetX,
      offsetY,
      width: 800,
      height: 600,
      bounds: { minX, maxX, minY, maxY }
    };
  }, [coordinates]);

  // Transform coordinate to screen space
  const transformPoint = (x: number, y: number) => ({
    x: x * plotData.scale + plotData.offsetX,
    y: plotData.height - (y * plotData.scale + plotData.offsetY) // Flip Y for screen coordinates
  });

  // Generate grid lines
  const generateGrid = () => {
    if (!showGrid) return null;
    
    const { bounds } = plotData;
    const gridSpacing = Math.pow(10, Math.floor(Math.log10(Math.max(bounds.maxX - bounds.minX, bounds.maxY - bounds.minY) / 10)));
    
    const lines = [];
    
    // Vertical lines
    for (let x = Math.floor(bounds.minX / gridSpacing) * gridSpacing; x <= bounds.maxX; x += gridSpacing) {
      const start = transformPoint(x, bounds.minY);
      const end = transformPoint(x, bounds.maxY);
      lines.push(
        <line
          key={`v-${x}`}
          x1={start.x}
          y1={start.y}
          x2={end.x}
          y2={end.y}
          stroke="#e5e7eb"
          strokeWidth="1"
        />
      );
    }
    
    // Horizontal lines
    for (let y = Math.floor(bounds.minY / gridSpacing) * gridSpacing; y <= bounds.maxY; y += gridSpacing) {
      const start = transformPoint(bounds.minX, y);
      const end = transformPoint(bounds.maxX, y);
      lines.push(
        <line
          key={`h-${y}`}
          x1={start.x}
          y1={start.y}
          x2={end.x}
          y2={end.y}
          stroke="#e5e7eb"
          strokeWidth="1"
        />
      );
    }
    
    return lines;
  };

  // Generate property boundary lines
  const generateBoundaryLines = () => {
    if (coordinates.length < 2) return null;
    
    const lines = [];
    
    for (let i = 0; i < coordinates.length; i++) {
      const current = coordinates[i];
      const next = coordinates[(i + 1) % coordinates.length];
      
      const start = transformPoint(current.x, current.y);
      const end = transformPoint(next.x, next.y);
      
      lines.push(
        <line
          key={`boundary-${i}`}
          x1={start.x}
          y1={start.y}
          x2={end.x}
          y2={end.y}
          stroke="#2563eb"
          strokeWidth="2"
          className="hover:stroke-primary-700 cursor-pointer"
        />
      );
      
      // Add bearing and distance labels
      if ((showBearings || showDistances) && next.bearing && next.distance) {
        const midX = (start.x + end.x) / 2;
        const midY = (start.y + end.y) / 2;
        
        let label = '';
        if (showBearings && showDistances) {
          label = `${next.bearing} ${next.distance}${next.units || 'ft'}`;
        } else if (showBearings) {
          label = next.bearing;
        } else if (showDistances) {
          label = `${next.distance}${next.units || 'ft'}`;
        }
        
        lines.push(
          <text
            key={`label-${i}`}
            x={midX}
            y={midY - 5}
            textAnchor="middle"
            className="text-xs fill-gray-600 font-mono"
            style={{ fontSize: '10px' }}
          >
            {label}
          </text>
        );
      }
    }
    
    return lines;
  };

  // Generate closure line if not closed
  const generateClosureLine = () => {
    if (!closure || closure.is_closed || coordinates.length < 2) return null;
    
    const first = coordinates[0];
    const last = coordinates[coordinates.length - 1];
    
    const start = transformPoint(last.x, last.y);
    const end = transformPoint(first.x, first.y);
    
    return (
      <line
        x1={start.x}
        y1={start.y}
        x2={end.x}
        y2={end.y}
        stroke="#ef4444"
        strokeWidth="2"
        strokeDasharray="5,5"
        className="opacity-70"
      />
    );
  };

  // Generate point markers
  const generatePoints = () => {
    return coordinates.map((coord, index) => {
      const point = transformPoint(coord.x, coord.y);
      
      return (
        <g key={`point-${index}`}>
          {/* Point marker */}
          <circle
            cx={point.x}
            cy={point.y}
            r="4"
            fill={coord.label === 'POB' ? '#dc2626' : '#2563eb'}
            stroke="white"
            strokeWidth="2"
            className="hover:r-6 cursor-pointer transition-all"
          />
          
          {/* Monument indicator */}
          {coord.monument && (
            <circle
              cx={point.x}
              cy={point.y}
              r="8"
              fill="none"
              stroke="#059669"
              strokeWidth="2"
              strokeDasharray="2,2"
            />
          )}
          
          {/* Label */}
          {showLabels && (
            <text
              x={point.x}
              y={point.y - 15}
              textAnchor="middle"
              className="text-xs font-semibold fill-gray-900"
              style={{ fontSize: '11px' }}
            >
              {coord.label}
            </text>
          )}
        </g>
      );
    });
  };

  if (!coordinates || coordinates.length === 0) {
    return (
      <div className="flex items-center justify-center h-96 bg-gray-50 rounded-lg">
        <div className="text-center">
          <Target className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-500">No coordinates to plot</p>
        </div>
      </div>
    );
  }

  return (
    <div className="relative bg-white rounded-lg border border-gray-200 overflow-hidden">
      {/* Plot SVG */}
      <svg
        width={plotData.width}
        height={plotData.height}
        className="w-full h-auto"
        viewBox={`0 0 ${plotData.width} ${plotData.height}`}
      >
        {/* Grid */}
        {generateGrid()}
        
        {/* Boundary lines */}
        {generateBoundaryLines()}
        
        {/* Closure line */}
        {generateClosureLine()}
        
        {/* Points */}
        {generatePoints()}
        
        {/* North arrow */}
        <g transform="translate(50, 50)">
          <Navigation size={24} className="fill-gray-600" />
          <text x="30" y="20" className="text-xs fill-gray-600" style={{ fontSize: '10px' }}>
            N
          </text>
        </g>
      </svg>
      
      {/* Legend */}
      <div className="absolute bottom-4 right-4 bg-white bg-opacity-90 p-3 rounded-lg border border-gray-200 text-xs">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <div className="w-3 h-0.5 bg-blue-600"></div>
            <span>Property Boundary</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-red-600 rounded-full"></div>
            <span>Point of Beginning</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-blue-600 rounded-full"></div>
            <span>Survey Point</span>
          </div>
          {!closure?.is_closed && (
            <div className="flex items-center gap-2">
              <div className="w-3 h-0.5 bg-red-600" style={{ borderTop: '2px dashed' }}></div>
              <span>Closure Error</span>
            </div>
          )}
        </div>
      </div>
      
      {/* Scale indicator */}
      <div className="absolute bottom-4 left-4 bg-white bg-opacity-90 p-2 rounded-lg border border-gray-200 text-xs">
        <div>Scale: 1" = {(100 / plotData.scale).toFixed(1)}ft</div>
      </div>
    </div>
  );
};

export default InteractivePlot; 