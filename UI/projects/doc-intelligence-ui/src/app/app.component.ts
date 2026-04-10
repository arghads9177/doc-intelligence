import { Component, OnInit, OnDestroy } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HeaderComponent, FooterComponent, ToastContainerComponent } from './shared/components/layout.component';
import { SettingsService } from './shared/services/settings.service';
import { DocumentService } from './shared/services/document.service';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, HeaderComponent, FooterComponent, ToastContainerComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit, OnDestroy {
  title = 'Document Intelligence';
  private destroy$ = new Subject<void>();
  private mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

  constructor(
    private settingsService: SettingsService,
    private documentService: DocumentService
  ) {}

  ngOnInit(): void {
    // Apply theme reactively whenever settings change
    this.settingsService.settings$.pipe(takeUntil(this.destroy$)).subscribe(settings => {
      this.applyTheme(settings.theme);
      this.enforceAutoClear(settings.autoClearHistory);
    });

    // Also react to OS-level prefers-color-scheme changes when theme is 'auto'
    this.mediaQuery.addEventListener('change', () => {
      const theme = this.settingsService.current.theme;
      if (theme === 'auto') this.applyTheme('auto');
    });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  private applyTheme(theme: 'light' | 'dark' | 'auto'): void {
    const html = document.documentElement;
    const prefersDark = this.mediaQuery.matches;
    if (theme === 'dark' || (theme === 'auto' && prefersDark)) {
      html.classList.add('dark');
    } else {
      html.classList.remove('dark');
    }
  }

  private enforceAutoClear(autoClearHistory: string): void {
    if (autoClearHistory === 'never') return;
    const msMap: Record<string, number> = {
      '1week':   7  * 24 * 60 * 60 * 1000,
      '1month':  30 * 24 * 60 * 60 * 1000,
      '3months': 90 * 24 * 60 * 60 * 1000,
    };
    const maxAge = msMap[autoClearHistory];
    if (!maxAge) return;
    const cutoff = Date.now() - maxAge;
    const history = this.documentService.getHistory();
    const hasOld = history.some(b => new Date(b.createdAt).getTime() < cutoff);
    if (hasOld) {
      const filtered = history.filter(b => new Date(b.createdAt).getTime() >= cutoff);
      // Replace history with only recent items
      this.documentService.replaceHistory(filtered);
    }
  }
}
