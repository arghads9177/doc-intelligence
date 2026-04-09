import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { NotificationService, Toast } from '../services/notification.service';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive],
  template: `
    <header class="sticky top-0 z-40 bg-white shadow-md border-b border-gray-200" role="banner">
      <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <!-- Logo & Branding -->
          <div class="flex-shrink-0">
            <a href="/" class="flex items-center gap-3 group">
              <div class="w-10 h-10 bg-gradient-to-br from-blue-600 to-blue-700 rounded-lg flex items-center justify-center shadow-md group-hover:shadow-lg transition-all transform group-hover:scale-110">
                <span class="text-white font-bold text-lg">📄</span>
              </div>
              <div>
                <span class="text-lg font-bold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">DocIntel</span>
                <p class="text-xs text-gray-500 leading-none">Intelligence</p>
              </div>
            </a>
          </div>

          <!-- Navigation Links -->
          <div class="hidden md:flex gap-1">
            <a
              routerLink="/upload"
              routerLinkActive="active"
              [routerLinkActiveOptions]="{ exact: true }"
              class="px-4 py-2 rounded-lg text-sm font-semibold text-gray-700 hover:bg-blue-50 hover:text-blue-600 transition-all duration-200 relative group"
            >
              📤 Upload
              <span class="absolute bottom-0 left-0 w-0 h-1 bg-gradient-to-r from-blue-600 to-blue-500 rounded-full group-hover:w-full transition-all duration-300"></span>
            </a>
            <a
              routerLink="/dashboard"
              routerLinkActive="active"
              [routerLinkActiveOptions]="{ exact: true }"
              class="px-4 py-2 rounded-lg text-sm font-semibold text-gray-700 hover:bg-blue-50 hover:text-blue-600 transition-all duration-200 relative group"
            >
              📊 Dashboard
              <span class="absolute bottom-0 left-0 w-0 h-1 bg-gradient-to-r from-blue-600 to-blue-500 rounded-full group-hover:w-full transition-all duration-300"></span>
            </a>
            <a
              routerLink="/history"
              routerLinkActive="active"
              [routerLinkActiveOptions]="{ exact: true }"
              class="px-4 py-2 rounded-lg text-sm font-semibold text-gray-700 hover:bg-blue-50 hover:text-blue-600 transition-all duration-200 relative group"
            >
              📋 History
              <span class="absolute bottom-0 left-0 w-0 h-1 bg-gradient-to-r from-blue-600 to-blue-500 rounded-full group-hover:w-full transition-all duration-300"></span>
            </a>
            <a
              routerLink="/comparison"
              routerLinkActive="active"
              [routerLinkActiveOptions]="{ exact: true }"
              class="px-4 py-2 rounded-lg text-sm font-semibold text-gray-700 hover:bg-blue-50 hover:text-blue-600 transition-all duration-200 relative group"
            >
              🔍 Compare
              <span class="absolute bottom-0 left-0 w-0 h-1 bg-gradient-to-r from-blue-600 to-blue-500 rounded-full group-hover:w-full transition-all duration-300"></span>
            </a>
            <a
              routerLink="/settings"
              routerLinkActive="active"
              [routerLinkActiveOptions]="{ exact: true }"
              class="px-4 py-2 rounded-lg text-sm font-semibold text-gray-700 hover:bg-blue-50 hover:text-blue-600 transition-all duration-200 relative group"
            >
              ⚙️ Settings
              <span class="absolute bottom-0 left-0 w-0 h-1 bg-gradient-to-r from-blue-600 to-blue-500 rounded-full group-hover:w-full transition-all duration-300"></span>
            </a>
          </div>

          <!-- Mobile Menu Button -->
          <button class="md:hidden p-2 rounded-lg text-gray-600 hover:bg-gray-100 hover:text-gray-900 transition-all transform active:scale-95">
            ☰
          </button>
        </div>
      </nav>
    </header>
  `,
  styles: [`
    :host ::ng-deep a.active {
      @apply bg-blue-100 text-blue-600;
    }
  `]
})
export class HeaderComponent {}

