# API Integration Guide

## Backend Connection Overview

The Document Intelligence UI connects to a FastAPI backend running on `http://localhost:8000`.

## Configuration

### Environment Setup

**Development** (`src/environments/environment.ts`):
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000'
};
```

**Production** (`src/environments/environment.prod.ts`):
```typescript
export const environment = {
  production: true,
  apiUrl: 'https://api.yourdomain.com'
};
```

### Proxy Configuration

For local development, the app uses a proxy to avoid CORS issues. This is configured in `proxy.conf.json`:

```json
{
  "/api": {
    "target": "http://localhost:8000",
    "secure": false,
    "changeOrigin": true,
    "pathRewrite": {
      "^/api": "/api"
    }
  }
}
```

## API Service Usage

### 1. Analyze Documents

Upload one or more documents for processing:

```typescript
import { ApiService } from './shared/services/api.service';

constructor(private api: ApiService) {}

uploadDocuments(files: File[]) {
  this.api.analyzeDocuments(files).subscribe(
    response => {
      console.log('Analysis complete:', response);
      // Handle results
    },
    error => {
      console.error('Analysis failed:', error);
      // Handle error
    }
  );
}
```

**Request:**
- Method: `POST`
- Endpoint: `/api/analyze`
- Body: FormData with file(s)

**Response:**
```json
{
  "batch_id": "uuid",
  "documents": [
    {
      "document_id": "uuid",
      "file_name": "invoice.pdf",
      "classification": {
        "type": "invoice",
        "confidence": 0.95
      },
      "extraction": {
        "company": "Acme Inc",
        "amount": "1500.00",
        "confidence": 0.92
      },
      "validation": {
        "score": 0.88,
        "issues": []
      },
      "summary": "Invoice from Acme Inc..."
    }
  ]
}
```

### 2. Health Check

Verify backend connectivity:

```typescript
this.api.healthCheck().subscribe(
  response => console.log('Backend healthy:', response.status),
  error => console.error('Backend unavailable:', error)
);
```

**Request:**
- Method: `GET`
- Endpoint: `/api/health`

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-04-09T10:30:00Z"
}
```

## Document Flow

```
User Upload
    ↓
[Upload Component]
    ↓
ApiService.analyzeDocuments()
    ↓
Backend /api/analyze
    ↓
[Processing Pipeline]
    ├─ Text Extraction
    ├─ Classification
    ├─ Field Extraction
    ├─ Validation
    └─ Summarization
    ↓
API Response
    ↓
[DocumentService] - Store in state & localStorage
    ↓
[Results/History Component] - Display results
```

## Data Models

### Document Request
```typescript
interface DocumentInput {
  file: File;
  // File types supported: pdf, image (png, jpg), txt
}
```

### Analysis Response
```typescript
interface AnalysisResult {
  document_id: string;
  file_name: string;
  classification: {
    type: 'invoice' | 'receipt' | 'contract';
    confidence: number;
  };
  extraction: {
    [key: string]: {
      value: string | number;
      confidence: number;
    };
  };
  validation: {
    score: number;
    issues: ValidationIssue[];
  };
  summary: string;
}

interface ValidationIssue {
  field: string;
  severity: 'low' | 'medium' | 'high';
  message: string;
  source: 'rule' | 'ai';
}
```

## Error Handling

The API service includes comprehensive error handling:

```typescript
// In api.service.ts
private handleError(error: HttpErrorResponse) {
  let errorMessage = 'An error occurred';

  if (error.error instanceof ErrorEvent) {
    // Client-side error
    errorMessage = `Error: ${error.error.message}`;
  } else {
    // Server-side error
    errorMessage = `Error Code: ${error.status}\nMessage: ${error.message}`;
  }

  console.error(errorMessage);
  return throwError(() => new Error(errorMessage));
}
```

## Request/Response Examples

### Example 1: Single Document Upload

**Request:**
```bash
curl -X POST http://localhost:8000/api/analyze \
  -F "files=@invoice.pdf"
```

