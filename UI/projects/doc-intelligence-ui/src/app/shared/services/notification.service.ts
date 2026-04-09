import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

export interface Toast {
  id: string;
  message: string;
  type: 'success' | 'error' | 'warning' | 'info';
  duration?: number; // ms, 0 = persistent
  timestamp: Date;
}

@Injectable({
  providedIn: 'root'
})
export class NotificationService {
  private toastsSubject = new BehaviorSubject<Toast[]>([]);
  toasts$ = this.toastsSubject.asObservable();

  private idCounter = 0;
  private readonly DEFAULT_DURATION = 5000; // 5 seconds

  constructor() {}

  /**
   * Show success notification
   */
  success(message: string, duration = this.DEFAULT_DURATION): string {
    return this.addToast(message, 'success', duration);
  }

  /**
   * Show error notification
   */
  error(message: string, duration = this.DEFAULT_DURATION): string {
    return this.addToast(message, 'error', duration);
  }

  /**
   * Show warning notification
   */
  warning(message: string, duration = this.DEFAULT_DURATION): string {
    return this.addToast(message, 'warning', duration);
  }

  /**
   * Show info notification
   */
  info(message: string, duration = this.DEFAULT_DURATION): string {
    return this.addToast(message, 'info', duration);
  }

  /**
   * Add custom toast
   */
  private addToast(message: string, type: Toast['type'], duration?: number): string {
    const id = `toast-${++this.idCounter}-${Date.now()}`;
    const toast: Toast = {
      id,
      message,
      type,
      duration: duration ?? this.DEFAULT_DURATION,
      timestamp: new Date()
    };

    const current = this.toastsSubject.value;
    this.toastsSubject.next([...current, toast]);

    // Auto-remove if duration is set
    if (duration !== 0) {
      setTimeout(() => this.removeToast(id), duration ?? this.DEFAULT_DURATION);
    }

    return id;
  }

  /**
   * Remove toast by ID
   */
  removeToast(id: string): void {
    const current = this.toastsSubject.value.filter((t) => t.id !== id);
    this.toastsSubject.next(current);
  }

  /**
   * Clear all toasts
   */
  clearAll(): void {
    this.toastsSubject.next([]);
  }

  /**
   * Get current toasts
   */
  getToasts(): Toast[] {
    return this.toastsSubject.value;
  }
}
