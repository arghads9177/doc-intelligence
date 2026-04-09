import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { DocumentService } from '../../shared/services/document.service';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

interface ComparisonField {
  fieldName: string;
  value1: string;
  value2: string;
  confidence1: number;
  confidence2: number;
  isDifferent: boolean;
}

interface ComparisonData {
  document1: any;
  document2: any;
  fields: ComparisonField[];
  similarities: number;
}

@Component({
  selector: 'app-comparison',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './comparison.component.html',
  styleUrls: ['./comparison.component.scss']
})
export class ComparisonComponent implements OnInit, OnDestroy {
  document1: any = null;
  document2: any = null;
  comparisonFields: ComparisonField[] = [];
  comparisonData: ComparisonData | null = null;
  availableDocuments: any[] = [];
  selectedDoc1Id: string | null = null;
  selectedDoc2Id: string | null = null;
  showDifferencesOnly = false;
  similarityPercentage = 0;
  viewMode: 'side-by-side' | 'diff' = 'side-by-side';

  private destroy$ = new Subject<void>();

  constructor(
    private documentService: DocumentService,
    private route: ActivatedRoute
  ) {}

  ngOnInit(): void {
    this.loadAvailableDocuments();
    this.loadSelectedDocuments();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  private loadAvailableDocuments(): void {
    // Mock data - in production, fetch from backend
    this.availableDocuments = [
      { id: '1', name: 'Invoice_001.pdf', type: 'invoice', date: new Date(Date.now() - 1000000) },
      { id: '2', name: 'Invoice_002.pdf', type: 'invoice', date: new Date(Date.now() - 2000000) },
      { id: '3', name: 'Receipt_001.pdf', type: 'receipt', date: new Date(Date.now() - 3000000) },
      { id: '4', name: 'Contract_001.pdf', type: 'contract', date: new Date(Date.now() - 4000000) }
    ];
  }

  private loadSelectedDocuments(): void {
    this.route.queryParams.pipe(
      takeUntil(this.destroy$)
    ).subscribe(params => {
      const doc1Id = params['doc1'];
      const doc2Id = params['doc2'];

      if (doc1Id && doc2Id) {
        this.selectDocuments(doc1Id, doc2Id);
      }
    });
  }

  selectDocuments(doc1Id: string, doc2Id: string): void {
    this.selectedDoc1Id = doc1Id;
    this.selectedDoc2Id = doc2Id;

    this.document1 = this.availableDocuments.find(d => d.id === doc1Id);
    this.document2 = this.availableDocuments.find(d => d.id === doc2Id);

    if (this.document1 && this.document2) {
      this.performComparison();
    }
  }

  private performComparison(): void {
    // Mock comparison data
    const mockFields: ComparisonField[] = [
      {
        fieldName: 'Company Name',
        value1: 'Acme Corporation Inc.',
        value2: 'ACME Corporation',
        confidence1: 0.95,
        confidence2: 0.92,
        isDifferent: false
      },
      {
        fieldName: 'Invoice Amount',
        value1: '$1,500.00',
        value2: 'USD 1500',
        confidence1: 0.98,
        confidence2: 0.96,
        isDifferent: false
      },
      {
        fieldName: 'Invoice Date',
        value1: '2024-04-01',
        value2: '04/01/2024',
        confidence1: 0.99,
        confidence2: 0.99,
        isDifferent: false
      },
      {
        fieldName: 'Payment Terms',
        value1: 'Net 30',
        value2: 'Due within 30 days',
        confidence1: 0.87,
        confidence2: 0.85,
        isDifferent: true
      },
      {
        fieldName: 'Purchase Order',
        value1: 'PO-2024-001',
        value2: 'Not found',
        confidence1: 0.91,
        confidence2: 0.0,
        isDifferent: true
      },
      {
        fieldName: 'Department',
        value1: 'Sales',
        value2: 'Sales',
        confidence1: 0.88,
        confidence2: 0.88,
        isDifferent: false
      }
    ];

    this.comparisonFields = mockFields;
    const totalFields = mockFields.length;
    const similarFields = mockFields.filter(f => !f.isDifferent).length;
    this.similarityPercentage = Math.round((similarFields / totalFields) * 100);

    this.comparisonData = {
      document1: this.document1,
      document2: this.document2,
      fields: mockFields,
      similarities: Math.round((similarFields / totalFields) * 100)
    };
  }

  toggleDifferencesOnly(): void {
    this.showDifferencesOnly = !this.showDifferencesOnly;
  }

  getDisplayedFields(): ComparisonField[] {
    if (this.showDifferencesOnly) {
      return this.comparisonFields.filter(f => f.isDifferent);
    }
    return this.comparisonFields;
  }

  getConfidenceColor(confidence: number): string {
    if (confidence >= 0.9) return 'text-green-600';
    if (confidence >= 0.7) return 'text-yellow-600';
    return 'text-red-600';
  }

  getConfidenceBgColor(confidence: number): string {
    if (confidence >= 0.9) return 'bg-green-100';
    if (confidence >= 0.7) return 'bg-yellow-100';
    return 'bg-red-100';
  }

  downloadComparison(): void {
    if (!this.comparisonData) return;

    const csv = this.generateCSV();
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `comparison_${this.document1?.name}_${this.document2?.name}.csv`;
    link.click();
  }

  private generateCSV(): string {
    let csv = 'Field,Document 1 Value,Confidence,Document 2 Value,Confidence,Different\n';
    
    this.comparisonFields.forEach(field => {
      csv += `"${field.fieldName}","${field.value1}",${field.confidence1},"${field.value2}",${field.confidence2},${field.isDifferent ? 'Yes' : 'No'}\n`;
    });

    return csv;
  }

  formatDate(date: Date): string {
    return new Date(date).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  }

  getDocumentIcon(type: string): string {
    const icons: { [key: string]: string } = {
      'invoice': '🧾',
      'receipt': '🛒',
      'contract': '⚖️',
      'default': '📄'
    };
    return icons[type] || icons['default'];
  }

  setViewMode(mode: 'side-by-side' | 'diff'): void {
    this.viewMode = mode;
  }

  getMatchingFieldsCount(): number {
    return this.comparisonFields.filter(f => !f.isDifferent).length;
  }

  getDifferencesCount(): number {
    return this.comparisonFields.filter(f => f.isDifferent).length;
  }
}
