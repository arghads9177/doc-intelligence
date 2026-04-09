import { TestBed } from '@angular/core/testing';
import { DocumentService } from './document.service';

describe('DocumentService', () => {
  let service: DocumentService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [DocumentService]
    });
    service = TestBed.inject(DocumentService);
    localStorage.clear();
  });

  afterEach(() => {
    localStorage.clear();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('Document State Management', () => {
    it('should initialize with empty documents', (done) => {
      service.documents$.subscribe(docs => {
        expect(docs).toBeDefined();
        done();
      });
    });

    it('should set current document', (done) => {
      const mockDoc = { id: '1', name: 'test.pdf', type: 'invoice' };
      
      service.setCurrentDocument(mockDoc);
      
      service.currentDocument$.subscribe(doc => {
        expect(doc).toEqual(mockDoc);
        done();
      });
    });

    it('should update processing status', (done) => {
      service.setProcessingStatus('processing');
      
      service.processingStatus$.subscribe(status => {
        expect(status).toBe('processing');
        done();
      });
    });

    it('should add document to history', (done) => {
      const mockDoc = {
        id: '1',
        name: 'invoice.pdf',
        type: 'invoice',
        date: new Date(),
        status: 'completed'
      };

      service.addToHistory(mockDoc);

      service.documentHistory$.subscribe(history => {
        expect(history.length).toBeGreaterThan(0);
        expect(history[history.length - 1]).toEqual(mockDoc);
        done();
      });
    });
  });

  describe('Local Storage Persistence', () => {
    it('should persist history to localStorage', () => {
      const mockDoc = {
        id: '1',
        name: 'test.pdf',
        type: 'invoice',
        date: new Date(),
        status: 'completed'
      };

      service.addToHistory(mockDoc);

      const stored = localStorage.getItem('document_history');
      expect(stored).toBeTruthy();
    });

    it('should load history from localStorage on initialization', () => {
      const mockHistory = [
        {
          id: '1',
          name: 'test1.pdf',
          type: 'invoice',
          date: new Date().toISOString(),
          status: 'completed'
        }
      ];

      localStorage.setItem('document_history', JSON.stringify(mockHistory));

      const newService = new DocumentService();
      newService.documentHistory$.subscribe(history => {
        expect(history.length).toBeGreaterThan(0);
      });
    });

    it('should limit history to 50 items', () => {
      for (let i = 0; i < 60; i++) {
        service.addToHistory({
          id: i.toString(),
          name: `doc${i}.pdf`,
          type: 'invoice',
          date: new Date(),
          status: 'completed'
        });
      }

      service.documentHistory$.subscribe(history => {
        expect(history.length).toBeLessThanOrEqual(50);
      });
    });
  });

  describe('Observable Subscriptions', () => {
    it('should emit new values on currentDocument$ changes', (done) => {
      const docs = [
        { id: '1', name: 'doc1.pdf', type: 'invoice' },
        { id: '2', name: 'doc2.pdf', type: 'receipt' }
      ];

      let emissionCount = 0;
      service.currentDocument$.subscribe(doc => {
        emissionCount++;
      });

      docs.forEach(doc => service.setCurrentDocument(doc));

      setTimeout(() => {
        expect(emissionCount).toBeGreaterThan(0);
        done();
      }, 100);
    });

    it('should handle multiple subscribers', (done) => {
      const mockDoc = { id: '1', name: 'test.pdf', type: 'invoice' };
      
      let subscriber1Value: any;
      let subscriber2Value: any;

      service.currentDocument$.subscribe(doc => {
        subscriber1Value = doc;
      });

      service.currentDocument$.subscribe(doc => {
        subscriber2Value = doc;
      });

      service.setCurrentDocument(mockDoc);

      setTimeout(() => {
        expect(subscriber1Value).toEqual(mockDoc);
        expect(subscriber2Value).toEqual(mockDoc);
        done();
      }, 100);
    });
  });

  describe('Error Handling', () => {
    it('should handle null documents gracefully', () => {
      expect(() => {
        service.setCurrentDocument(null);
      }).not.toThrow();
    });

    it('should handle corrupted localStorage data', () => {
      localStorage.setItem('document_history', 'invalid json');
      const newService = new DocumentService();
      expect(newService).toBeTruthy();
    });
  });
});
