import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import { useDropzone } from 'react-dropzone';
import toast from 'react-hot-toast';
import { Upload, FileText, Zap, MessageCircle, BarChart3, CheckCircle, Map } from 'lucide-react';
import { uploadDocument, processText } from '../services/api';

const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const [documentText, setDocumentText] = useState('');
  const [showTextInput, setShowTextInput] = useState(false);
  const [processedDocument, setProcessedDocument] = useState<any>(null);

  // File upload mutation
  const uploadMutation = useMutation({
    mutationFn: uploadDocument,
    onSuccess: (data) => {
      toast.success('Document uploaded successfully!');
      setProcessedDocument(data);
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.message || 'Upload failed');
    },
  });

  // Text processing mutation
  const textMutation = useMutation({
    mutationFn: processText,
    onSuccess: (data) => {
      toast.success('Text processed successfully!');
      setProcessedDocument(data);
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.message || 'Text processing failed');
    },
  });

  const onDrop = (acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      uploadMutation.mutate(file);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/plain': ['.txt'],
      'application/pdf': ['.pdf'],
      'image/*': ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']
    },
    multiple: false,
    maxSize: 50 * 1024 * 1024, // 50MB
  });

  const handleTextSubmit = () => {
    if (documentText.trim()) {
      textMutation.mutate(documentText);
    } else {
      toast.error('Please enter some text');
    }
  };

  const isLoading = uploadMutation.isPending || textMutation.isPending;

  return (
    <div className="max-w-6xl mx-auto">
      {/* Hero Section */}
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Deed Reader Pro
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          AI-powered deed document analysis for surveyors and professionals
        </p>
        
        {/* Feature Pills */}
        <div className="flex flex-wrap justify-center gap-3 mb-8">
          <div className="flex items-center gap-2 bg-primary-100 text-primary-800 px-4 py-2 rounded-full text-sm">
            <Zap size={16} />
            AI Analysis
          </div>
          <div className="flex items-center gap-2 bg-surveyor-100 text-surveyor-800 px-4 py-2 rounded-full text-sm">
            <Map size={16} />
            Deed Plotting
          </div>
          <div className="flex items-center gap-2 bg-green-100 text-green-800 px-4 py-2 rounded-full text-sm">
            <BarChart3 size={16} />
            Smart Parsing
          </div>
        </div>
      </div>

      {/* Upload Section */}
      <div className="grid lg:grid-cols-2 gap-8 mb-12">
        {/* File Upload */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Upload Document
          </h2>
          
          <div
            {...getRootProps()}
            className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
              isDragActive
                ? 'border-primary-500 bg-primary-50'
                : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
            } ${isLoading ? 'opacity-50 pointer-events-none' : ''}`}
          >
            <input {...getInputProps()} />
            
            {isLoading ? (
              <div className="flex flex-col items-center">
                <div className="loading-dots">
                  <div></div>
                  <div></div>
                  <div></div>
                  <div></div>
                </div>
                <p className="text-gray-600 mt-4">Processing document...</p>
              </div>
            ) : (
              <div className="flex flex-col items-center">
                <Upload className="h-12 w-12 text-gray-400 mb-4" />
                <p className="text-lg font-medium text-gray-900 mb-2">
                  {isDragActive
                    ? 'Drop your deed document here'
                    : 'Drag & drop your deed document'}
                </p>
                <p className="text-sm text-gray-500 mb-4">
                  or click to browse files
                </p>
                <p className="text-xs text-gray-400">
                  Supports: PDF, TXT, PNG, JPG, TIFF (max 50MB)
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Text Input */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Paste Text
          </h2>
          
          {!showTextInput ? (
            <div 
              className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center cursor-pointer hover:border-primary-400 hover:bg-gray-50 transition-colors"
              onClick={() => setShowTextInput(true)}
            >
              <FileText className="h-12 w-12 text-gray-400 mb-4 mx-auto" />
              <p className="text-lg font-medium text-gray-900 mb-2">
                Paste deed text directly
              </p>
              <p className="text-sm text-gray-500">
                Copy and paste your deed document text
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              <textarea
                value={documentText}
                onChange={(e) => setDocumentText(e.target.value)}
                placeholder="Paste your deed document text here..."
                className="input min-h-[200px] resize-none"
                disabled={isLoading}
              />
              <div className="flex gap-3">
                <button
                  onClick={handleTextSubmit}
                  disabled={isLoading || !documentText.trim()}
                  className="btn-primary flex-1"
                >
                  {isLoading ? 'Processing...' : 'Analyze Text'}
                </button>
                <button
                  onClick={() => {
                    setShowTextInput(false);
                    setDocumentText('');
                  }}
                  className="btn-secondary"
                  disabled={isLoading}
                >
                  Cancel
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Action Buttons - Shown after document processing */}
      {processedDocument && (
        <div className="card mb-12 bg-gradient-to-r from-green-50 to-primary-50 border-green-200">
          <div className="flex items-center gap-4 mb-6">
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <CheckCircle className="h-6 w-6 text-green-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">
                Document Ready!
              </h3>
              <p className="text-sm text-gray-600">
                {processedDocument.filename || 'Text input'} • {processedDocument.text_length?.toLocaleString()} characters
              </p>
            </div>
          </div>
          
          <div className="flex flex-wrap gap-4">
            <button
              onClick={() => navigate('/analysis', { state: { documentData: processedDocument } })}
              className="btn-primary flex items-center gap-2"
            >
              <BarChart3 size={16} />
              Analyze Document
            </button>
            <button
              onClick={() => navigate('/plotting', { state: { documentData: processedDocument } })}
              className="btn-secondary flex items-center gap-2"
            >
              <Map size={16} />
              Plot Deed
            </button>
            <button
              onClick={() => navigate('/chat', { state: { documentData: processedDocument } })}
              className="btn-secondary flex items-center gap-2"
            >
              <MessageCircle size={16} />
              Ask Questions
            </button>
            <button
              onClick={() => setProcessedDocument(null)}
              className="btn-ghost"
            >
              Upload Another
            </button>
          </div>
        </div>
      )}

      {/* Features Section */}
      <div className="grid md:grid-cols-3 gap-6 mb-12">
        <div className="card text-center">
          <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-4">
            <Zap className="h-6 w-6 text-primary-600" />
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            AI-Powered Analysis
          </h3>
          <p className="text-gray-600 text-sm">
            Extract key information, bearings, distances, and legal descriptions using advanced AI
          </p>
        </div>

        <div className="card text-center">
          <div className="w-12 h-12 bg-surveyor-100 rounded-lg flex items-center justify-center mx-auto mb-4">
            <Map className="h-6 w-6 text-surveyor-600" />
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Interactive Plotting
          </h3>
          <p className="text-gray-600 text-sm">
            Plot deed coordinates with AI-powered metes and bounds analysis and closure reports
          </p>
        </div>

        <div className="card text-center">
          <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-4">
            <CheckCircle className="h-6 w-6 text-green-600" />
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Professional Grade
          </h3>
          <p className="text-gray-600 text-sm">
            Built for surveyors with accurate parsing and professional validation
          </p>
        </div>
      </div>

      {/* Quick Start Tips */}
      <div className="card bg-gradient-to-r from-primary-50 to-surveyor-50 border-primary-200">
        <h3 className="text-lg font-semibold text-gray-900 mb-3">
          Quick Start Tips
        </h3>
        <ul className="space-y-2 text-sm text-gray-700">
          <li className="flex items-start gap-2">
            <CheckCircle size={16} className="text-primary-600 mt-0.5 flex-shrink-0" />
            Upload a PDF or image of your deed document for automatic text extraction
          </li>
          <li className="flex items-start gap-2">
            <CheckCircle size={16} className="text-primary-600 mt-0.5 flex-shrink-0" />
            For best results, ensure the document contains metes and bounds descriptions
          </li>
          <li className="flex items-start gap-2">
            <CheckCircle size={16} className="text-primary-600 mt-0.5 flex-shrink-0" />
            Use the chat feature to ask specific questions about property boundaries
          </li>
        </ul>
      </div>
    </div>
  );
};

export default HomePage; 