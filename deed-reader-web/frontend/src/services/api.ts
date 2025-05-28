import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5000/api',
  timeout: 120000, // 2 minutes for large files and AI processing
  headers: {
    'Content-Type': 'application/json',
  },
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    // Add more detailed error logging
    if (error.response) {
      console.error('Response Error:', error.response.status, error.response.data);
    } else if (error.request) {
      console.error('Request Error:', error.request);
    } else {
      console.error('Error:', error.message);
    }
    return Promise.reject(error);
  }
);

// Types
export interface DocumentData {
  success: boolean;
  filename?: string;
  file_type?: string;
  text_length: number;
  extracted_text: string;
  upload_id: string;
  message: string;
}

export interface AnalysisResult {
  success: boolean;
  analysis: {
    summary: string;
    property_description: {
      legal_description: string;
      acres: string;
      lot_block: string;
      subdivision: string;
    };
    parties: {
      grantor: string;
      grantee: string;
    };
    metes_and_bounds: Array<{
      call_number: number;
      bearing: string;
      distance: string;
      description: string;
    }>;
    monuments: Array<{
      type: string;
      description: string;
      action: string;
    }>;
    dates: {
      deed_date: string;
      recording_date: string;
    };
    references: {
      book_page: string;
      deed_book: string;
      plat_references: string;
    };
    key_findings: string[];
    confidence_score: number;
    parsing_notes: string;
  };
  message: string;
}

export interface ChatResponse {
  success: boolean;
  question: string;
  answer: string;
  session_id: string;
  exchange_count: number;
  message: string;
}

export interface ChatHistory {
  success: boolean;
  session_id: string;
  history: Array<{
    question: string;
    answer: string;
    timestamp?: string;
  }>;
  exchange_count: number;
  message: string;
}

// Document APIs
export const uploadDocument = async (file: File): Promise<DocumentData> => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post('/documents/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export const processText = async (text: string): Promise<DocumentData> => {
  const response = await api.post('/documents/text', { text });
  return response.data;
};

export const validateDocument = async (text: string) => {
  const response = await api.post('/documents/validate', { text });
  return response.data;
};

// Analysis APIs
export const analyzeDocument = async (text: string): Promise<AnalysisResult> => {
  const response = await api.post('/analysis/analyze', { text });
  return response.data;
};

export const generateSummary = async (text: string) => {
  const response = await api.post('/analysis/summary', { text });
  return response.data;
};

export const extractCoordinates = async (text: string) => {
  const response = await api.post('/analysis/coordinates', { text });
  return response.data;
};

export const validateAnalysis = async (extractedData: any) => {
  const response = await api.post('/analysis/validate', { extracted_data: extractedData });
  return response.data;
};

export const parseDeedLegacy = async (text: string) => {
  const response = await api.post('/analysis/parse', { text });
  return response.data;
};

export const compareAnalysis = async (text: string) => {
  const response = await api.post('/analysis/compare', { text });
  return response.data;
};

// Chat APIs
export const askQuestion = async (
  question: string,
  documentText: string,
  sessionId: string = 'default'
): Promise<ChatResponse> => {
  const response = await api.post('/chat/ask', {
    question,
    document_text: documentText,
    session_id: sessionId,
  });
  return response.data;
};

export const getChatHistory = async (sessionId: string): Promise<ChatHistory> => {
  const response = await api.get(`/chat/history/${sessionId}`);
  return response.data;
};

export const clearChatHistory = async (sessionId: string) => {
  const response = await api.delete(`/chat/clear/${sessionId}`);
  return response.data;
};

export const getChatSessions = async () => {
  const response = await api.get('/chat/sessions');
  return response.data;
};

export const getQuestionSuggestions = async (documentText: string) => {
  const response = await api.post('/chat/suggestions', { document_text: documentText });
  return response.data;
};

export const explainTerm = async (term: string, documentText?: string) => {
  const response = await api.post('/chat/explain', { 
    term, 
    document_text: documentText 
  });
  return response.data;
};

// Plotting APIs
export const plotDeed = async (text: string): Promise<any> => {
  const response = await api.post('/plotting/plot', { text });
  return response.data;
};

export const getCoordinates = async (text: string): Promise<any> => {
  const response = await api.post('/plotting/coordinates', { text });
  return response.data;
};

export const analyzeClosure = async (coordinates: any[]): Promise<any> => {
  const response = await api.post('/plotting/closure', { coordinates });
  return response.data;
};

export const exportPlotData = async (formatType: string, coordinates: any[]): Promise<Blob> => {
  const response = await api.post(`/plotting/export/${formatType}`, { coordinates }, {
    responseType: 'blob'
  });
  return response.data;
};

export const exportAllFormats = async (coordinates: any[]): Promise<Blob> => {
  const response = await api.post('/plotting/export/all', { coordinates }, {
    responseType: 'blob'
  });
  return response.data;
};

export const validatePlot = async (text: string): Promise<any> => {
  const response = await api.post('/plotting/validate', { text });
  return response.data;
};

export const transformCoordinates = async (coordinates: any[], fromSystem: string, toSystem: string): Promise<any> => {
  const response = await api.post('/plotting/transform', { 
    coordinates, 
    from_system: fromSystem, 
    to_system: toSystem 
  });
  return response.data;
};

// Health check
export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api; 