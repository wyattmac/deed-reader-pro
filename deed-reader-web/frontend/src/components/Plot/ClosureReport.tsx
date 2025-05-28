import React from 'react';
import { CheckCircle, AlertTriangle, AlertCircle, Calculator } from 'lucide-react';

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

interface ClosureReportProps {
  closure: ClosureData;
}

const ClosureReport: React.FC<ClosureReportProps> = ({ closure }) => {
  const getClosureStatus = () => {
    if (closure.is_closed) {
      return {
        icon: CheckCircle,
        color: 'text-green-600',
        bgColor: 'bg-green-50',
        borderColor: 'border-green-200',
        status: 'CLOSED',
        message: 'Plot closes within acceptable tolerance'
      };
    } else if (closure.closure_error_ppm < 5000) { // Better than 1:200
      return {
        icon: AlertTriangle,
        color: 'text-yellow-600',
        bgColor: 'bg-yellow-50',
        borderColor: 'border-yellow-200',
        status: 'ACCEPTABLE',
        message: 'Good closure with minor error'
      };
    } else {
      return {
        icon: AlertCircle,
        color: 'text-red-600',
        bgColor: 'bg-red-50',
        borderColor: 'border-red-200',
        status: 'NEEDS REVIEW',
        message: 'Significant closure error detected'
      };
    }
  };

  const getPrecisionRating = () => {
    const ppm = closure.closure_error_ppm;
    if (ppm < 1000) return { rating: 'Excellent', color: 'text-green-600' };
    if (ppm < 2500) return { rating: 'Very Good', color: 'text-green-500' };
    if (ppm < 5000) return { rating: 'Good', color: 'text-yellow-600' };
    if (ppm < 10000) return { rating: 'Fair', color: 'text-orange-600' };
    return { rating: 'Poor', color: 'text-red-600' };
  };

  const statusInfo = getClosureStatus();
  const precisionInfo = getPrecisionRating();
  const StatusIcon = statusInfo.icon;

  return (
    <div className="card">
      <div className="flex items-center gap-3 mb-4">
        <Calculator className="h-5 w-5 text-primary-600" />
        <h3 className="text-lg font-semibold text-gray-900">Closure Analysis</h3>
      </div>

      {/* Status Banner */}
      <div className={`p-3 rounded-lg border ${statusInfo.bgColor} ${statusInfo.borderColor} mb-4`}>
        <div className="flex items-center gap-2">
          <StatusIcon className={`h-5 w-5 ${statusInfo.color}`} />
          <div>
            <div className={`font-semibold ${statusInfo.color}`}>
              {statusInfo.status}
            </div>
            <div className="text-sm text-gray-600">
              {statusInfo.message}
            </div>
          </div>
        </div>
      </div>

      {/* Closure Metrics */}
      <div className="space-y-4">
        {/* Closure Distance */}
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600">Closure Distance:</span>
          <div className="text-right">
            <span className="text-sm font-medium">
              {closure.closure_distance.toFixed(3)} ft
            </span>
            {!closure.is_closed && (
              <div className="text-xs text-gray-500">
                {closure.closure_bearing}
              </div>
            )}
          </div>
        </div>

        {/* Precision Ratio */}
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600">Precision Ratio:</span>
          <div className="text-right">
            <span className="text-sm font-medium">
              {closure.precision_ratio}
            </span>
            <div className={`text-xs ${precisionInfo.color}`}>
              {precisionInfo.rating}
            </div>
          </div>
        </div>

        {/* Error in PPM */}
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600">Error (PPM):</span>
          <span className={`text-sm font-medium ${precisionInfo.color}`}>
            {closure.closure_error_ppm.toFixed(1)}
          </span>
        </div>

        <hr className="border-gray-200" />

        {/* Area Calculations */}
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600">Total Area:</span>
          <div className="text-right">
            <div className="text-sm font-medium">
              {closure.area_acres.toFixed(3)} acres
            </div>
            <div className="text-xs text-gray-500">
              {closure.area_sq_feet.toLocaleString()} sq ft
            </div>
          </div>
        </div>

        {/* Perimeter */}
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600">Perimeter:</span>
          <span className="text-sm font-medium">
            {closure.perimeter_feet.toFixed(1)} ft
          </span>
        </div>

        {/* Additional Info */}
        <div className="mt-4 p-3 bg-gray-50 rounded-lg">
          <h4 className="text-sm font-medium text-gray-900 mb-2">Survey Notes</h4>
          <ul className="text-xs text-gray-600 space-y-1">
            <li>• Closure tolerance: ±0.10 ft for good surveys</li>
            <li>• Precision better than 1:5000 recommended</li>
            <li>• Area calculated using coordinate method</li>
            {!closure.is_closed && (
              <li className="text-red-600">
                • Review field notes for closure discrepancy
              </li>
            )}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ClosureReport; 