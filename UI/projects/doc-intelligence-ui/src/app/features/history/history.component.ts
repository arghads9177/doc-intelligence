import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { DocumentService } from '../../shared/services/document.service';
import { DocumentBatch } from '../../shared/models';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'app-history',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-50">
      <div class="max-w-7xl mx-auto px-4 py-12">
        <!-- Header -->
        <div class="mb-8">
          <h1 class="text-4xl font-bold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent mb-2">
            Processing History
          </h1>
          <p class="text-gray-600">View and manage your document processing history with detailed insights.</p>
        </div>

        <!-- Empty State -->
        <div *ngIf="history.length === 0" class="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
          <p class="text-2xl mb-2">📋</p>
          <p class="text-lg font-semibold text-gray-900 mb-2">No processing history yet</p>
          <p class="text-gray-600 mb-6">Start by uploading and analyzing documents to see your history here.</p>
          <a routerLink="/upload" class="inline-block px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
            Upload Documents →
          </a>
        </div>

        <!-- Table Container -->
        <div *ngIf="history.length > 0" class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full">
              <!-- Table Header -->
              <thead>
                <tr class="bg-gradient-to-r from-gray-50 to-gray-50 border-b border-gray-200">
                  <th class="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">Document(s)</th>
                  <th class="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">Total</th>
                  <th class="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">Processed</th>
                  <th class="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">Errors</th>
                  <th class="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">Date</th>
                  <th class="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>

              <!-- Table Body -->
              <tbody class="divide-y divide-gray-200">
                <tr *ngFor="let batch of history; let i = index" 
                  class="hover:bg-blue-50 transition-colors duration-150 group"
                  [ngClass]="{ 'bg-green-50 hover:bg-green-100': batch.failedDocuments === 0 }">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <div class="w-10 h-10 rounded-lg" 
                        [ngClass]="batch.failedDocuments === 0 ? 'bg-green-100' : 'bg-red-100'"
                        [innerHTML]="'📄'">
                      </div>
                      <div class="ml-3">
                        <p class="text-sm font-semibold text-gray-900">{{ batch.documents.length }} document(s)</p>
                        <p class="text-xs text-gray-500">{{ formatBatchId(batch.id) }}</p>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-3 py-1 inline-flex items-center text-xs font-semibold rounded-full bg-blue-100 text-blue-700 border border-blue-200">
                      {{ batch.totalDocuments }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-3 py-1 inline-flex items-center text-xs font-bold rounded-full" 
                      [ngClass]="batch.processedDocuments === batch.totalDocuments ? 'bg-green-100 text-green-800 border border-green-300' : 'bg-amber-100 text-amber-800 border border-amber-300'">
                      {{ batch.processedDocuments }}/{{ batch.totalDocuments }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span *ngIf="batch.failedDocuments > 0" class="px-3 py-1 inline-flex items-center text-xs font-bold rounded-full bg-red-100 text-red-800 border border-red-300">
                      {{ batch.failedDocuments }}
                    </span>
                    <span *ngIf="batch.failedDocuments === 0" class="text-sm text-gray-500">—</span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                    <div>{{ batch.createdAt | date: 'MMM d, yyyy' }}</div>
                    <div class="text-xs text-gray-500">{{ batch.createdAt | date: 'h:mm a' }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div class="flex gap-2">
                      <a [routerLink]="['/results', batch.id]" 
                        class="px-3 py-1.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all transform hover:scale-105 inline-block">
                        View →
                      </a>
                      <button (click)="deleteHistory(batch.id)"
                        class="px-3 py-1.5 bg-red-100 text-red-600 rounded-lg hover:bg-red-200 transition-all">
                        ✕
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Table Footer Stats -->
          <div class="px-6 py-4 bg-gray-50 border-t border-gray-200 grid grid-cols-4 gap-4">
            <div class="text-center">
              <p class="text-2xl font-bold text-blue-600">{{ getTotalDocuments() }}</p>
              <p class="text-xs text-gray-600">Total Documents</p>
            </div>
            <div class="text-center">
              <p class="text-2xl font-bold text-green-600">{{ getTotalProcessed() }}</p>
              <p class="text-xs text-gray-600">Successfully Processed</p>
            </div>
            <div class="text-center">
              <p class="text-2xl font-bold text-red-600">{{ getTotalErrors() }}</p>
              <p class="text-xs text-gray-600">Errors</p>
            </div>
            <div class="text-center">
              <p class="text-2xl font-bold text-purple-600">{{ history.length }}</p>
              <p class="text-xs text-gray-600">Total Batches</p>
            </div>
          </div>
        </div>

        <!-- Info Card -->
        <div class="mt-8 p-6 bg-gradient-to-r from-blue-50 to-cyan-50 rounded-xl border border-blue-200 shadow-sm">
          <div class="flex items-start gap-4">
            <div class="text-2xl">💡</div>
            <div>
              <p class="font-semibold text-blue-900">Pro Tip</p>
              <p class="text-sm text-blue-800 mt-1">Click on "View" to see detailed extraction results and manually correct any fields if needed.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: []
})
export class HistoryComponent implements OnInit, OnDestroy {
  history: DocumentBatch[] = [];
  private destroy$ = new Subject<void>();

  constructor(private documentService: DocumentService) {}

  ngOnInit(): void {
    this.documentService.documentHistory$
      .pipe(takeUntil(this.destroy$))
      .subscribe((batches) => {
        this.history = batches;
      });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  getTotalDocuments(): number {
    return this.history.reduce((sum, batch) => sum + batch.totalDocuments, 0);
  }

  getTotalProcessed(): number {
    return this.history.reduce((sum, batch) => sum + batch.processedDocuments, 0);
  }

  getTotalErrors(): number {
    return this.history.reduce((sum, batch) => sum + batch.failedDocuments, 0);
  }

  formatBatchId(id: string): string {
    return id.substring(0, 8) + '...';
  }

  deleteHistory(batchId: string): void {
    if (confirm('Are you sure you want to delete this history item?')) {
      this.documentService.deleteHistoryItem(batchId);
    }
  }
}
