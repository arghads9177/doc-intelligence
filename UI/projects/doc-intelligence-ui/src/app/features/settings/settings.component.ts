import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SettingsService, AppSettings } from '../../shared/services/settings.service';
import { DocumentService } from '../../shared/services/document.service';

@Component({
  selector: 'app-settings',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-50">
      <div class="max-w-3xl mx-auto px-4 py-12">
        <!-- Header -->
        <div class="mb-8">
          <h1 class="text-4xl font-bold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent mb-2">
            Settings
          </h1>
          <p class="text-gray-600">Configure application preferences and behavior to suit your needs.</p>
        </div>

        <!-- Save confirmation -->
        <div *ngIf="saveMessage" class="mb-4 px-4 py-3 bg-green-50 border border-green-300 text-green-800 rounded-lg text-sm font-medium transition-all">
          {{ saveMessage }}
        </div>

        <!-- API Settings Section -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden mb-6 hover:shadow-md transition-shadow">
          <div class="bg-gradient-to-r from-blue-50 to-cyan-50 px-6 py-4 border-b border-gray-200">
            <h2 class="text-lg font-bold text-blue-900">🔌 API Configuration</h2>
          </div>
          <div class="p-6 space-y-6">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">API Endpoint</label>
              <input
                type="text"
                value="http://localhost:8000"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg bg-gray-50 text-gray-700 font-mono text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                disabled
              />
              <p class="text-xs text-gray-500 mt-2">Backend API server address (read-only)</p>
            </div>

            <div class="border-t border-gray-200 pt-6 space-y-4">
              <div class="flex items-center justify-between p-4 bg-blue-50 rounded-lg border border-blue-200 hover:shadow-sm transition-all">
                <div>
                  <p class="font-semibold text-gray-900">Include Validation</p>
                  <p class="text-sm text-gray-600 mt-1">Run validation on extracted data</p>
                </div>
                <input type="checkbox"
                  [(ngModel)]="settings.includeValidation"
                  (ngModelChange)="persist()"
                  class="w-5 h-5 text-blue-600 rounded cursor-pointer accent-blue-600" />
              </div>

              <div class="flex items-center justify-between p-4 bg-green-50 rounded-lg border border-green-200 hover:shadow-sm transition-all">
                <div>
                  <p class="font-semibold text-gray-900">Generate Summary</p>
                  <p class="text-sm text-gray-600 mt-1">Create AI summary of documents</p>
                </div>
                <input type="checkbox"
                  [(ngModel)]="settings.includeSummary"
                  (ngModelChange)="persist()"
                  class="w-5 h-5 text-blue-600 rounded cursor-pointer accent-blue-600" />
              </div>
            </div>
          </div>
        </div>

        <!-- Processing Settings Section -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden mb-6 hover:shadow-md transition-shadow">
          <div class="bg-gradient-to-r from-purple-50 to-pink-50 px-6 py-4 border-b border-gray-200">
            <h2 class="text-lg font-bold text-purple-900">⚙️ Processing Options</h2>
          </div>
          <div class="p-6 space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-3">Batch Size</label>
                <select [(ngModel)]="settings.batchSize" (ngModelChange)="persist()"
                  class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all">
                  <option [ngValue]="5">5 documents</option>
                  <option [ngValue]="10">10 documents</option>
                  <option [ngValue]="20">20 documents</option>
                  <option [ngValue]="50">50 documents</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-3">Auto-Clear History</label>
                <select [(ngModel)]="settings.autoClearHistory" (ngModelChange)="persist()"
                  class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all">
                  <option value="never">Never</option>
                  <option value="1week">1 week</option>
                  <option value="1month">1 month</option>
                  <option value="3months">3 months</option>
                </select>
              </div>
            </div>

            <div class="bg-purple-50 p-4 rounded-lg border border-purple-200">
              <p class="text-sm text-purple-900"><strong>💡 Tip:</strong> Larger batch sizes process files faster but use more memory.</p>
            </div>
          </div>
        </div>

        <!-- Appearance Section -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden mb-6 hover:shadow-md transition-shadow">
          <div class="bg-gradient-to-r from-amber-50 to-orange-50 px-6 py-4 border-b border-gray-200">
            <h2 class="text-lg font-bold text-amber-900">🎨 Appearance</h2>
          </div>
          <div class="p-6">
            <label class="block text-sm font-semibold text-gray-700 mb-4">Theme Preference</label>
            <div class="grid grid-cols-3 gap-4">
              <label class="relative flex items-center p-4 border-2 rounded-lg cursor-pointer transition-all"
                [class.border-blue-600]="settings.theme === 'light'"
                [class.bg-blue-50]="settings.theme === 'light'"
                [class.border-gray-200]="settings.theme !== 'light'"
                [class.hover:border-blue-300]="settings.theme !== 'light'">
                <input type="radio" name="theme" value="light"
                  [(ngModel)]="settings.theme" (ngModelChange)="persist()"
                  class="w-4 h-4 accent-blue-600" />
                <span class="ml-3 font-medium text-gray-900">☀️ Light</span>
              </label>

              <label class="relative flex items-center p-4 border-2 rounded-lg cursor-pointer transition-all"
                [class.border-blue-600]="settings.theme === 'dark'"
                [class.bg-blue-50]="settings.theme === 'dark'"
                [class.border-gray-200]="settings.theme !== 'dark'"
                [class.hover:border-gray-300]="settings.theme !== 'dark'">
                <input type="radio" name="theme" value="dark"
                  [(ngModel)]="settings.theme" (ngModelChange)="persist()"
                  class="w-4 h-4 accent-blue-600" />
                <span class="ml-3 font-medium text-gray-900">🌙 Dark</span>
              </label>

              <label class="relative flex items-center p-4 border-2 rounded-lg cursor-pointer transition-all"
                [class.border-blue-600]="settings.theme === 'auto'"
                [class.bg-blue-50]="settings.theme === 'auto'"
                [class.border-gray-200]="settings.theme !== 'auto'"
                [class.hover:border-purple-300]="settings.theme !== 'auto'">
                <input type="radio" name="theme" value="auto"
                  [(ngModel)]="settings.theme" (ngModelChange)="persist()"
                  class="w-4 h-4 accent-blue-600" />
                <span class="ml-3 font-medium text-gray-900">🔄 Auto</span>
              </label>
            </div>
          </div>
        </div>

        <!-- Data Management Section -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden mb-6 hover:shadow-md transition-shadow">
          <div class="bg-gradient-to-r from-red-50 to-orange-50 px-6 py-4 border-b border-gray-200">
            <h2 class="text-lg font-bold text-red-900">📦 Data Management</h2>
          </div>
          <div class="p-6 space-y-4">
            <button (click)="exportHistory()" class="w-full px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg hover:from-blue-700 hover:to-blue-800 font-semibold shadow-md hover:shadow-lg transition-all transform hover:scale-105">
              ⬇️ Export History
            </button>

            <button (click)="backupSettings()" class="w-full px-6 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 font-semibold transition-all transform hover:scale-105">
              💾 Backup Settings
            </button>

            <button (click)="clearHistory()" class="w-full px-6 py-3 bg-red-50 text-red-600 border border-red-200 rounded-lg hover:bg-red-100 hover:border-red-300 font-semibold transition-all">
              🗑️ Clear History
            </button>

            <div class="bg-red-50 p-4 rounded-lg border border-red-200">
              <p class="text-sm text-red-900"><strong>⚠️ Warning:</strong> Clearing history cannot be undone. Export first if needed.</p>
            </div>
          </div>
        </div>

        <!-- Info Card -->
        <div class="bg-gradient-to-r from-blue-50 to-cyan-50 p-6 rounded-xl border border-blue-200 shadow-sm">
          <div class="flex items-start gap-4">
            <div class="text-2xl">📄</div>
            <div>
              <p class="font-semibold text-blue-900">Settings Auto-Save</p>
              <p class="text-sm text-blue-800 mt-1">Your preferences are saved automatically to browser local storage. No additional action required.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: []
})
export class SettingsComponent implements OnInit {
  settings!: AppSettings;
  saveMessage = '';
  private saveTimeout: any;

  constructor(
    private settingsService: SettingsService,
    private documentService: DocumentService
  ) {}

  ngOnInit(): void {
    this.settings = { ...this.settingsService.current };
  }

  persist(): void {
    this.settingsService.update(this.settings);
    this.showSaveMessage('✓ Settings saved');
  }

  clearHistory(): void {
    if (confirm('Clear all document history? This cannot be undone.')) {
      this.documentService.clearHistory();
      this.showSaveMessage('✓ History cleared');
    }
  }

  exportHistory(): void {
    const history = this.documentService.getHistory();
    const json = JSON.stringify(history, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `doc-intelligence-history-${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
    this.showSaveMessage('✓ History exported');
  }

  backupSettings(): void {
    const json = JSON.stringify(this.settings, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `doc-intelligence-settings-${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
    this.showSaveMessage('✓ Settings backed up');
  }

  private showSaveMessage(msg: string): void {
    this.saveMessage = msg;
    if (this.saveTimeout) clearTimeout(this.saveTimeout);
    this.saveTimeout = setTimeout(() => (this.saveMessage = ''), 2500);
  }
}