@Component({
  selector: 'app-footer',
  standalone: true,
  imports: [CommonModule],
  template: `
    <footer class="bg-gradient-to-b from-gray-900 to-black text-gray-300 py-12 mt-16 border-t border-gray-800">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- Main Content -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-12 mb-12">
          <!-- About Section -->
          <div class="group">
            <div class="flex items-center gap-2 mb-4">
              <span class="text-2xl">📄</span>
              <h3 class="text-xl font-bold text-white">DocIntel</h3>
            </div>
            <p class="text-sm text-gray-400 leading-relaxed">
              AI-powered document analysis and intelligent data extraction. Transform your documents into structured data effortlessly.
            </p>
            <div class="flex gap-4 mt-6">
              <a href="#" class="inline-flex items-center justify-center w-10 h-10 rounded-lg bg-gray-800 text-gray-400 hover:bg-blue-600 hover:text-white transition-all transform hover:scale-110">
                f
              </a>
              <a href="#" class="inline-flex items-center justify-center w-10 h-10 rounded-lg bg-gray-800 text-gray-400 hover:bg-blue-600 hover:text-white transition-all transform hover:scale-110">
                𝕏
              </a>
              <a href="#" class="inline-flex items-center justify-center w-10 h-10 rounded-lg bg-gray-800 text-gray-400 hover:bg-blue-600 hover:text-white transition-all transform hover:scale-110">
                in
              </a>
            </div>
          </div>

          <!-- Quick Links Section -->
          <div>
            <h3 class="text-white font-bold mb-4 flex items-center gap-2">
              <span class="w-1 h-6 bg-gradient-to-b from-blue-600 to-blue-400 rounded-full"></span>
              Quick Links
            </h3>
            <ul class="text-sm space-y-3">
              <li>
                <a href="#" class="text-gray-400 hover:text-white hover:translate-x-1 transition-all inline-flex items-center gap-2">
                  <span>→</span>
                  <span>Documentation</span>
                </a>
              </li>
              <li>
                <a href="#" class="text-gray-400 hover:text-white hover:translate-x-1 transition-all inline-flex items-center gap-2">
                  <span>→</span>
                  <span>API Reference</span>
                </a>
              </li>
              <li>
                <a href="#" class="text-gray-400 hover:text-white hover:translate-x-1 transition-all inline-flex items-center gap-2">
                  <span>→</span>
                  <span>Support Center</span>
                </a>
              </li>
              <li>
                <a href="#" class="text-gray-400 hover:text-white hover:translate-x-1 transition-all inline-flex items-center gap-2">
                  <span>→</span>
                  <span>Blog</span>
                </a>
              </li>
            </ul>
          </div>

          <!-- Legal Section -->
          <div>
            <h3 class="text-white font-bold mb-4 flex items-center gap-2">
              <span class="w-1 h-6 bg-gradient-to-b from-green-600 to-green-400 rounded-full"></span>
              Legal & Compliance
            </h3>
            <ul class="text-sm space-y-3">
              <li>
                <a href="#" class="text-gray-400 hover:text-white hover:translate-x-1 transition-all inline-flex items-center gap-2">
                  <span>→</span>
                  <span>Privacy Policy</span>
                </a>
              </li>
              <li>
                <a href="#" class="text-gray-400 hover:text-white hover:translate-x-1 transition-all inline-flex items-center gap-2">
                  <span>→</span>
                  <span>Terms of Service</span>
                </a>
              </li>
              <li>
                <a href="#" class="text-gray-400 hover:text-white hover:translate-x-1 transition-all inline-flex items-center gap-2">
                  <span>→</span>
                  <span>Cookie Policy</span>
                </a>
              </li>
              <li>
                <a href="#" class="text-gray-400 hover:text-white hover:translate-x-1 transition-all inline-flex items-center gap-2">
                  <span>→</span>
                  <span>Data Processing</span>
                </a>
              </li>
            </ul>
          </div>
        </div>

        <!-- Divider -->
        <div class="border-t border-gray-800 my-8"></div>

        <!-- Bottom Section -->
        <div class="flex flex-col md:flex-row justify-between items-center gap-6 text-sm">
          <p class="text-gray-500">
            {{ currentYear }} &copy; Document Intelligence. All rights reserved.
          </p>
          <p class="text-gray-500">
            Proudly powered by <span class="text-blue-400 font-semibold">Angular</span> &amp; <span class="text-blue-300 font-semibold">Tailwind CSS</span>
          </p>
          <p class="text-gray-500">
            v1.0.0 • Built with <span class="text-red-500">❤</span> for intelligence
          </p>
        </div>
      </div>
    </footer>
  `,
  styles: []
})
export class FooterComponent {
  currentYear = new Date().getFullYear();
}

@Component({
  selector: 'app-toast-container',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="fixed top-4 right-4 space-y-2 z-50">
      <div
        *ngFor="let toast of toasts"
        class="px-4 py-3 rounded-lg shadow-lg animate-slide-in"
        [ngClass]="{
          'bg-green-50 text-green-800 border border-green-200': toast.type === 'success',
          'bg-red-50 text-red-800 border border-red-200': toast.type === 'error',
          'bg-yellow-50 text-yellow-800 border border-yellow-200': toast.type === 'warning',
          'bg-blue-50 text-blue-800 border border-blue-200': toast.type === 'info'
        }"
      >
        <div class="flex items-center justify-between gap-3">
          <p class="text-sm font-medium">{{ toast.message }}</p>
          <button
            (click)="removeToast(toast.id)"
            class="text-lg leading-none hover:opacity-70"
          >
            ✕
          </button>
        </div>
      </div>
    </div>
  `,
  styles: [
    `
      @keyframes slideIn {
        from {
          transform: translateX(400px);
          opacity: 0;
        }
        to {
          transform: translateX(0);
          opacity: 1;
        }
      }

      .animate-slide-in {
        animation: slideIn 0.3s ease-out;
      }
    `
  ]
})
export class ToastContainerComponent implements OnInit {
  toasts: Toast[] = [];

  constructor(private notificationService: NotificationService) {}

  ngOnInit(): void {
    this.notificationService.toasts$.subscribe((toasts: Toast[]) => {
      this.toasts = toasts;
    });
  }

  removeToast(id: string): void {
    this.notificationService.removeToast(id);
  }
}
