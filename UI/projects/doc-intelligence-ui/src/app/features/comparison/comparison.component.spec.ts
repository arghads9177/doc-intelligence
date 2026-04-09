import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ComparisonComponent } from './comparison.component';
import { DocumentService } from '../../shared/services/document.service';
import { ActivatedRoute } from '@angular/router';
import { of } from 'rxjs';

describe('ComparisonComponent', () => {
  let component: ComparisonComponent;
  let fixture: ComponentFixture<ComparisonComponent>;
  let documentServiceMock: any;

  beforeEach(async () => {
    documentServiceMock = {
      documentHistory$: of([])
    };

    await TestBed.configureTestingModule({
      imports: [ComparisonComponent],
      providers: [
        { provide: DocumentService, useValue: documentServiceMock },
        {
          provide: ActivatedRoute,
          useValue: {
            queryParams: of({ doc1: '1', doc2: '2' })
          }
        }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(ComparisonComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('Document Selection', () => {
    it('should load available documents', () => {
      expect(component.availableDocuments.length).toBeGreaterThan(0);
    });

    it('should select two documents for comparison', () => {
      component.selectDocuments('1', '2');
      expect(component.document1).toBeDefined();
      expect(component.document2).toBeDefined();
    });

    it('should trigger comparison on document selection', () => {
      component.selectDocuments('1', '2');
      expect(component.comparisonData).toBeDefined();
    });
  });

  describe('Comparison Data', () => {
    beforeEach(() => {
      component.selectDocuments('1', '2');
    });

    it('should have comparison fields', () => {
      expect(component.comparisonFields.length).toBeGreaterThan(0);
    });

    it('should calculate similarity percentage', () => {
      expect(component.similarityPercentage).toBeGreaterThanOrEqual(0);
      expect(component.similarityPercentage).toBeLessThanOrEqual(100);
    });

    it('should identify different fields', () => {
      const differentFields = component.comparisonFields.filter(f => f.isDifferent);
      expect(differentFields.length).toBeGreaterThan(0);
    });
  });

  describe('View Modes', () => {
    beforeEach(() => {
      component.selectDocuments('1', '2');
    });

    it('should toggle side-by-side view', () => {
      component.viewMode = 'side-by-side';
      expect(component.viewMode).toBe('side-by-side');

      component.viewMode = 'diff';
      expect(component.viewMode).toBe('diff');
    });

    it('should toggle differences only filter', () => {
      component.showDifferencesOnly = false;
      component.toggleDifferencesOnly();
      expect(component.showDifferencesOnly).toBe(true);

      component.toggleDifferencesOnly();
      expect(component.showDifferencesOnly).toBe(false);
    });

    it('should filter fields when differences only is enabled', () => {
      component.showDifferencesOnly = true;
      const filtered = component.getDisplayedFields();
      const allDifferent = filtered.every(f => f.isDifferent);
      expect(allDifferent).toBe(true);
    });
  });

  describe('Confidence Scores', () => {
    beforeEach(() => {
      component.selectDocuments('1', '2');
    });

    it('should assign correct colors for high confidence', () => {
      const color = component.getConfidenceColor(0.95);
      expect(color).toContain('green');
    });

    it('should assign correct colors for moderate confidence', () => {
      const color = component.getConfidenceColor(0.75);
      expect(color).toContain('yellow');
    });

    it('should assign correct colors for low confidence', () => {
      const color = component.getConfidenceColor(0.5);
      expect(color).toContain('red');
    });

    it('should assign background colors correctly', () => {
      const bgColor = component.getConfidenceBgColor(0.95);
      expect(bgColor).toContain('100');
    });
  });

  describe('Export Functionality', () => {
    beforeEach(() => {
      component.selectDocuments('1', '2');
    });

    it('should generate CSV data', () => {
      const csv = component['generateCSV']();
      expect(csv).toContain('Field');
      expect(csv).toContain('Document 1 Value');
      expect(csv).toContain('Document 2 Value');
    });

    it('should include all fields in CSV', () => {
      const csv = component['generateCSV']();
      component.comparisonFields.forEach(field => {
        expect(csv).toContain(field.fieldName);
      });
    });
  });

  describe('Helper Methods', () => {
    it('should return correct icons for document types', () => {
      expect(component.getDocumentIcon('invoice')).toBe('🧾');
      expect(component.getDocumentIcon('receipt')).toBe('🛒');
      expect(component.getDocumentIcon('contract')).toBe('⚖️');
    });

    it('should format dates correctly', () => {
      const date = new Date('2024-04-09');
      const formatted = component.formatDate(date);
      expect(formatted).toContain('Apr');
    });
  });

  describe('Component Lifecycle', () => {
    it('should unsubscribe on destroy', () => {
      spyOn(component['destroy$'], 'next');
      spyOn(component['destroy$'], 'complete');

      component.ngOnDestroy();

      expect(component['destroy$'].next).toHaveBeenCalled();
      expect(component['destroy$'].complete).toHaveBeenCalled();
    });
  });

  describe('Statistics Display', () => {
    beforeEach(() => {
      component.selectDocuments('1', '2');
    });

    it('should calculate total fields', () => {
      expect(component.comparisonData?.fields.length).toBe(component.comparisonFields.length);
    });

    it('should calculate matching fields', () => {
      const matchingFields = component.comparisonFields.filter(f => !f.isDifferent);
      expect(matchingFields.length).toBeGreaterThan(0);
    });

    it('should calculate different fields count', () => {
      const differentFields = component.comparisonFields.filter(f => f.isDifferent);
      expect(differentFields.length).toBeGreaterThan(0);
    });
  });
});
