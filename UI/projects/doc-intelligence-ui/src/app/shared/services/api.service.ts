import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import {
  AnalyzeRequest,
  AnalyzeResponse,
  HealthCheckResponse,
  ApiError,
  DocumentInput
} from '../models';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  /**
   * Analyze documents through the complete pipeline
   * @param documents - Array of documents to analyze
   * @param includeSummary - Include AI-generated summaries
   * @param includeValidation - Include validation reports
   */
  analyzeDocuments(
    documents: DocumentInput[],
    includeSummary: boolean = true,
    includeValidation: boolean = true
  ): Observable<AnalyzeResponse> {
    const request: AnalyzeRequest = {
      documents,
      includeSummary,
      includeValidation
    };

    return this.http
      .post<AnalyzeResponse>(`${this.apiUrl}/api/analyze`, request)
      .pipe(
        tap((response) => {
          console.log('Analysis completed:', response);
        }),
        catchError(this.handleError)
      );
  }

  /**
   * Check API health status
   */
  healthCheck(): Observable<HealthCheckResponse> {
    return this.http
      .get<HealthCheckResponse>(`${this.apiUrl}/health`)
      .pipe(
        tap((response) => {
          console.log('Health check passed:', response);
        }),
        catchError(this.handleError)
      );
  }

  /**
   * Convert file to base64 string
   * @param file - File to convert
   */
  fileToBase64(file: File): Promise<string> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        const result = reader.result as string;
        const base64String = result.split(',')[1];
        resolve(base64String);
      };
      reader.onerror = (error) => {
        reject(error);
      };
      reader.readAsDataURL(file);
    });
  }

  /**
   * Convert multiple files to DocumentInput array
   * @param files - Files to convert
   */
  async filesToDocumentInputs(files: File[]): Promise<DocumentInput[]> {
    const documentInputs: DocumentInput[] = [];

    for (const file of files) {
      const base64 = await this.fileToBase64(file);
      documentInputs.push({
        filename: file.name,
        contentType: file.type || 'application/octet-stream',
        fileBytes: base64
      });
    }

    return documentInputs;
  }

  /**
   * Handle HTTP errors
   * @param error - HTTP error response
   */
  private handleError(error: HttpErrorResponse): Observable<never> {
    let apiError: ApiError;

    if (error.error instanceof ErrorEvent) {
      // Client-side or network error
      apiError = {
        status: 0,
        message: 'Network error',
        error: error.error.message
      };
    } else {
      // Backend returned an unsuccessful response code
      apiError = {
        status: error.status,
        message: error.message || 'Server error',
        error: error.error?.message || error.statusText,
        details: error.error
      };
    }

    console.error('API Error:', apiError);
    return throwError(() => apiError);
  }
}
