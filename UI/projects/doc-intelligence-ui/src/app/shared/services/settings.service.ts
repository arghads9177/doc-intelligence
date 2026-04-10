import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

export interface AppSettings {
  includeValidation: boolean;
  includeSummary: boolean;
  batchSize: number;
  autoClearHistory: string;
  theme: 'light' | 'dark' | 'auto';
}

const DEFAULT_SETTINGS: AppSettings = {
  includeValidation: true,
  includeSummary: true,
  batchSize: 10,
  autoClearHistory: 'never',
  theme: 'light'
};

const STORAGE_KEY = 'doc_intelligence_settings';

@Injectable({
  providedIn: 'root'
})
export class SettingsService {
  private settingsSubject = new BehaviorSubject<AppSettings>(this.loadFromStorage());
  settings$ = this.settingsSubject.asObservable();

  get current(): AppSettings {
    return this.settingsSubject.value;
  }

  update(partial: Partial<AppSettings>): void {
    const updated = { ...this.settingsSubject.value, ...partial };
    this.settingsSubject.next(updated);
    this.saveToStorage(updated);
  }

  private loadFromStorage(): AppSettings {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        return { ...DEFAULT_SETTINGS, ...JSON.parse(stored) };
      }
    } catch {
      // ignore parse errors
    }
    return { ...DEFAULT_SETTINGS };
  }

  private saveToStorage(settings: AppSettings): void {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(settings));
    } catch {
      // ignore storage errors
    }
  }
}
