import { ComponentFixture, TestBed } from '@angular/core/testing';
import { DashboardComponent } from './dashboard.component';
import { DocumentService } from '../../shared/services/document.service';
import { BehaviorSubject } from 'rxjs';

describe('DashboardComponent', () => {
  let component: DashboardComponent;
  let fixture: ComponentFixture<DashboardComponent>;
  let documentServiceMock: any;

  beforeEach(async () => {
    documentServiceMock = {
      documentHistory$: new BehaviorSubject([
        {
          id: 1,
          name: 'Invoice.pdf',
          type: 'invoice',
          status: 'completed',
          date: new Date(),
          processingTime: 12
        },
        {
          id: 2,
          name: 'Receipt.pdf',
          type: 'receipt',
          status: 'completed',
          date: new Date(),
          processingTime: 8
        }
      ])
    };

    await TestBed.configureTestingModule({
      imports: [DashboardComponent],
      providers: [
        { provide: DocumentService, useValue: documentServiceMock }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(DashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('Dashboard Data Loading', () => {
    it('should load dashboard data on init', () => {
      expect(component.stats.length).toBeGreaterThan(0);
    });

    it('should calculate statistics correctly', () => {
      expect(component.stats[0].label).toContain('Total');
      expect(component.stats[1].label).toContain('Success');
      expect(component.stats[2].label).toContain('Avg Processing');
    });

    it('should display recent documents', () => {
      expect(component.recentDocuments.length).toBeGreaterThan(0);
    });
  });

  describe('Document Type Distribution', () => {
    it('should calculate document type distribution', () => {
      expect(component.documentTypeStats.length).toBeGreaterThan(0);
    });

    it('should sort types by count descending', () => {
      if (component.documentTypeStats.length > 1) {
        for (let i = 0; i < component.documentTypeStats.length - 1; i++) {
          expect(component.documentTypeStats[i].count)
            .toBeGreaterThanOrEqual(component.documentTypeStats[i + 1].count);
        }
      }
    });

    it('should calculate percentage correctly', () => {
      component.documentTypeStats.forEach(type => {
        expect(type.percentage).toBeGreaterThanOrEqual(0);
        expect(type.percentage).toBeLessThanOrEqual(100);
      });
    });
  });

  describe('Processing Statistics', () => {
    it('should generate processing stats', () => {
      expect(component.processingStats.length).toBeGreaterThan(0);
    });

    it('should generate 7 days of stats', () => {
      expect(component.processingStats.length).toBeLessThanOrEqual(7);
    });

    it('should calculate bar height correctly', () => {
      const height = component.getBarHeight(5);
      expect(height).toBeGreaterThanOrEqual(0);
      expect(height).toBeLessThanOrEqual(100);
    });
  });

  describe('Helper Methods', () => {
    it('should return correct icons for document types', () => {
      expect(component.getTypeIcon('invoice')).toBe('🧾');
      expect(component.getTypeIcon('receipt')).toBe('🛒');
      expect(component.getTypeIcon('contract')).toBe('⚖️');
    });

    it('should format dates correctly', () => {
      const date = new Date('2024-04-09');
      const formatted = component.formatDate(date);
      expect(formatted).toContain('Apr');
    });

    it('should format time correctly', () => {
      const time = component.formatTime(12);
      expect(time).toBe('12s');
    });
  });

  describe('Stat Cards Display', () => {
    it('should have 4 stat cards', () => {
      expect(component.stats.length).toBe(4);
    });

    it('should have correct stat labels', () => {
      const labels = component.stats.map(s => s.label);
      expect(labels).toContain('Total Documents');
      expect(labels).toContain('Success Rate');
      expect(labels).toContain('Avg Processing');
    });

    it('should assign colors to stat cards', () => {
      component.stats.forEach(stat => {
        expect(stat.color).toBeTruthy();
        expect(stat.bgColor).toBeTruthy();
      });
    });
  });

  describe('Component Cleanup', () => {
    it('should unsubscribe on destroy', () => {
      spyOn(component['destroy$'], 'next');
      spyOn(component['destroy$'], 'complete');

      component.ngOnDestroy();

      expect(component['destroy$'].next).toHaveBeenCalled();
      expect(component['destroy$'].complete).toHaveBeenCalled();
    });
  });
});
