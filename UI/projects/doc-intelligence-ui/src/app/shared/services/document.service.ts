import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { Document, DocumentBatch, ProcessingStatus, DocumentType } from '../models';

@Injectable({
  providedIn: 'root'
})
export class DocumentService {
  // State management
  private currentDocumentSubject = new BehaviorSubject<Document | null>(null);
  private documentsSubject = new BehaviorSubject<Document[]>([]);
  private processingStatusSubject = new BehaviorSubject<ProcessingStatus>(ProcessingStatus.PENDING);
  private documentHistorySubject = new BehaviorSubject<DocumentBatch[]>([]);

  // Public observables
  currentDocument$ = this.currentDocumentSubject.asObservable();
  documents$ = this.documentsSubject.asObservable();
  processingStatus$ = this.processingStatusSubject.asObservable();
  documentHistory$ = this.documentHistorySubject.asObservable();

  // Local storage key
  private readonly HISTORY_STORAGE_KEY = 'doc_intelligence_history';
  private readonly MAX_HISTORY_ITEMS = 50;

  constructor() {
    this.loadHistoryFromStorage();
  }

  /**
   * Add document to current batch
   */
  addDocument(filename: string, fileSize: number, contentType: string): Document {
    const doc: Document = {
      id: this.generateUUID(),
      filename,
      contentType,
      fileSize,
      uploadedAt: new Date(),
      processingStatus: ProcessingStatus.PENDING,
      documentType: DocumentType.UNKNOWN
    };

    const current = this.documentsSubject.value;
    this.documentsSubject.next([...current, doc]);
    this.setCurrentDocument(doc);

    return doc;
  }

  /**
   * Remove document from batch
   */
  removeDocument(documentId: string): void {
    const current = this.documentsSubject.value.filter((d) => d.id !== documentId);
    this.documentsSubject.next(current);

    if (this.currentDocumentSubject.value?.id === documentId) {
      this.setCurrentDocument(current[0] || null);
    }
  }

  /**
   * Clear all documents in current batch
   */
  clearDocuments(): void {
    this.documentsSubject.next([]);
    this.currentDocumentSubject.next(null);
    this.processingStatusSubject.next(ProcessingStatus.PENDING);
  }

  /**
   * Set current document being viewed
   */
  setCurrentDocument(doc: Document | null): void {
    this.currentDocumentSubject.next(doc);
  }

  /**
   * Update document with processing results
   */
  updateDocument(documentId: string, updates: Partial<Document>): void {
    const current = this.documentsSubject.value;
    const updated = current.map((d) =>
      d.id === documentId ? { ...d, ...updates } : d
    );
    this.documentsSubject.next(updated);

    if (this.currentDocumentSubject.value?.id === documentId) {
      this.currentDocumentSubject.next(updated.find((d) => d.id === documentId) || null);
    }
  }

  /**
   * Update processing status
   */
  setProcessingStatus(status: ProcessingStatus): void {
    this.processingStatusSubject.next(status);
  }

  /**
   * Add batch to history
   */
  addToHistory(batch: DocumentBatch): void {
    const current = this.documentHistorySubject.value;
    const updated = [batch, ...current].slice(0, this.MAX_HISTORY_ITEMS);
    this.documentHistorySubject.next(updated);
    this.saveHistoryToStorage(updated);
  }

  /**
   * Get document from history
   */
  getHistoryItem(batchId: string): DocumentBatch | undefined {
    return this.documentHistorySubject.value.find((b) => b.id === batchId);
  }

  /**
   * Delete history item
   */
  deleteHistoryItem(batchId: string): void {
    const current = this.documentHistorySubject.value.filter((b) => b.id !== batchId);
    this.documentHistorySubject.next(current);
    this.saveHistoryToStorage(current);
  }

  /**
   * Clear entire history
   */
  clearHistory(): void {
    this.documentHistorySubject.next([]);
    localStorage.removeItem(this.HISTORY_STORAGE_KEY);
  }

  /**
   * Save history to local storage
   */
  private saveHistoryToStorage(history: DocumentBatch[]): void {
    try {
      const serialized = JSON.stringify(history);
      localStorage.setItem(this.HISTORY_STORAGE_KEY, serialized);
    } catch (error) {
      console.error('Failed to save history to storage:', error);
    }
  }

  /**
   * Load history from local storage
   */
  private loadHistoryFromStorage(): void {
    try {
      const stored = localStorage.getItem(this.HISTORY_STORAGE_KEY);
      if (stored) {
        const history = JSON.parse(stored) as DocumentBatch[];
        // Convert date strings back to Date objects
        const normalized = history.map((b) => ({
          ...b,
          createdAt: new Date(b.createdAt),
          completedAt: b.completedAt ? new Date(b.completedAt) : undefined
        }));
        this.documentHistorySubject.next(normalized);
      }
    } catch (error) {
      console.error('Failed to load history from storage:', error);
    }
  }

  /**
   * Generate unique batch ID
   */
  generateBatchId(): string {
    return this.generateUUID();
  }

  /**
   * Generate UUID v4 string
   */
  private generateUUID(): string {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
      const r = (Math.random() * 16) | 0;
      const v = c === 'x' ? r : (r & 0x3) | 0x8;
      return v.toString(16);
    });
  }
}
