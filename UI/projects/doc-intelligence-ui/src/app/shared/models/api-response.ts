import { ExtractedFinancial, ExtractedContract } from './extraction';
import { ValidationReport } from './validation';

/**
 * Processed document result
 */
export interface ProcessedDocument {
  filename: string;
  docType: string;
  docTypeConfidence: number;
  extractedFields?: ExtractedFinancial | ExtractedContract;
  validationReport?: ValidationReport;
  summary?: string;
  rawTextPreview?: string;
}

/**
 * Complete API response from /api/analyze
 */
export interface AnalyzeResponse {
  status: 'success' | 'error';
  message: string;
  processedDocuments: ProcessedDocument[];
  totalProcessed: number;
  totalErrors: number;
  processingTimeSecs: number;
}

/**
 * API error response
 */
export interface ApiError {
  status: number;
  message: string;
  error?: string;
  details?: Record<string, any>;
}

/**
 * Health check response
 */
export interface HealthCheckResponse {
  status: 'healthy' | 'degraded' | 'unhealthy';
  service: string;
  timestamp: number;
  version?: string;
}
