import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { ApiService } from './api.service';

describe('ApiService', () => {
  let service: ApiService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [ApiService]
    });
    service = TestBed.inject(ApiService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('analyzeDocuments', () => {
    it('should send POST request with form data', () => {
      const mockFiles = [
        new File(['content1'], 'test1.pdf', { type: 'application/pdf' }),
        new File(['content2'], 'test2.pdf', { type: 'application/pdf' })
      ];

      service.analyzeDocuments(mockFiles).subscribe(response => {
        expect(response).toBeDefined();
      });

      const req = httpMock.expectOne('http://localhost:8000/api/analyze');
      expect(req.request.method).toBe('POST');
      req.flush({ success: true, results: [] });
    });

    it('should handle file conversion errors', () => {
      const invalidFiles = [];
      expect(() => {
        service.analyzeDocuments(invalidFiles);
      }).not.toThrow();
    });
  });

  describe('healthCheck', () => {
    it('should make GET request to health endpoint', () => {
      service.healthCheck().subscribe(response => {
        expect(response.status).toBe('healthy');
      });

      const req = httpMock.expectOne('http://localhost:8000/api/health');
      expect(req.request.method).toBe('GET');
      req.flush({ status: 'healthy' });
    });

    it('should handle health check failures', () => {
      service.healthCheck().subscribe(
        () => {},
        error => {
          expect(error).toBeDefined();
        }
      );

      const req = httpMock.expectOne('http://localhost:8000/api/health');
      req.error(new ErrorEvent('Network error'));
    });
  });

  describe('fileToBase64', () => {
    it('should convert file to base64 string', (done) => {
      const file = new File(['test content'], 'test.txt', { type: 'text/plain' });
      
      service.fileToBase64(file).then(base64 => {
        expect(base64).toContain('data:text/plain;base64');
        done();
      }).catch(error => {
        fail('Should not error: ' + error);
      });
    });

    it('should handle invalid file', (done) => {
      const file = null as any;
      
      service.fileToBase64(file).catch(error => {
        expect(error).toBeDefined();
        done();
      });
    });
  });

  describe('error handling', () => {
    it('should log and rethrow errors', () => {
      const errorResponse = { status: 500, message: 'Server error' };
      
      service.analyzeDocuments([new File(['test'], 'test.pdf')]).subscribe(
        () => {},
        error => {
          expect(error).toBeDefined();
        }
      );

      const req = httpMock.expectOne('http://localhost:8000/api/analyze');
      req.flush(errorResponse, { status: 500, statusText: 'Server Error' });
    });
  });
});
