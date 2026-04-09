import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DocumentService } from '../../shared/services/document.service';
import { ApiService } from '../../shared/services/api.service';
import { NotificationService } from '../../shared/services/notification.service';
import { Document } from '../../shared/models';

@Component({
  selector: 'app-upload',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-50">
      <div class="max-w-4xl mx-auto px-4 py-12">
        <!-- Header -->
        <div class="mb-12">
          <h1 class="text-4xl font-bold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent mb-2">
            Upload Documents
          </h1>
          <p class="text-gray-600 text-lg">Drag and drop your documents or click to select files for analysis.</p>
        </div>

        <!-- Drag-Drop Zone -->
        <div
          (dragover)="onDragOver($event)"
          (dragleave)="onDragLeave($event)"
          (drop)="onDrop($event)"
          [class.border-blue-500]="isDragging"
          [class.bg-blue-50]="isDragging"
          class="relative border-2 border-dashed border-gray-300 rounded-2xl p-12 text-center cursor-pointer hover:border-blue-400 hover:bg-blue-50 transition-all duration-300 shadow-sm hover:shadow-md"
        >
          <input
            #fileInput
            type="file"
            multiple
            [(ngModel)]="selectedFiles"
            (change)="onFileSelected($event)"
            hidden
            accept=".pdf,.doc,.docx,.jpg,.jpeg,.png,.tiff"
            #fileInputRef
          />

          <div class="space-y-4">
            <div class="text-6xl">{{ isDragging ? '⬇️' : '📄' }}</div>
            <div>
              <p class="text-xl font-semibold text-gray-900 mb-2">
                {{ isDragging ? 'Drop files now' : 'Drag files here or click to browse' }}
              </p>
              <p class="text-sm text-gray-500">Supports PDF, DOC, DOCX, JPG, PNG, TIFF (max 50MB each)</p>
            </div>
            <button
              (click)="fileInputRef.click()"
              class="inline-block px-8 py-3 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg hover:from-blue-700 hover:to-blue-800 transition-all duration-200 font-semibold shadow-md hover:shadow-lg transform hover:scale-105"
            >
              Select Files
            </button>
          </div>
        </div>

        <!-- File List -->
        <div *ngIf="uploadedDocuments.length > 0" class="mt-12">
          <h2 class="text-2xl font-bold text-gray-900 mb-6">Selected Documents <span class="text-blue-600">({{ uploadedDocuments.length }})</span></h2>
          <div class="space-y-3">
            <div
              *ngFor="let doc of uploadedDocuments; let i = index"
              class="flex items-center justify-between bg-white border border-gray-200 rounded-xl p-6 hover:shadow-lg hover:border-blue-300 transition-all duration-200"
            >
              <div class="flex items-center gap-4 flex-1">
                <div class="text-3xl">📋</div>
                <div class="flex-1 min-w-0">
                  <p class="font-semibold text-gray-900 truncate">{{ doc.filename }}</p>
                  <p class="text-sm text-gray-500">{{ (doc.fileSize / 1024 / 1024).toFixed(2) }} MB • Added just now</p>
                </div>
              </div>
              <button
                (click)="removeDocument(doc.id)"
                class="ml-4 px-4 py-2 text-red-600 hover:bg-red-50 hover:text-red-700 rounded-lg font-medium transition-colors duration-200"
              >
                Remove
              </button>
            </div>
          </div>
        </div>

        <!-- Processing Options -->
        <div *ngIf="uploadedDocuments.length > 0" class="mt-12 bg-white rounded-xl p-8 border border-gray-200 shadow-sm">
          <h3 class="text-lg font-bold text-gray-900 mb-6">Processing Options</h3>
          <div class="space-y-4">
            <label class="flex items-center gap-3 cursor-pointer group">
              <input 
                type="checkbox" 
                [checked]="includeValidation" 
                (change)="includeValidation = !includeValidation" 
                class="w-5 h-5 text-blue-600 rounded border-gray-300 cursor-pointer"
              />
              <div class="flex-1">
                <span class="text-base font-medium text-gray-900 group-hover:text-blue-600 transition-colors">Run Data Validation</span>
                <p class="text-sm text-gray-500">Validate extracted data against business rules</p>
              </div>
            </label>
            <label class="flex items-center gap-3 cursor-pointer group">
              <input 
                type="checkbox" 
                [checked]="includeSummary" 
                (change)="includeSummary = !includeSummary" 
                class="w-5 h-5 text-blue-600 rounded border-gray-300 cursor-pointer"
              />
              <div class="flex-1">
                <span class="text-base font-medium text-gray-900 group-hover:text-blue-600 transition-colors">Generate AI Summary</span>
                <p class="text-sm text-gray-500">Create a concise summary of document contents</p>
              </div>
            </label>
          </div>
        </div>

        <!-- Action Buttons -->
        <div *ngIf="uploadedDocuments.length > 0" class="mt-12 flex gap-4">
          <button
            (click)="submitDocuments()"
            [disabled]="isProcessing"
            class="flex-1 px-8 py-4 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg hover:from-blue-700 hover:to-blue-800 disabled:from-gray-400 disabled:to-gray-500 disabled:cursor-not-allowed transition-all duration-200 font-bold shadow-md hover:shadow-lg text-lg"
          >
            {{ isProcessing ? '⏳ Processing...' : '🚀 Analyze Documents' }}
          </button>
          <button
            (click)="clearAll()"
            [disabled]="isProcessing"
            class="px-8 py-4 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 disabled:bg-gray-50 disabled:text-gray-400 disabled:cursor-not-allowed transition-all duration-200 font-semibold"
          >
            Clear All
          </button>
        </div>

        <!-- Empty State -->
        <div *ngIf="uploadedDocuments.length === 0" class="mt-16 text-center py-12">
          <p class="text-gray-500 text-lg">No documents selected yet. Upload a document to begin analysis.</p>
        </div>
      </div>
    </div>
  `,
  styles: [
    `
      :host {
        display: block;
      }
    `
  ]
})
export class UploadComponent implements OnInit {
  @ViewChild('fileInputRef') fileInputRef!: ElementRef;

  uploadedDocuments: Document[] = [];
  isDragging = false;
  isProcessing = false;
  selectedFiles: FileList | null = null;
  includeValidation = true;
  includeSummary = true;

  private readonly MAX_FILE_SIZE = 50 * 1024 * 1024; // 50MB
  private readonly ALLOWED_TYPES = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'image/jpeg', 'image/png', 'image/tiff'];

  constructor(
    private documentService: DocumentService,
    private apiService: ApiService,
    private notificationService: NotificationService
  ) {}

  ngOnInit(): void {
    // Clear documents on component load
    this.documentService.clearDocuments();
  }

  onDragOver(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    this.isDragging = true;
  }

  onDragLeave(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    this.isDragging = false;
  }

  onDrop(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    this.isDragging = false;

    const files = event.dataTransfer?.files;
    if (files) {
      this.processFiles(files);
    }
  }

  onFileSelected(event: Event): void {
    const target = event.target as HTMLInputElement;
    const files = target.files;
    if (files) {
      this.processFiles(files);
    }
  }

  private processFiles(files: FileList): void {
    const validFiles: File[] = [];
    let hasInvalidFiles = false;

    for (let i = 0; i < files.length; i++) {
      const file = files[i];

      // Validate file size
      if (file.size > this.MAX_FILE_SIZE) {
        this.notificationService.error(`${file.name} exceeds 50MB limit`);
        hasInvalidFiles = true;
        continue;
      }

      // Validate file type
      if (!this.ALLOWED_TYPES.includes(file.type)) {
        this.notificationService.error(`${file.name} is not a supported file type`);
        hasInvalidFiles = true;
        continue;
      }

      validFiles.push(file);
    }

    if (validFiles.length > 0) {
      // Add valid files to document service
      validFiles.forEach((file) => {
        this.documentService.addDocument(file.name, file.size, file.type);
      });

      // Update local reference
      this.documentService.documents$.subscribe((docs) => {
        this.uploadedDocuments = docs;
      });

      this.notificationService.success(`${validFiles.length} file(s) added`);
    }

    if (hasInvalidFiles && validFiles.length === 0) {
      this.notificationService.error('No valid files to upload');
    }
  }

  removeDocument(documentId: string): void {
    this.documentService.removeDocument(documentId);
  }

  clearAll(): void {
    this.documentService.clearDocuments();
    this.uploadedDocuments = [];
    if (this.fileInputRef) {
      this.fileInputRef.nativeElement.value = '';
    }
  }

  submitDocuments(): void {
    if (this.uploadedDocuments.length === 0) {
      this.notificationService.warning('Please select documents to analyze');
      return;
    }

    this.isProcessing = true;
    this.documentService.setProcessingStatus('ingesting' as any);

    // Convert documents to API request format
    this.apiService.filesToDocumentInputs(Array.from((this.fileInputRef.nativeElement as HTMLInputElement).files || [])).then((documentInputs) => {
      const analyzeRequest = {
        documents: documentInputs,
        include_validation: this.includeValidation,
        include_summary: this.includeSummary
      };

      this.apiService.analyzeDocuments(analyzeRequest.documents, this.includeSummary, this.includeValidation).subscribe({
        next: (response) => {
          this.isProcessing = false;
          this.notificationService.success(`Successfully analyzed ${response.processedDocuments.length} document(s)`);

          // Save to history
          const batch = {
            id: this.documentService.generateBatchId(),
            createdAt: new Date(),
            completedAt: new Date(),
            documents: this.uploadedDocuments,
            totalDocuments: this.uploadedDocuments.length,
            processedDocuments: response.totalProcessed,
            failedDocuments: response.totalErrors
          };
          this.documentService.addToHistory(batch);

          // Clear and redirect would happen here
          setTimeout(() => {
            this.clearAll();
          }, 1000);
        },
        error: (error) => {
          this.isProcessing = false;
          this.notificationService.error(`Failed to analyze documents: ${error.message}`);
        }
      });
    });
  }
}
