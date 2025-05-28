/**
 * TypeScript type definitions
 */

export interface DeedAnalysis {
  id: string;
  filename: string;
  uploadDate: string;
  status: 'processing' | 'completed' | 'error';
  parties?: {
    grantor: string[];
    grantee: string[];
  };
  propertyDescription?: string;
  metesAndBounds?: string[];
  monuments?: string[];
  legalDescription?: string;
  confidence?: number;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}

export interface FileUploadResponse {
  fileId: string;
  filename: string;
  size: number;
  type: string;
}