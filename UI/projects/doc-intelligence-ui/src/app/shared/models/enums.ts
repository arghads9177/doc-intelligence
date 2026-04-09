/**
 * Processing Status Enum
 * Represents the current state of document processing
 */
export enum ProcessingStatus {
  PENDING = 'pending',
  INGESTING = 'ingesting',
  CLASSIFYING = 'classifying',
  EXTRACTING = 'extracting',
  VALIDATING = 'validating',
  SUMMARIZING = 'summarizing',
  COMPLETE = 'complete',
  ERROR = 'error'
}

/**
 * Document Type
 * Supported document types
 */
export enum DocumentType {
  INVOICE = 'invoice',
  RECEIPT = 'receipt',
  CONTRACT = 'contract',
  UNKNOWN = 'unknown'
}
