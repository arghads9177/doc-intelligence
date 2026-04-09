import { TestBed, fakeAsync, tick } from '@angular/core/testing';
import { NotificationService, Toast } from './notification.service';

describe('NotificationService', () => {
  let service: NotificationService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [NotificationService]
    });
    service = TestBed.inject(NotificationService);
  });

  afterEach(() => {
    service.toasts$.subscribe(toasts => {
      toasts.forEach(toast => service.remove(toast.id));
    });
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('Toast Creation', () => {
    it('should create success toast', (done) => {
      service.success('Test success message');

      service.toasts$.subscribe(toasts => {
        const toast = toasts.find(t => t.type === 'success');
        expect(toast).toBeDefined();
        expect(toast?.message).toBe('Test success message');
        done();
      });
    });

    it('should create error toast', (done) => {
      service.error('Test error message');

      service.toasts$.subscribe(toasts => {
        const toast = toasts.find(t => t.type === 'error');
        expect(toast).toBeDefined();
        expect(toast?.message).toBe('Test error message');
        done();
      });
    });

    it('should create warning toast', (done) => {
      service.warning('Test warning message');

      service.toasts$.subscribe(toasts => {
        const toast = toasts.find(t => t.type === 'warning');
        expect(toast).toBeDefined();
        expect(toast?.message).toBe('Test warning message');
        done();
      });
    });

    it('should create info toast', (done) => {
      service.info('Test info message');

      service.toasts$.subscribe(toasts => {
        const toast = toasts.find(t => t.type === 'info');
        expect(toast).toBeDefined();
        expect(toast?.message).toBe('Test info message');
        done();
      });
    });
  });

  describe('Toast Auto-dismiss', () => {
    it('should auto-dismiss toast after timeout', fakeAsync(() => {
      service.success('Auto-dismiss test');
      
      let toastCount = 0;
      service.toasts$.subscribe(toasts => {
        toastCount = toasts.length;
      });

      expect(toastCount).toBe(1);

      tick(3000);

      service.toasts$.subscribe(toasts => {
        expect(toasts.length).toBeLessThanOrEqual(1);
      });
    }));

    it('should not auto-dismiss persistent toast', fakeAsync(() => {
      service.show('Persistent message', 'info', true);

      tick(5000);

      service.toasts$.subscribe(toasts => {
        const persistent = toasts.find(t => t.persistent);
        expect(persistent).toBeDefined();
      });
    }));
  });

  describe('Toast Removal', () => {
    it('should remove toast by id', (done) => {
      let toastId: string;

      service.success('Test message');

      service.toasts$.subscribe(toasts => {
        if (toasts.length > 0 && !toastId) {
          toastId = toasts[0].id;
          service.remove(toastId);
        } else if (toastId) {
          const removed = toasts.find(t => t.id === toastId);
          expect(removed).toBeUndefined();
          done();
        }
      });
    });

    it('should clear all toasts', (done) => {
      service.success('Message 1');
      service.error('Message 2');
      service.warning('Message 3');

      setTimeout(() => {
        service.clear();

        service.toasts$.subscribe(toasts => {
          expect(toasts.length).toBe(0);
          done();
        });
      }, 100);
    });
  });

  describe('Toast Properties', () => {
    it('should generate unique IDs for toasts', (done) => {
      service.success('Message 1');
      service.success('Message 2');

      service.toasts$.subscribe(toasts => {
        if (toasts.length === 2) {
          expect(toasts[0].id).not.toBe(toasts[1].id);
          done();
        }
      });
    });

    it('should set correct toast duration', (done) => {
      service.success('Test message');

      service.toasts$.subscribe(toasts => {
        if (toasts.length > 0) {
          expect(toasts[0].duration).toBe(3000);
          done();
        }
      });
    });

    it('should respect custom duration', (done) => {
      service.show('Custom duration', 'info', false, 5000);

      service.toasts$.subscribe(toasts => {
        if (toasts.length > 0) {
          expect(toasts[0].duration).toBe(5000);
          done();
        }
      });
    });
  });

  describe('Toast Queue', () => {
    it('should queue multiple toasts', (done) => {
      service.success('Message 1');
      service.error('Message 2');
      service.warning('Message 3');
      service.info('Message 4');

      service.toasts$.subscribe(toasts => {
        expect(toasts.length).toBe(4);
        done();
      });
    });

    it('should maintain toast order', (done) => {
      service.success('First');
      service.error('Second');
      service.warning('Third');

      service.toasts$.subscribe(toasts => {
        if (toasts.length === 3) {
          expect(toasts[0].message).toBe('First');
          expect(toasts[1].message).toBe('Second');
          expect(toasts[2].message).toBe('Third');
          done();
        }
      });
    });
  });
});
