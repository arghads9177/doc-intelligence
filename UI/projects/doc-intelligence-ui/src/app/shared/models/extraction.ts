/**
 * Field value with confidence score
 */
export interface FieldValue<T = any> {
  value: T;
  confidence: number;
  notes?: string;
}

/**
 * Extracted data from financial documents (invoices, receipts)
 */
export interface ExtractedFinancial {
  company?: FieldValue<string>;
  date?: FieldValue<string>;
  totalAmount?: FieldValue<number>;
  currency?: FieldValue<string>;
  items?: FieldValue<LineItem[]>;
  invoiceNumber?: FieldValue<string>;
}

/**
 * Line item in financial document
 */
export interface LineItem {
  description: string;
  amount: number;
  quantity?: number;
  unitPrice?: number;
}

/**
 * Extracted data from contracts
 */
export interface ExtractedContract {
  parties?: FieldValue<string[]>;
  effectiveDate?: FieldValue<string>;
  expirationDate?: FieldValue<string>;
  keyObligations?: FieldValue<Obligation[]>;
  contractType?: FieldValue<string>;
}

/**
 * Contract obligation
 */
export interface Obligation {
  description: string;
  party?: string;
  dueDate?: string;
}

/**
 * Generic extraction result that can hold either financial or contract data
 */
export interface ExtractionResult {
  documentType: string;
  extractedFields: ExtractedFinancial | ExtractedContract;
}
