import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import toast from 'react-hot-toast';
import { BarChart3, Download, RefreshCw, CheckCircle, AlertCircle, Map } from 'lucide-react';
import { analyzeDocument, type DocumentData, type AnalysisResult } from '../services/api';

const AnalysisPage: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [documentData, setDocumentData] = useState<DocumentData | null>(null);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);

  // Get document data from navigation state
  useEffect(() => {
    if (location.state?.documentData) {
      setDocumentData(location.state.documentData);
    }
  }, [location.state]);

  // Analysis mutation
  const analysisMutation = useMutation({
    mutationFn: analyzeDocument,
    onSuccess: (data) => {
      setAnalysisResult(data);
      toast.success('Analysis completed successfully!');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.message || 'Analysis failed');
    },
  });

  // Auto-analyze when document is available
  useEffect(() => {
    if (documentData && !analysisResult && !analysisMutation.isPending) {
      analysisMutation.mutate(documentData.extracted_text);
    }
  }, [documentData, analysisResult, analysisMutation]);

  const handleReanalyze = () => {
    if (documentData) {
      analysisMutation.mutate(documentData.extracted_text);
    }
  };

  const handlePlotDeed = () => {
    if (documentData) {
      navigate('/plotting', { state: { documentData } });
    }
  };

  if (!documentData) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="card text-center py-12">
          <BarChart3 className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">
            No Document to Analyze
          </h2>
          <p className="text-gray-600">
            Please upload a document from the home page to start analysis.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Document Analysis</h1>
          <p className="text-gray-600 mt-2">
            AI-powered analysis of your deed document
          </p>
        </div>
        
        <div className="flex gap-3">
          <button
            onClick={handleReanalyze}
            disabled={analysisMutation.isPending}
            className="btn-secondary"
          >
            <RefreshCw size={16} className={analysisMutation.isPending ? 'animate-spin' : ''} />
            Re-analyze
          </button>
          <button
            onClick={handlePlotDeed}
            className="btn-secondary"
          >
            <Map size={16} />
            Plot Deed
          </button>
          <button className="btn-primary">
            <Download size={16} />
            Export Results
          </button>
        </div>
      </div>

      {/* Document Info */}
      <div className="card mb-8">
        <div className="flex items-center gap-4 mb-4">
          <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
            <BarChart3 className="h-6 w-6 text-primary-600" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">
              {documentData.filename || 'Text Input'}
            </h3>
            <p className="text-sm text-gray-500">
              {documentData.text_length.toLocaleString()} characters • 
              {documentData.file_type || 'text'} format
            </p>
          </div>
        </div>
      </div>

      {/* Analysis Results */}
      {analysisMutation.isPending && (
        <div className="card text-center py-12">
          <div className="loading-dots mx-auto mb-4">
            <div></div>
            <div></div>
            <div></div>
            <div></div>
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Analyzing Document...
          </h3>
          <p className="text-gray-600">
            AI is processing your deed document. This may take a moment.
          </p>
        </div>
      )}

      {analysisResult && (
        <div className="space-y-6">
          {/* Summary */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Summary</h3>
            <p className="text-gray-700 leading-relaxed">
              {analysisResult.analysis.summary}
            </p>
          </div>

          {/* Parties */}
          <div className="grid md:grid-cols-2 gap-6">
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Parties</h3>
              <div className="space-y-3">
                <div>
                  <label className="text-sm font-medium text-gray-600">Grantor</label>
                  <p className="text-gray-900">{analysisResult.analysis.parties.grantor || 'Not specified'}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600">Grantee</label>
                  <p className="text-gray-900">{analysisResult.analysis.parties.grantee || 'Not specified'}</p>
                </div>
              </div>
            </div>

            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Property Description</h3>
              <div className="space-y-3">
                <div>
                  <label className="text-sm font-medium text-gray-600">Acres</label>
                  <p className="text-gray-900">{analysisResult.analysis.property_description.acres || 'Not specified'}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600">Legal Description</label>
                  <p className="text-gray-900 text-sm">{analysisResult.analysis.property_description.legal_description || 'Not specified'}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Metes and Bounds */}
          {analysisResult.analysis.metes_and_bounds && analysisResult.analysis.metes_and_bounds.length > 0 && (
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Metes and Bounds</h3>
              <div className="space-y-4">
                {analysisResult.analysis.metes_and_bounds.map((call, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-start gap-3">
                      <div className="w-8 h-8 bg-surveyor-100 rounded-full flex items-center justify-center text-sm font-medium text-surveyor-600">
                        {call.call_number || index + 1}
                      </div>
                      <div className="flex-1">
                        <div className="grid md:grid-cols-2 gap-4">
                          <div>
                            <label className="text-xs font-medium text-gray-600">Bearing</label>
                            <p className="text-gray-900 font-mono">{call.bearing || 'N/A'}</p>
                          </div>
                          <div>
                            <label className="text-xs font-medium text-gray-600">Distance</label>
                            <p className="text-gray-900 font-mono">{call.distance || 'N/A'}</p>
                          </div>
                        </div>
                        <div className="mt-2">
                          <label className="text-xs font-medium text-gray-600">Description</label>
                          <p className="text-gray-700 text-sm">{call.description}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Confidence and Quality */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Analysis Quality</h3>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                {analysisResult.analysis.confidence_score >= 0.8 ? (
                  <CheckCircle className="h-5 w-5 text-green-600" />
                ) : (
                  <AlertCircle className="h-5 w-5 text-yellow-600" />
                )}
                <span className="text-sm font-medium text-gray-700">
                  Confidence: {Math.round(analysisResult.analysis.confidence_score * 100)}%
                </span>
              </div>
              <div className="flex-1 bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${analysisResult.analysis.confidence_score * 100}%` }}
                />
              </div>
            </div>
            {analysisResult.analysis.parsing_notes && (
              <div className="mt-4 p-3 bg-gray-50 rounded-lg">
                <p className="text-sm text-gray-700">{analysisResult.analysis.parsing_notes}</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default AnalysisPage; 