import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { DocumentService } from '../../shared/services/document.service';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

interface StatCard {
  label: string;
  value: number | string;
  unit?: string;
  icon: string;
  color: string;
  bgColor: string;
}

interface DocumentTypeStat {
  type: string;
  count: number;
  percentage: number;
  color: string;
}

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit, OnDestroy {
  stats: StatCard[] = [];
  documentTypeStats: DocumentTypeStat[] = [];
  recentDocuments: any[] = [];
  processingStats: { timestamp: string; count: number }[] = [];
  peakDayCount: number = 0;
  totalWeekCount: number = 0;
  
  private destroy$ = new Subject<void>();

  constructor(private documentService: DocumentService) {}

  ngOnInit(): void {
    this.loadDashboardData();
    this.subscribeToDocuments();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  private subscribeToDocuments(): void {
    this.documentService.documentHistory$.pipe(
      takeUntil(this.destroy$)
    ).subscribe(documents => {
      this.calculateStats(documents);
      this.recentDocuments = documents.slice(0, 5).reverse();
      this.generateProcessingStats(documents);
    });
  }

  private loadDashboardData(): void {
    // Simulated data - in production, fetch from backend
    const mockDocuments = [
      { id: 1, name: 'Invoice_001.pdf', type: 'invoice', status: 'completed', date: new Date(Date.now() - 1000000), processingTime: 12 },
      { id: 2, name: 'Receipt_Bank.pdf', type: 'receipt', status: 'completed', date: new Date(Date.now() - 2000000), processingTime: 8 },
      { id: 3, name: 'Contract_Q1.pdf', type: 'contract', status: 'completed', date: new Date(Date.now() - 3000000), processingTime: 15 },
      { id: 4, name: 'Invoice_002.pdf', type: 'invoice', status: 'completed', date: new Date(Date.now() - 4000000), processingTime: 11 },
      { id: 5, name: 'Receipt_Store.pdf', type: 'receipt', status: 'completed', date: new Date(Date.now() - 5000000), processingTime: 9 }
    ];

    this.calculateStats(mockDocuments);
    this.recentDocuments = mockDocuments.slice(0, 5).reverse();
    this.generateProcessingStats(mockDocuments);
  }

  private calculateStats(documents: any[]): void {
    const total = documents.length;
    const completed = documents.filter(d => d.status === 'completed').length;
    const successRate = total > 0 ? ((completed / total) * 100).toFixed(1) : 0;
    const avgProcessingTime = total > 0 
      ? (documents.reduce((sum, d) => sum + (d.processingTime || 0), 0) / total).toFixed(1)
      : 0;

    const typeDistribution = this.calculateTypeDistribution(documents);

    this.stats = [
      {
        label: 'Total Documents',
        value: total,
        icon: '📄',
        color: 'text-blue-600',
        bgColor: 'bg-blue-50'
      },
      {
        label: 'Success Rate',
        value: successRate,
        unit: '%',
        icon: '✓',
        color: 'text-green-600',
        bgColor: 'bg-green-50'
      },
      {
        label: 'Avg Processing',
        value: avgProcessingTime,
        unit: 's',
        icon: '⏱️',
        color: 'text-purple-600',
        bgColor: 'bg-purple-50'
      },
      {
        label: 'Document Types',
        value: typeDistribution.length,
        icon: '📊',
        color: 'text-orange-600',
        bgColor: 'bg-orange-50'
      }
    ];

    this.documentTypeStats = typeDistribution;
  }

  private calculateTypeDistribution(documents: any[]): DocumentTypeStat[] {
    const typeCounts: { [key: string]: number } = {};
    documents.forEach(doc => {
      const type = doc.type || 'unknown';
      typeCounts[type] = (typeCounts[type] || 0) + 1;
    });

    const total = documents.length;
    const colors = ['bg-blue-500', 'bg-green-500', 'bg-orange-500', 'bg-purple-500', 'bg-red-500'];
    
    return Object.entries(typeCounts)
      .map((entry, index) => ({
        type: entry[0],
        count: entry[1],
        percentage: total > 0 ? Math.round((entry[1] / total) * 100) : 0,
        color: colors[index % colors.length]
      }))
      .sort((a, b) => b.count - a.count);
  }

  private generateProcessingStats(documents: any[]): void {
    // Generate last 7 days of stats
    const stats: { [key: string]: number } = {};
    
    for (let i = 6; i >= 0; i--) {
      const date = new Date();
      date.setDate(date.getDate() - i);
      const dateStr = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
      stats[dateStr] = 0;
    }

    documents.forEach(doc => {
      if (doc.date) {
        const dateStr = new Date(doc.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        if (dateStr in stats) {
          stats[dateStr]++;
        }
      }
    });

    this.processingStats = Object.entries(stats).map(([timestamp, count]) => ({
      timestamp,
      count
    }));
    
    // Compute peak day and total week count
    this.peakDayCount = this.getMaxCount();
    this.totalWeekCount = this.processingStats.reduce((sum, s) => sum + s.count, 0);
  }

  getTypeIcon(type: string): string {
    const icons: { [key: string]: string } = {
      'invoice': '🧾',
      'receipt': '🛒',
      'contract': '⚖️',
      'default': '📄'
    };
    return icons[type] || icons['default'];
  }

  formatDate(date: Date): string {
    return new Date(date).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  }

  formatTime(seconds: number): string {
    return `${seconds}s`;
  }

  getMaxCount(): number {
    return Math.max(...this.processingStats.map(s => s.count), 1);
  }

  getBarHeight(count: number): number {
    const maxCount = this.getMaxCount();
    return maxCount > 0 ? (count / maxCount) * 100 : 0;
  }
}