**Response:**
```json
{
  "batch_id": "abc123",
  "documents": [{
    "document_id": "doc456",
    "file_name": "invoice.pdf",
    "classification": {
      "type": "invoice",
      "confidence": 0.96
    },
    "extraction": {
      "company": { "value": "Acme Corp", "confidence": 0.95 },
      "amount": { "value": "1500.00", "confidence": 0.98 },
      "date": { "value": "2024-04-09", "confidence": 0.99 }
    },
    "validation": {
      "score": 0.92,
      "issues": []
    },
    "summary": "Invoice from Acme Corp for $1500 dated April 9, 2024."
  }]
}
```

### Example 2: Batch Documents Upload

**Request:**
```bash
curl -X POST http://localhost:8000/api/analyze \
  -F "files=@invoice1.pdf" \
  -F "files=@invoice2.pdf" \
  -F "files=@receipt.jpg"
```

**Response:** Array of 3 document results in `documents[]`

### Example 3: Error Response

**Request:**
```bash
curl -X POST http://localhost:8000/api/analyze \
  -F "files=@huge_file.zip"
```

**Response (400):**
```json
{
  "error": "File too large",
  "details": "Maximum file size is 50MB",
  "code": "FILE_SIZE_EXCEEDED"
}
```

## Interceptors (Future Enhancement)

Add authentication token to all requests:

```typescript
import { HttpInterceptor } from '@angular/common/http';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const token = localStorage.getItem('auth_token');
    if (token) {
      req = req.clone({
        setHeaders: { Authorization: `Bearer ${token}` }
      });
    }
    return next.handle(req);
  }
}
```

## Testing Endpoints Locally

### Start Backend
```bash
cd /path/to/doc-intelligence
source .venv/bin/activate
python main.py
# Backend runs on http://localhost:8000
```

### Test with curl
```bash
# Health check
curl http://localhost:8000/api/health

# Analyze documents
curl -X POST http://localhost:8000/api/analyze \
  -F "files=@document.pdf"
```

### Test with Angular
```typescript
// In component
constructor(private api: ApiService) {}

testConnection() {
  this.api.healthCheck().subscribe(
    res => console.log('Connected!', res),
    err => console.error('Connection failed', err)
  );
}
```

## Rate Limiting

Backend may implement rate limiting. Handle 429 responses:

```typescript
if (error.status === 429) {
  // Too many requests - wait before retrying
  this.notificationService.warning('Rate limited. Please wait a moment.');
  setTimeout(() => this.retry(), 5000);
}
```

## Timeout Configuration

Set request timeout in api.service:

```typescript
private readonly REQUEST_TIMEOUT = 30000; // 30 seconds

analyzeDocuments(files: File[]) {
  return this.http.post<AnalysisResult[]>(
    `${this.API_URL}/analyze`,
    formData
  ).pipe(
    timeout(this.REQUEST_TIMEOUT),
    catchError(error => {
      if (error.name === 'TimeoutError') {
        throw new Error('Request timed out. Please try again.');
      }
      return throwError(() => error);
    })
  );
}
```

## CORS Configuration

If backend is on different domain, ensure CORS is enabled:

**Backend (FastAPI):**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Debugging

### Enable Request Logging
```typescript
// In api.service.ts
analyzeDocuments(files: File[]) {
  console.log('Sending files:', files);
  return this.http.post(url, formData).pipe(
    tap(response => console.log('Response:', response)),
    catchError(error => {
      console.error('Error:', error);
      return throwError(() => error);
    })
  );
}
```

### Check Network Requests
1. Open DevTools (F12)
2. Go to Network tab
3. Filter by "fetch/xhr"
4. Click on requests to see headers, body, response

### Monitor Performance
```typescript
const start = performance.now();
this.api.analyzeDocuments(files).subscribe(
  () => {
    const duration = performance.now() - start;
    console.log(`Analysis took ${duration}ms`);
  }
);
```

## Production Deployment

### Backend URL Configuration
Update environment.prod.ts:
```typescript
export const environment = {
  production: true,
  apiUrl: 'https://api.yourdomain.com'
};
```

### Build Command
```bash
ng build --configuration production
```

### Deploy to Server
```bash
# Copy dist files to server
scp -r dist/doc-intelligence-ui/* user@server:/var/www/html/
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| CORS errors | Check backend CORS policy |
| 404 endpoints | Verify backend is running on :8000 |
| 500 errors | Check backend logs |
| Timeout errors | Increase timeout or check backend performance |
| File upload fails | Check file size, format, and permissions |

---

For backend API documentation, see [Backend README](../../README.md)
