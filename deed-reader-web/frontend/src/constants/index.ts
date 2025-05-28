/**
 * Application constants
 */

export const API_ENDPOINTS = {
  UPLOAD: '/documents/upload',
  ANALYZE: '/documents/analyze', 
  CHAT: '/chat',
  HEALTH: '/health',
  PLOTTING: '/plotting/plot'
} as const;

export const FILE_TYPES = {
  PDF: 'application/pdf',
  PNG: 'image/png',
  JPEG: 'image/jpeg',
  JPG: 'image/jpg',
  TIFF: 'image/tiff',
  TEXT: 'text/plain'
} as const;

export const MAX_FILE_SIZE_MB = 50;

export const ROUTES = {
  HOME: '/',
  ANALYSIS: '/analysis',
  CHAT: '/chat',
  PLOTTING: '/plotting',
  SETTINGS: '/settings'
} as const;