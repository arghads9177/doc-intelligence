import { ExtractedFinancial, ExtractedContract } from './extraction';
import { ValidationReport } from './validation';

/**
 * Processed document result
 */
export interface ProcessedDocument {
  filename: string;
  doc_type: string;
  doc_type_confidence: number;
  extracted_fields?: ExtractedFinancial | ExtractedContract;
  validation_report?: ValidationReport;
  summary?: string;
  raw_text_preview?: string;
}

/**
 * Complete API response from /api/analyze
 */
export interface AnalyzeResponse {
  status: 'success' | 'error' | 'partial_success';
  message: string;
  processed_documents: ProcessedDocument[];
  total_processed: number;
  total_errors: number;
  processing_time_seconds: number;
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
