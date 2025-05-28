import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import toast from 'react-hot-toast';
import { 
  Map, 
  Download, 
  RefreshCw, 
  CheckCircle, 
  AlertCircle, 
  Target, 
  Layers,
  Grid3x3,
  Compass,
  Calculator
} from 'lucide-react';
import InteractivePlot from '../components/Plot/InteractivePlot';
import ClosureReport from '../components/Plot/ClosureReport';
import ExportMenu from '../components/Plot/ExportMenu';
import { plotDeed, type DocumentData } from '../services/api';

interface PlotData {
  success: boolean;
  plot_data: {
    coordinates: Array<{
      point_number: number;
      x: number;
      y: number;
      label: string;
      description: string;
      monument?: string;
      bearing?: string;
      distance?: number;
      units?: string;
    }>;
    closure_analysis: {
      closure_distance: number;
      closure_bearing: string;
      precision_ratio: string;
      area_acres: number;
      area_sq_feet: number;
      perimeter_feet: number;
      is_closed: boolean;
      closure_error_ppm: number;
    };
    plotting_instructions: any;
    export_formats: any;
  };
}

const PlottingPage: React.FC = () => {
  const location = useLocation();
  const [documentData, setDocumentData] = useState<DocumentData | null>(null);
  const [plotData, setPlotData] = useState<PlotData | null>(null);
  const [showGrid, setShowGrid] = useState(true);
  const [showLabels, setShowLabels] = useState(true);
  const [showBearings, setShowBearings] = useState(true);
  const [showDistances, setShowDistances] = useState(true);

  // Get document data from navigation state
  useEffect(() => {
    if (location.state?.documentData) {
      setDocumentData(location.state.documentData);
    }
  }, [location.state]);

  // Plotting mutation
  const plottingMutation = useMutation({
    mutationFn: plotDeed,
    onSuccess: (data) => {
      setPlotData(data);
      toast.success('Deed plotted successfully!');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.message || 'Plotting failed');
    },
  });

  // Auto-plot when document is available
  useEffect(() => {
    if (documentData && !plotData && !plottingMutation.isPending) {
      plottingMutation.mutate(documentData.extracted_text);
    }
  }, [documentData, plotData, plottingMutation]);

  const handleReplot = () => {
    if (documentData) {
      plottingMutation.mutate(documentData.extracted_text);
    }
  };

  if (!documentData) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="card text-center py-12">
          <Map className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">
            No Document to Plot
          </h2>
          <p className="text-gray-600">
            Please upload a document from the home page to start plotting.
          </p>
        </div>
      </div>
    );
  }

  const closure = plotData?.plot_data?.closure_analysis;
  const coordinates = plotData?.plot_data?.coordinates || [];

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Interactive Deed Plot</h1>
          <p className="text-gray-600 mt-2">
            AI-powered deed plotting with precision analysis
          </p>
        </div>
        
        <div className="flex gap-3">
          <button
            onClick={handleReplot}
            disabled={plottingMutation.isPending}
            className="btn-secondary"
          >
            <RefreshCw size={16} className={plottingMutation.isPending ? 'animate-spin' : ''} />
            Re-plot
          </button>
          {plotData && (
            <ExportMenu coordinates={coordinates} />
          )}
        </div>
      </div>

      {/* Plot Controls */}
      {plotData && (
        <div className="card mb-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Plot Controls</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={showGrid}
                onChange={(e) => setShowGrid(e.target.checked)}
                className="rounded border-gray-300 text-primary-600 mr-2"
              />
              <Grid3x3 size={16} className="mr-1" />
              <span className="text-sm">Grid</span>
            </label>
            
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={showLabels}
                onChange={(e) => setShowLabels(e.target.checked)}
                className="rounded border-gray-300 text-primary-600 mr-2"
              />
              <Target size={16} className="mr-1" />
              <span className="text-sm">Labels</span>
            </label>
            
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={showBearings}
                onChange={(e) => setShowBearings(e.target.checked)}
                className="rounded border-gray-300 text-primary-600 mr-2"
              />
              <Compass size={16} className="mr-1" />
              <span className="text-sm">Bearings</span>
            </label>
            
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={showDistances}
                onChange={(e) => setShowDistances(e.target.checked)}
                className="rounded border-gray-300 text-primary-600 mr-2"
              />
              <Calculator size={16} className="mr-1" />
              <span className="text-sm">Distances</span>
            </label>
          </div>
        </div>
      )}

      {/* Plotting Results */}
      {plottingMutation.isPending && (
        <div className="card text-center py-12">
          <div className="loading-dots mx-auto mb-4">
            <div></div>
            <div></div>
            <div></div>
            <div></div>
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Plotting Deed...
          </h3>
          <p className="text-gray-600">
            AI is calculating coordinates and generating the plot. This may take a moment.
          </p>
        </div>
      )}

      {plotData && (
        <div className="grid lg:grid-cols-3 gap-6">
          {/* Main Plot Area */}
          <div className="lg:col-span-2">
            <div className="card p-4">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">Plot Visualization</h3>
                <div className="flex items-center gap-2">
                  {closure?.is_closed ? (
                    <CheckCircle className="h-5 w-5 text-green-600" />
                  ) : (
                    <AlertCircle className="h-5 w-5 text-yellow-600" />
                  )}
                  <span className="text-sm font-medium">
                    {closure?.is_closed ? 'Closed' : 'Open'}
                  </span>
                </div>
              </div>
              
              <InteractivePlot
                coordinates={coordinates}
                showGrid={showGrid}
                showLabels={showLabels}
                showBearings={showBearings}
                showDistances={showDistances}
                closure={closure}
              />
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Closure Analysis */}
            {closure && (
              <ClosureReport closure={closure} />
            )}

            {/* Coordinate Table */}
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Coordinates ({coordinates.length} points)
              </h3>
              <div className="max-h-96 overflow-y-auto scrollbar-thin">
                <div className="space-y-2">
                  {coordinates.map((coord, index) => (
                    <div key={index} className="border border-gray-200 rounded p-3 text-sm">
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-medium">{coord.label}</span>
                        {coord.monument && (
                          <span className="text-xs bg-gray-100 px-2 py-1 rounded">
                            {coord.monument}
                          </span>
                        )}
                      </div>
                      <div className="grid grid-cols-2 gap-2 text-xs text-gray-600">
                        <div>X: {coord.x.toFixed(3)}</div>
                        <div>Y: {coord.y.toFixed(3)}</div>
                      </div>
                      {coord.bearing && coord.distance && (
                        <div className="text-xs text-gray-500 mt-1">
                          {coord.bearing} • {coord.distance} {coord.units || 'ft'}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Stats */}
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Plot Statistics</h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Total Points:</span>
                  <span className="text-sm font-medium">{coordinates.length}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Perimeter:</span>
                  <span className="text-sm font-medium">
                    {closure?.perimeter_feet?.toFixed(1)} ft
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Area:</span>
                  <span className="text-sm font-medium">
                    {closure?.area_acres?.toFixed(3)} acres
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Precision:</span>
                  <span className="text-sm font-medium">
                    {closure?.precision_ratio}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PlottingPage; 