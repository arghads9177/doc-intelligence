import { Component, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { DocumentService } from '../../shared/services/document.service';
import { AnalyzeResponse, ProcessedDocument } from '../../shared/models';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'app-results',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-50">
      <div class="max-w-6xl mx-auto px-4 py-12">
        <!-- Header -->
        <div class="mb-8">
          <h1 class="text-4xl font-bold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent mb-2">
            Extraction Results
          </h1>
          <p class="text-gray-600" *ngIf="analysisResults?.processed_documents[0]?.filename">
            Document: <code class="bg-blue-50 text-blue-700 px-3 py-1 rounded text-sm font-mono">{{ analysisResults.processed_documents[0].filename }}</code>
          </p>
        </div>

        <!-- Status Message -->
        <div *ngIf="analysisResults" class="mb-8 p-6 rounded-lg" 
          [ngClass]="{'bg-green-50 border border-green-200': analysisResults.status === 'success', 'bg-yellow-50 border border-yellow-200': analysisResults.status !== 'success'}">
          <p [ngClass]="{'text-green-700': analysisResults.status === 'success', 'text-yellow-700': analysisResults.status !== 'success'}" class="font-semibold">
            {{ analysisResults.message }}
          </p>
        </div>

        <!-- Summary Cards -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12" *ngIf="analysisResults?.processed_documents[0]">
          <!-- Document Type Card -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-all duration-200">
            <div class="bg-gradient-to-br from-blue-50 to-cyan-50 p-6 border-b border-blue-200">
              <p class="text-sm font-semibold text-blue-700 uppercase tracking-wide">Document Type</p>
              <p class="text-4xl font-bold text-blue-600 mt-3 capitalize">{{ analysisResults.processed_documents[0].doc_type }}</p>
            </div>
            <div class="p-4 bg-blue-50/50">
              <p class="text-xs text-blue-700 font-medium">
                ✓ {{ (analysisResults.processed_documents[0].doc_type_confidence * 100).toFixed(0) }}% confidence
              </p>
            </div>
          </div>

          <!-- Total Amount Card -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-all duration-200" 
            *ngIf="analysisResults.processed_documents[0].extracted_fields?.total_amount">
            <div class="bg-gradient-to-br from-emerald-50 to-green-50 p-6 border-b border-green-200">
              <p class="text-sm font-semibold text-green-700 uppercase tracking-wide">Total Amount</p>
              <p class="text-3xl font-bold text-green-600 mt-3">
                {{ analysisResults.processed_documents[0].extracted_fields.total_amount.value }}
                <span class="text-lg ml-2" *ngIf="analysisResults.processed_documents[0].extracted_fields?.currency">
                  {{ analysisResults.processed_documents[0].extracted_fields.currency.value }}
                </span>
              </p>
            </div>
            <div class="p-4 bg-green-50/50">
              <p class="text-xs text-green-700 font-medium">
                ✓ {{ (analysisResults.processed_documents[0].extracted_fields.total_amount.confidence * 100).toFixed(0) }}% confidence
              </p>
            </div>
          </div>

          <!-- Validation Status Card -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-all duration-200"
            *ngIf="analysisResults.processed_documents[0].validation_report">
            <div class="bg-gradient-to-br p-6 border-b" 
              [ngClass]="analysisResults.processed_documents[0].validation_report.is_valid ? 'from-green-50 to-emerald-50 border-green-200' : 'from-orange-50 to-amber-50 border-orange-200'">
              <p class="text-sm font-semibold uppercase tracking-wide" 
                [ngClass]="analysisResults.processed_documents[0].validation_report.is_valid ? 'text-green-700' : 'text-orange-700'">
                Validation Status
              </p>
              <p class="text-2xl font-bold mt-3" 
                [ngClass]="analysisResults.processed_documents[0].validation_report.is_valid ? 'text-green-600' : 'text-orange-600'">
                {{ analysisResults.processed_documents[0].validation_report.is_valid ? '✓ Valid' : analysisResults.processed_documents[0].validation_report.total_issues + ' Issues' }}
              </p>
            </div>
            <div class="p-4" [ngClass]="analysisResults.processed_documents[0].validation_report.is_valid ? 'bg-green-50/50' : 'bg-orange-50/50'">
              <p class="text-xs font-medium" 
                [ngClass]="analysisResults.processed_documents[0].validation_report.is_valid ? 'text-green-700' : 'text-orange-700'">
                {{ (analysisResults.processed_documents[0].validation_report.validation_confidence * 100).toFixed(0) }}% confidence
              </p>
            </div>
          </div>
        </div>

        <!-- Tabs & Content -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden" *ngIf="analysisResults?.processed_documents[0]">
          <!-- Tab Navigation -->
          <div class="border-b border-gray-200 flex gap-0 px-6">
            <button (click)="activeTab = 'fields'" 
              [class.border-blue-600]="activeTab === 'fields'"
              [class.text-blue-600]="activeTab === 'fields'"
              class="py-4 px-4 font-semibold border-b-2 border-transparent hover:text-gray-900 transition-colors"
              [ngClass]="activeTab === 'fields' ? '' : 'text-gray-600'">
              Extracted Data
            </button>
            <button (click)="activeTab = 'validation'"
              [class.border-blue-600]="activeTab === 'validation'"
              [class.text-blue-600]="activeTab === 'validation'"
              class="py-4 px-4 font-medium border-b-2 border-transparent hover:text-gray-900 transition-colors"
              [ngClass]="activeTab === 'validation' ? '' : 'text-gray-600'">
              Validation Report
            </button>
            <button (click)="activeTab = 'summary'"
              [class.border-blue-600]="activeTab === 'summary'"
              [class.text-blue-600]="activeTab === 'summary'"
              class="py-4 px-4 font-medium border-b-2 border-transparent hover:text-gray-900 transition-colors"
              [ngClass]="activeTab === 'summary' ? '' : 'text-gray-600'">
              Summary
            </button>
          </div>

          <!-- Tab Content -->
          <div class="p-8">
            <!-- Extracted Fields Tab -->
            <div *ngIf="activeTab === 'fields'" class="space-y-4">
              <ng-container *ngFor="let field of getExtractedFields()">
                <div class="bg-gradient-to-r p-6 rounded-lg border hover:shadow-md transition-all duration-200"
                  [ngClass]="field.confidence >= 0.9 ? 'from-green-50 to-emerald-50 border-green-200' : field.confidence >= 0.7 ? 'from-blue-50 to-cyan-50 border-blue-200' : 'from-yellow-50 to-amber-50 border-yellow-200'">
                  <div class="flex items-start justify-between mb-3">
                    <p class="text-sm font-semibold text-gray-900 capitalize">{{ field.label }}</p>
                    <span class="inline-block px-3 py-1 rounded-full text-xs font-bold"
                      [ngClass]="field.confidence >= 0.9 ? 'bg-green-100 text-green-800' : field.confidence >= 0.7 ? 'bg-blue-100 text-blue-800' : 'bg-yellow-100 text-yellow-800'">
                      {{ (field.confidence * 100).toFixed(0) }}%
                    </span>
                  </div>
                  <p class="text-lg font-bold text-gray-900">{{ formatFieldValue(field.value) }}</p>
                  <p class="text-xs mt-3" [ngClass]="field.confidence >= 0.9 ? 'text-green-700' : field.confidence >= 0.7 ? 'text-blue-700' : 'text-yellow-700'">
                    Confidence: {{ (field.confidence * 100).toFixed(0) }}{{ field.notes ? ' • ' + field.notes : '' }}
                  </p>
                </div>
              </ng-container>
            </div>

            <!-- Validation Report Tab -->
            <div *ngIf="activeTab === 'validation'" class="space-y-4">
              <div class="p-6 rounded-lg border" 
                [ngClass]="analysisResults.processed_documents[0].validation_report?.is_valid ? 'bg-green-50 border-green-200' : 'bg-orange-50 border-orange-200'">
                <h3 class="text-lg font-bold mb-3" 
                  [ngClass]="analysisResults.processed_documents[0].validation_report?.is_valid ? 'text-green-900' : 'text-orange-900'">
                  Validation Result
                </h3>
                <p class="text-base font-semibold mb-2" 
                  [ngClass]="analysisResults.processed_documents[0].validation_report?.is_valid ? 'text-green-700' : 'text-orange-700'">
                  Status: {{ analysisResults.processed_documents[0].validation_report?.is_valid ? '✓ VALID' : '⚠️ ISSUES FOUND' }}
                </p>
                <p class="text-sm text-gray-700">
                  Total Issues: {{ analysisResults.processed_documents[0].validation_report?.total_issues }}
                </p>
                <p class="text-sm text-gray-700">
                  Validation Confidence: {{ (analysisResults.processed_documents[0].validation_report?.validation_confidence ?? 0 * 100).toFixed(0) }}%
                </p>
              </div>

              <div *ngIf="(analysisResults.processed_documents[0].validation_report?.issues || []).length > 0" class="space-y-3">
                <h4 class="font-semibold text-gray-900">Issues Found:</h4>
                <div *ngFor="let issue of analysisResults.processed_documents[0].validation_report?.issues" 
                  class="p-4 rounded-lg border-l-4" 
                  [ngClass]="issue.severity === 'high' ? 'bg-red-50 border-red-400' : issue.severity === 'medium' ? 'bg-yellow-50 border-yellow-400' : 'bg-blue-50 border-blue-400'">
                  <p class="font-semibold text-gray-900">{{ issue.field }} - {{ issue.severity | uppercase }}</p>
                  <p class="text-sm text-gray-700 mt-1">{{ issue.explanation }}</p>
                </div>
              </div>
              <div *ngIf="(analysisResults.processed_documents[0].validation_report?.issues || []).length === 0" class="p-4 rounded-lg bg-green-50 border border-green-200">
                <p class="text-green-700 font-semibold">✓ All validations passed. No issues detected.</p>
              </div>
            </div>

            <!-- Summary Tab -->
            <div *ngIf="activeTab === 'summary'" class="space-y-4">
              <div class="p-6 rounded-lg bg-gradient-to-br from-indigo-50 to-purple-50 border border-indigo-200">
                <h3 class="text-lg font-bold text-indigo-900 mb-4">AI-Generated Summary</h3>
                <p class="text-gray-800 leading-relaxed text-justify">
                  {{ analysisResults.processed_documents[0].summary }}
                </p>
              </div>
              <div *ngIf="analysisResults.processed_documents[0].raw_text_preview" class="p-6 rounded-lg bg-gray-100 border border-gray-300">
                <h3 class="text-sm font-bold text-gray-900 mb-3">Raw Text Preview:</h3>
                <p class="text-xs text-gray-700 font-mono whitespace-pre-wrap break-words">
                  {{ analysisResults.processed_documents[0].raw_text_preview }}...
                </p>
              </div>
            </div>

            <!-- Action Section -->
            <div class="mt-8 pt-8 border-t border-gray-200 flex gap-4">
              <button (click)="downloadReport()" class="px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg hover:from-blue-700 hover:to-blue-800 font-semibold shadow-md hover:shadow-lg transition-all duration-200">
                📥 Download Report
              </button>
              <button (click)="goBack()" class="px-6 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 font-semibold transition-colors">
                ← Back to Upload
              </button>
            </div>
          </div>
        </div>

        <!-- Loading State -->
        <div *ngIf="!analysisResults" class="text-center py-12">
          <p class="text-gray-600 text-lg">Loading analysis results...</p>
        </div>

        <!-- Not Found State -->
        <div *ngIf="notFound" class="text-center py-12 bg-red-50 rounded-lg border border-red-200">
          <p class="text-red-700 text-lg font-semibold mb-4">Analysis results not found</p>
          <p class="text-red-600 mb-6">The batch ID "{{ batchId }}" could not be located.</p>
          <button (click)="goBack()" class="px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 font-semibold transition-colors">
            ← Back to Upload
          </button>
        </div>
      </div>
    </div>
  `,
  styles: []
})
export class ResultsComponent implements OnInit, OnDestroy {
  analysisResults: AnalyzeResponse | null = null;
  activeTab: 'fields' | 'validation' | 'summary' = 'fields';
  batchId: string | null = null;
  notFound: boolean = false;
  private destroy$ = new Subject<void>();

  constructor(
    private documentService: DocumentService,
    private route: ActivatedRoute,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    // Get batch ID from route parameter
    this.route.params.pipe(takeUntil(this.destroy$)).subscribe((params) => {
      const batchId = params['id'];
      if (batchId) {
        this.batchId = batchId;
        // Fetch analysis results for this specific batch
        const results = this.documentService.getAnalysisResultsByBatchId(batchId);
        if (results) {
          this.analysisResults = results;
          this.notFound = false;
        } else {
          // If not found in local storage, try the current observable (for fresh uploads)
          const currentResults = this.documentService.getAnalysisResults();
          const latestId = this.documentService.getLatestResultId();
          if (currentResults && latestId === batchId) {
            this.analysisResults = currentResults;
            this.notFound = false;
          } else {
            this.notFound = true;
          }
        }
        // Force change detection
        this.cdr.markForCheck();
      }
    });

    // Also subscribe to analysis results in case it gets updated
    this.documentService.analysisResults$
      .pipe(takeUntil(this.destroy$))
      .subscribe((results) => {
        // Only update if this is for the current batch
        if (this.batchId && this.documentService.getLatestResultId() === this.batchId) {
          this.analysisResults = results;
          this.notFound = false;
          this.cdr.markForCheck();
        }
      });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  getExtractedFields(): any[] {
    if (!this.analysisResults?.processed_documents[0]?.extracted_fields) {
      return [];
    }

    const fields = this.analysisResults.processed_documents[0].extracted_fields;
    const result: any[] = [];

    Object.entries(fields).forEach(([key, value]: [string, any]) => {
      if (value && typeof value === 'object' && 'value' in value) {
        result.push({
          label: key.replace(/_/g, ' '),
          value: value.value,
          confidence: value.confidence || 0,
          notes: value.notes
        });
      }
    });

    return result;
  }

  formatFieldValue(value: any): string {
    if (Array.isArray(value)) {
      return value.length + ' item(s)';
    }
    if (typeof value === 'object') {
      return JSON.stringify(value);
    }
    return String(value);
  }

  downloadReport(): void {
    const data = JSON.stringify(this.analysisResults, null, 2);
    const blob = new Blob([data], { type: 'application/json' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `analysis-report-${Date.now()}.json`;
    a.click();
    window.URL.revokeObjectURL(url);
  }

  goBack(): void {
    this.router.navigate(['/upload']);
  }
}
