import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';

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
          <p class="text-gray-600">Document ID: <code class="bg-blue-50 text-blue-700 px-3 py-1 rounded text-sm font-mono">{{ documentId }}</code></p>
        </div>

        <!-- Summary Cards -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <!-- Confidence Card -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-all duration-200">
            <div class="bg-gradient-to-br from-green-50 to-emerald-50 p-6 border-b border-green-200">
              <p class="text-sm font-semibold text-green-700 uppercase tracking-wide">Confidence Score</p>
              <p class="text-4xl font-bold text-green-600 mt-3">94%</p>
            </div>
            <div class="p-4 bg-green-50/50">
              <p class="text-xs text-green-700 font-medium">✓ High confidence extraction</p>
            </div>
          </div>

          <!-- Document Type Card -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-all duration-200">
            <div class="bg-gradient-to-br from-blue-50 to-cyan-50 p-6 border-b border-blue-200">
              <p class="text-sm font-semibold text-blue-700 uppercase tracking-wide">Document Type</p>
              <p class="text-4xl font-bold text-blue-600 mt-3">Invoice</p>
            </div>
            <div class="p-4 bg-blue-50/50">
              <p class="text-xs text-blue-700 font-medium">✓ Confidently identified</p>
            </div>
          </div>

          <!-- Validation Card -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-all duration-200">
            <div class="bg-gradient-to-br from-orange-50 to-amber-50 p-6 border-b border-orange-200">
              <p class="text-sm font-semibold text-orange-700 uppercase tracking-wide">Validation Status</p>
              <p class="text-4xl font-bold text-orange-600 mt-3">3</p>
            </div>
            <div class="p-4 bg-orange-50/50">
              <p class="text-xs text-orange-700 font-medium">⚠️ Issues found - review recommended</p>
            </div>
          </div>
        </div>

        <!-- Tabs & Content -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <!-- Tab Navigation -->
          <div class="border-b border-gray-200 flex gap-0 px-6">
            <button class="py-4 px-4 font-semibold text-blue-600 border-b-2 border-blue-600 hover:text-blue-700 transition-colors">
              Extracted Data
            </button>
            <button class="py-4 px-4 font-medium text-gray-600 hover:text-gray-900 transition-colors border-b-2 border-transparent">
              Validation Report
            </button>
            <button class="py-4 px-4 font-medium text-gray-600 hover:text-gray-900 transition-colors border-b-2 border-transparent">
              Summary
            </button>
          </div>

          <!-- Tab Content -->
          <div class="p-8">
            <div class="space-y-4">
              <div class="bg-gradient-to-r from-blue-50 to-cyan-50 p-6 rounded-lg border border-blue-200 hover:shadow-md transition-all duration-200">
                <div class="flex items-start justify-between mb-3">
                  <p class="text-sm font-semibold text-blue-900">Invoice Number</p>
                  <span class="inline-block px-3 py-1 bg-green-100 text-green-800 rounded-full text-xs font-bold">98%</span>
                </div>
                <p class="text-2xl font-bold text-gray-900">INV-2024-001</p>
                <p class="text-xs text-blue-700 mt-3">Confidence: 98% • Extracted field • No corrections needed</p>
              </div>

              <div class="bg-gradient-to-r from-emerald-50 to-green-50 p-6 rounded-lg border border-green-200 hover:shadow-md transition-all duration-200">
                <div class="flex items-start justify-between mb-3">
                  <p class="text-sm font-semibold text-green-900">Total Amount</p>
                  <span class="inline-block px-3 py-1 bg-green-100 text-green-800 rounded-full text-xs font-bold">99%</span>
                </div>
                <p class="text-2xl font-bold text-gray-900">$1,500.00 USD</p>
                <p class="text-xs text-green-700 mt-3">Confidence: 99% • Verified against totals • ISO 4217 currency</p>
              </div>

              <div class="bg-gradient-to-r from-purple-50 to-pink-50 p-6 rounded-lg border border-purple-200 hover:shadow-md transition-all duration-200">
                <div class="flex items-start justify-between mb-3">
                  <p class="text-sm font-semibold text-purple-900">Invoice Date</p>
                  <span class="inline-block px-3 py-1 bg-green-100 text-green-800 rounded-full text-xs font-bold">95%</span>
                </div>
                <p class="text-2xl font-bold text-gray-900">2024-01-15</p>
                <p class="text-xs text-purple-700 mt-3">Confidence: 95% • ISO 8601 format • Valid date range</p>
              </div>
            </div>

            <!-- Action Section -->
            <div class="mt-8 pt-8 border-t border-gray-200 flex gap-4">
              <button class="px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg hover:from-blue-700 hover:to-blue-800 font-semibold shadow-md hover:shadow-lg transition-all duration-200">
                ✓ Approve & Confirm
              </button>
              <button class="px-6 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 font-semibold transition-colors">
                ✏️ Edit Fields
              </button>
              <button class="px-6 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 font-semibold transition-colors">
                📥 Download Report
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: []
})
export class ResultsComponent implements OnInit {
  documentId: string | null = null;

  constructor(private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.route.paramMap.subscribe((params) => {
      this.documentId = params.get('id');
    });
  }
}
