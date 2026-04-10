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
    ).subscribe(batches => {
      this.calculateStats(batches);
      // Transform batches to document display format
      this.recentDocuments = batches.slice(0, 5).reverse().flatMap(batch => 
        batch.documents.map(doc => ({
          id: batch.id,
          name: doc.filename,
          type: doc.documentType || 'unknown',
          status: batch.completedAt ? 'completed' : 'processing',
          date: batch.createdAt,
          processingTime: 0, // Will be calculated or fetched from analysis
          confidence: doc.documentTypeConfidence || 0
        }))
      );
      this.generateProcessingStats(batches);
    });
  }

  private loadDashboardData(): void {
    // Simulated data - in production, fetch from backend
    // Use recent dates within the last 7 days for mock data
    const mockDocuments = [
      { id: 1, name: 'Invoice_001.pdf', type: 'invoice', status: 'completed', date: new Date(Date.now() - 86400000), processingTime: 12 }, // 1 day ago
      { id: 2, name: 'Receipt_Bank.pdf', type: 'receipt', status: 'completed', date: new Date(Date.now() - 172800000), processingTime: 8 }, // 2 days ago
      { id: 3, name: 'Contract_Q1.pdf', type: 'contract', status: 'completed', date: new Date(Date.now() - 259200000), processingTime: 15 }, // 3 days ago
      { id: 4, name: 'Invoice_002.pdf', type: 'invoice', status: 'completed', date: new Date(Date.now() - 345600000), processingTime: 11 }, // 4 days ago
      { id: 5, name: 'Receipt_Store.pdf', type: 'receipt', status: 'completed', date: new Date(Date.now() - 432000000), processingTime: 9 } // 5 days ago
    ];

    this.calculateStats(mockDocuments);
    this.recentDocuments = mockDocuments.slice(0, 5).reverse();
    this.generateProcessingStats(mockDocuments);
  }

  private calculateStats(batches: any[]): void {
    // Handle both DocumentBatch and mock document structures
    let totalDocs = 0;
    let processedDocs = 0;
    let totalProcessingTime = 0;
    let docCount = 0;

    batches.forEach(batch => {
      if (batch.totalDocuments !== undefined) {
        // This is a DocumentBatch structure
        totalDocs += batch.totalDocuments;
        processedDocs += batch.processedDocuments;
      } else if (batch.status !== undefined) {
        // This is a mock document structure
        totalDocs++;
        if (batch.status === 'completed') processedDocs++;
        if (batch.processingTime) {
          totalProcessingTime += batch.processingTime;
          docCount++;
        }
      }
    });

    const successRate = totalDocs > 0 ? ((processedDocs / totalDocs) * 100).toFixed(1) : 0;
    
    // For processing time, use analysis time or avg from available data
    let avgProcessingTime = '0';
    if (docCount > 0) {
      avgProcessingTime = (totalProcessingTime / docCount).toFixed(1);
    }

    const typeDistribution = this.calculateTypeDistribution(batches);

    this.stats = [
      {
        label: 'Total Documents',
        value: totalDocs,
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

  private calculateTypeDistribution(batches: any[]): DocumentTypeStat[] {
    const typeCounts: { [key: string]: number } = {};
    let totalDocs = 0;

    batches.forEach(batch => {
      if (batch.documents && Array.isArray(batch.documents)) {
        // DocumentBatch structure
        batch.documents.forEach((doc: any) => {
          totalDocs++;
          const type = (doc.documentType || 'unknown').toLowerCase();
          typeCounts[type] = (typeCounts[type] || 0) + 1;
        });
      } else if (batch.type !== undefined) {
        // Mock document structure
        totalDocs++;
        const type = batch.type || 'unknown';
        typeCounts[type] = (typeCounts[type] || 0) + 1;
      }
    });

    const colors = ['bg-blue-500', 'bg-green-500', 'bg-orange-500', 'bg-purple-500', 'bg-red-500'];
    
    return Object.entries(typeCounts)
      .map((entry, index) => ({
        type: entry[0],
        count: entry[1],
        percentage: totalDocs > 0 ? Math.round((entry[1] / totalDocs) * 100) : 0,
        color: colors[index % colors.length]
      }))
      .sort((a, b) => b.count - a.count);
  }

  private generateProcessingStats(batches: any[]): void {
    // Generate last 7 days of stats - use a helper function for consistent date formatting
    const stats: { [key: string]: number } = {};
    
    for (let i = 6; i >= 0; i--) {
      const date = new Date();
      date.setDate(date.getDate() - i);
      const dateStr = this.formatDateForChart(date);
      stats[dateStr] = 0;
    }

    batches.forEach((batch) => {
      let dateToCheck: Date | null = null;

      if (batch.createdAt) {
        // DocumentBatch structure
        dateToCheck = new Date(batch.createdAt);
      } else if (batch.date) {
        // Mock document structure
        dateToCheck = new Date(batch.date);
      }

      if (dateToCheck) {
        const dateStr = this.formatDateForChart(dateToCheck);
        
        if (dateStr in stats) {
          // For DocumentBatch, count all documents in the batch, not the batch itself
          if (batch.totalDocuments !== undefined) {
            stats[dateStr] += batch.totalDocuments;
          } else {
            stats[dateStr]++;
          }
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

  private formatDateForChart(date: Date): string {
    // Ensure consistent date formatting for chart labels
    // Use local date string in 'Short Mon Day' format
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  }

  getTypeIcon(type: string): string {
    const icons: { [key: string]: string } = {
      'invoice': '📋',
      'receipt': '🧾',
      'contract': '📜',
      'unknown': '📄'
    };
    return icons[(type || 'unknown').toLowerCase()] || icons['unknown'];
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
