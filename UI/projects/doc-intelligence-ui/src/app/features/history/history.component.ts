import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';

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

        <!-- Table Container -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full">
              <!-- Table Header -->
              <thead>
                <tr class="bg-gradient-to-r from-gray-50 to-gray-50 border-b border-gray-200">
                  <th class="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">Document</th>
                  <th class="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">Type</th>
                  <th class="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">Status</th>
                  <th class="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">Confidence</th>
                  <th class="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">Date</th>
                  <th class="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>

              <!-- Table Body -->
              <tbody class="divide-y divide-gray-200">
                <!-- Row 1 -->
                <tr class="hover:bg-blue-50 transition-colors duration-150 group">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <div class="w-10 h-10 rounded-lg bg-red-100 flex items-center justify-center mr-3 group-hover:scale-105 transition-transform">
                        <span class="text-red-600 font-bold">📄</span>
                      </div>
                      <div>
                        <p class="text-sm font-semibold text-gray-900">Invoice_2024_01.pdf</p>
                        <p class="text-xs text-gray-500">1.2 MB</p>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-3 py-1 inline-flex items-center text-xs font-semibold rounded-full bg-blue-100 text-blue-700 border border-blue-200">
                      📋 Invoice
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-3 py-1 inline-flex items-center text-xs font-bold rounded-full bg-green-100 text-green-800 border border-green-300">
                      ✓ Complete
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center gap-2">
                      <div class="w-16 bg-gray-200 rounded-full h-2">
                        <div class="bg-gradient-to-r from-green-400 to-green-600 h-2 rounded-full" style="width: 94%;"></div>
                      </div>
                      <span class="text-sm font-semibold text-green-600">94%</span>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                    <div>2024-01-15</div>
                    <div class="text-xs text-gray-500">10:30 AM</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <a routerLink="/results/123" class="px-3 py-1.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all transform hover:scale-105 inline-block">
                      View →
                    </a>
                  </td>
                </tr>

                <!-- Row 2 -->
                <tr class="hover:bg-amber-50 transition-colors duration-150 group">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <div class="w-10 h-10 rounded-lg bg-purple-100 flex items-center justify-center mr-3 group-hover:scale-105 transition-transform">
                        <span class="text-purple-600 font-bold">🔗</span>
                      </div>
                      <div>
                        <p class="text-sm font-semibold text-gray-900">Contract_Q4_2024.pdf</p>
                        <p class="text-xs text-gray-500">2.8 MB</p>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-3 py-1 inline-flex items-center text-xs font-semibold rounded-full bg-purple-100 text-purple-700 border border-purple-200">
                      📜 Contract
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-3 py-1 inline-flex items-center text-xs font-bold rounded-full bg-amber-100 text-amber-800 border border-amber-300 animate-pulse">
                      ⟳ Processing
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center gap-2">
                      <span class="text-sm font-semibold text-gray-500">--</span>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                    <div>2024-01-14</div>
                    <div class="text-xs text-gray-500">3:45 PM</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <a routerLink="/process/456" class="px-3 py-1.5 bg-amber-600 text-white rounded-lg hover:bg-amber-700 transition-all transform hover:scale-105 inline-block">
                      Monitor →
                    </a>
                  </td>
                </tr>

                <!-- Row 3 -->
                <tr class="hover:bg-teal-50 transition-colors duration-150 group">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <div class="w-10 h-10 rounded-lg bg-orange-100 flex items-center justify-center mr-3 group-hover:scale-105 transition-transform">
                        <span class="text-orange-600 font-bold">🧾</span>
                      </div>
                      <div>
                        <p class="text-sm font-semibold text-gray-900">Receipt_Jan.pdf</p>
                        <p class="text-xs text-gray-500">0.8 MB</p>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-3 py-1 inline-flex items-center text-xs font-semibold rounded-full bg-orange-100 text-orange-700 border border-orange-200">
                      🛒 Receipt
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-3 py-1 inline-flex items-center text-xs font-bold rounded-full bg-green-100 text-green-800 border border-green-300">
                      ✓ Complete
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center gap-2">
                      <div class="w-16 bg-gray-200 rounded-full h-2">
                        <div class="bg-gradient-to-r from-yellow-400 to-yellow-600 h-2 rounded-full" style="width: 87%;"></div>
                      </div>
                      <span class="text-sm font-semibold text-yellow-600">87%</span>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                    <div>2024-01-13</div>
                    <div class="text-xs text-gray-500">2:15 PM</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <a routerLink="/results/789" class="px-3 py-1.5 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-all transform hover:scale-105 inline-block">
                      View →
                    </a>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Table Footer Stats -->
          <div class="px-6 py-4 bg-gray-50 border-t border-gray-200 grid grid-cols-4 gap-4">
            <div class="text-center">
              <p class="text-2xl font-bold text-blue-600">3</p>
              <p class="text-xs text-gray-600">Total Documents</p>
            </div>
            <div class="text-center">
              <p class="text-2xl font-bold text-green-600">2</p>
              <p class="text-xs text-gray-600">Completed</p>
            </div>
            <div class="text-center">
              <p class="text-2xl font-bold text-amber-600">1</p>
              <p class="text-xs text-gray-600">Processing</p>
            </div>
            <div class="text-center">
              <p class="text-2xl font-bold text-purple-600">91%</p>
              <p class="text-xs text-gray-600">Avg Confidence</p>
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
export class HistoryComponent {}
