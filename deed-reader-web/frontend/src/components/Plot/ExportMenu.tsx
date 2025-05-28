import React, { useState } from 'react';
import { Download, ChevronDown, FileText, Map, Database, Code, Globe } from 'lucide-react';
import { exportPlotData, exportAllFormats } from '../../services/api';
import toast from 'react-hot-toast';

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

interface ExportMenuProps {
  coordinates: Coordinate[];
}

const ExportMenu: React.FC<ExportMenuProps> = ({ coordinates }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isExporting, setIsExporting] = useState(false);

  const exportFormats = [
    {
      id: 'dxf',
      name: 'AutoCAD DXF',
      description: 'CAD drawing format for AutoCAD, Civil3D',
      icon: FileText,
      extension: '.dxf'
    },
    {
      id: 'csv',
      name: 'Coordinate CSV',
      description: 'Spreadsheet with point coordinates',
      icon: Database,
      extension: '.csv'
    },
    {
      id: 'esri_traverse',
      name: 'ESRI Traverse',
      description: 'For ArcGIS Pro and ESRI software',
      icon: Map,
      extension: '.txt'
    },
    {
      id: 'autocad_script',
      name: 'AutoCAD Script',
      description: 'Command script for AutoCAD',
      icon: Code,
      extension: '.scr'
    },
    {
      id: 'kml',
      name: 'Google Earth KML',
      description: 'For Google Earth visualization',
      icon: Globe,
      extension: '.kml'
    }
  ];

  const handleExport = async (formatId: string) => {
    setIsExporting(true);
    try {
      // Create a blob and download the file
      const response = await fetch('/api/plotting/export/' + formatId, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ coordinates }),
      });

      if (!response.ok) {
        throw new Error('Export failed');
      }

      // Get filename from response headers or use default
      const contentDisposition = response.headers.get('content-disposition');
      let filename = `deed_plot.${formatId}`;
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?([^"]+)"?/);
        if (filenameMatch) {
          filename = filenameMatch[1];
        }
      }

      // Create blob and download
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      toast.success(`Exported ${formatId.toUpperCase()} successfully!`);
      setIsOpen(false);
    } catch (error) {
      console.error('Export error:', error);
      toast.error('Export failed. Please try again.');
    } finally {
      setIsExporting(false);
    }
  };

  const handleExportAll = async () => {
    setIsExporting(true);
    try {
      const response = await fetch('/api/plotting/export/all', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ coordinates }),
      });

      if (!response.ok) {
        throw new Error('Export failed');
      }

      // Download the ZIP file
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'deed_plot_exports.zip';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      toast.success('All formats exported successfully!');
      setIsOpen(false);
    } catch (error) {
      console.error('Export all error:', error);
      toast.error('Export failed. Please try again.');
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="btn-primary flex items-center gap-2"
        disabled={isExporting || coordinates.length === 0}
      >
        <Download size={16} />
        Export
        <ChevronDown size={16} className={`transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg border border-gray-200 z-50">
          <div className="p-4">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">Export Plot Data</h3>
            
            {/* Export All Button */}
            <button
              onClick={handleExportAll}
              disabled={isExporting}
              className="w-full mb-3 p-3 border-2 border-dashed border-primary-300 rounded-lg hover:border-primary-500 transition-colors text-center"
            >
              <div className="flex items-center justify-center gap-2 text-primary-600">
                <Download size={20} />
                <span className="font-medium">Download All Formats (ZIP)</span>
              </div>
              <div className="text-xs text-gray-500 mt-1">
                Get all export formats in one download
              </div>
            </button>

            <div className="text-xs text-gray-500 text-center mb-3">
              or choose individual formats:
            </div>

            {/* Individual Format Options */}
            <div className="space-y-2">
              {exportFormats.map((format) => {
                const Icon = format.icon;
                return (
                  <button
                    key={format.id}
                    onClick={() => handleExport(format.id)}
                    disabled={isExporting}
                    className="w-full p-3 text-left hover:bg-gray-50 rounded-lg border border-gray-200 transition-colors"
                  >
                    <div className="flex items-start gap-3">
                      <Icon size={16} className="text-gray-600 mt-0.5 flex-shrink-0" />
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between">
                          <span className="text-sm font-medium text-gray-900">
                            {format.name}
                          </span>
                          <span className="text-xs text-gray-500">
                            {format.extension}
                          </span>
                        </div>
                        <div className="text-xs text-gray-500 mt-1">
                          {format.description}
                        </div>
                      </div>
                    </div>
                  </button>
                );
              })}
            </div>

            {/* Usage Notes */}
            <div className="mt-4 p-3 bg-gray-50 rounded-lg">
              <h4 className="text-xs font-medium text-gray-900 mb-2">Export Notes:</h4>
              <ul className="text-xs text-gray-600 space-y-1">
                <li>• DXF files can be opened in AutoCAD, Civil3D, and most CAD software</li>
                <li>• CSV files work with Excel and GIS applications</li>
                <li>• ESRI Traverse files import directly into ArcGIS Pro</li>
                <li>• Coordinates are in local survey coordinate system</li>
              </ul>
            </div>

            {/* Close Button */}
            <button
              onClick={() => setIsOpen(false)}
              className="w-full mt-3 px-4 py-2 text-sm text-gray-600 hover:text-gray-900 transition-colors"
            >
              Close
            </button>
          </div>
        </div>
      )}

      {/* Overlay to close menu when clicking outside */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40"
          onClick={() => setIsOpen(false)}
        />
      )}
    </div>
  );
};

export default ExportMenu; 