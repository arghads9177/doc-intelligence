import { ProcessingStatus, DocumentType } from './enums';

/**
 * Represents a single uploaded document
 */
export interface Document {
  id: string;
  filename: string;
  contentType: string;
  fileSize: number;
  uploadedAt: Date;
  processingStatus: ProcessingStatus;
  documentType?: DocumentType;
  documentTypeConfidence?: number;
  rawTextPreview?: string;
  error?: string;
}

/**
 * Request model for document upload and analysis
 */
export interface AnalyzeRequest {
  documents: DocumentInput[];
  includeSummary?: boolean;
  includeValidation?: boolean;
}

/**
 * Single document input for API request
 */
export interface DocumentInput {
  filename: string;
  content_type: string;
  file_bytes: string; // Base64 encoded
  metadata?: Record<string, any>;
}

/**
 * Collection of documents for batch processing
 */
export interface DocumentBatch {
  id: string;
  documents: Document[];
  createdAt: Date;
  completedAt?: Date;
  totalDocuments: number;
  processedDocuments: number;
  failedDocuments: number;
}
