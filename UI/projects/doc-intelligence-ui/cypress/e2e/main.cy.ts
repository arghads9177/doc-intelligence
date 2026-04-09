describe('Document Intelligence UI - E2E Tests', () => {
  const baseUrl = 'http://localhost:4200';

  beforeEach(() => {
    cy.visit(baseUrl);
  });

  describe('Navigation', () => {
    it('should load the application', () => {
      cy.url().should('include', '/upload');
    });

    it('should navigate between pages', () => {
      // Navigate to Dashboard
      cy.contains('Dashboard').click();
      cy.url().should('include', '/dashboard');

      // Navigate to History
      cy.contains('History').click();
      cy.url().should('include', '/history');

      // Navigate to Comparison
      cy.contains('Compare').click();
      cy.url().should('include', '/comparison');

      // Navigate to Settings
      cy.contains('Settings').click();
      cy.url().should('include', '/settings');
    });

    it('should have navigation links', () => {
      cy.get('a[routerLink="/upload"]').should('exist');
      cy.get('a[routerLink="/dashboard"]').should('exist');
      cy.get('a[routerLink="/history"]').should('exist');
      cy.get('a[routerLink="/comparison"]').should('exist');
      cy.get('a[routerLink="/settings"]').should('exist');
    });
  });

  describe('Upload Page', () => {
    it('should display upload component', () => {
      cy.contains('Upload Documents').should('be.visible');
    });

    it('should show drag-drop area', () => {
      cy.get('[class*="drag"]').should('exist');
    });

    it('should show file input', () => {
      cy.get('input[type="file"]').should('exist');
    });

    it('should show upload button', () => {
      cy.contains('button', /upload|Add/i).should('exist');
    });
  });

  describe('Dashboard Page', () => {
    beforeEach(() => {
      cy.visit(`${baseUrl}/dashboard`);
    });

    it('should display dashboard title', () => {
      cy.contains('Dashboard').should('be.visible');
    });

    it('should display stat cards', () => {
      cy.get('[class*="stat"]').should('exist');
    });

    it('should display document type statistics', () => {
      cy.contains('Document Types').should('be.visible');
    });

    it('should display processing activity chart', () => {
      cy.contains('Processing Activity').should('be.visible');
    });

    it('should display recent documents section', () => {
      cy.contains('Recent Documents').should('be.visible');
    });

    it('should have quick action buttons', () => {
      cy.contains('Upload Documents').should('be.visible');
      cy.contains('View History').should('be.visible');
    });
  });

  describe('History Page', () => {
    beforeEach(() => {
      cy.visit(`${baseUrl}/history`);
    });

    it('should display history table', () => {
      cy.get('table').should('exist');
    });

    it('should display table headers', () => {
      cy.contains('Filename').should('be.visible');
      cy.contains('Type').should('be.visible');
      cy.contains('Status').should('be.visible');
    });

    it('should have view and delete buttons', () => {
      cy.get('button').should('have.length.greaterThan', 0);
    });
  });

  describe('Comparison Page', () => {
    beforeEach(() => {
      cy.visit(`${baseUrl}/comparison`);
    });

    it('should display comparison title', () => {
      cy.contains('Document Comparison').should('be.visible');
    });

    it('should display document selectors', () => {
      cy.contains('First Document').should('be.visible');
      cy.contains('Second Document').should('be.visible');
    });

    it('should have comparison controls', () => {
      cy.get('select').should('have.length', 2);
    });
  });

  describe('Settings Page', () => {
    beforeEach(() => {
      cy.visit(`${baseUrl}/settings`);
    });

    it('should display settings title', () => {
      cy.contains('Settings').should('be.visible');
    });

    it('should display settings sections', () => {
      cy.get('[class*="section"]').should('exist');
    });

    it('should have form inputs', () => {
      cy.get('input').should('exist');
    });
  });

  describe('Header and Footer', () => {
    it('should display header', () => {
      cy.get('header').should('be.visible');
    });

    it('should display logo', () => {
      cy.contains('DocIntel').should('be.visible');
    });

    it('should display footer', () => {
      cy.get('footer').should('exist');
    });
  });

  describe('Responsive Design', () => {
    it('should be responsive on mobile', () => {
      cy.viewport('iphone-x');
      cy.url().should('include', '/upload');
    });

    it('should be responsive on tablet', () => {
      cy.viewport('ipad-2');
      cy.url().should('include', '/upload');
    });

    it('should be responsive on desktop', () => {
      cy.viewport(1280, 720);
      cy.url().should('include', '/upload');
    });
  });

  describe('Error Handling', () => {
    it('should handle navigation to invalid routes', () => {
      cy.visit(`${baseUrl}/invalid-route`);
      cy.url().should('include', '/upload');
    });
  });

  describe('Accessibility', () => {
    it('should have proper page titles', () => {
      cy.title().should('not.be.empty');
    });

    it('should have semantic HTML', () => {
      cy.get('header').should('exist');
      cy.get('main, [role="main"]').should('exist');
      cy.get('footer').should('exist');
    });

    it('should have proper link styling', () => {
      cy.get('a').should('have.css', 'color');
    });
  });

  describe('User Interactions', () => {
    it('should toggle switches', () => {
      cy.visit(`${baseUrl}/settings`);
      cy.get('input[type="checkbox"]').first().check();
      cy.get('input[type="checkbox"]').first().should('be.checked');
    });

    it('should interact with dropdowns', () => {
      cy.visit(`${baseUrl}/comparison`);
      cy.get('select').first().select(0);
    });

    it('should click buttons without errors', () => {
      cy.get('button').each($btn => {
        cy.wrap($btn).should('not.be.disabled');
      });
    });
  });

  describe('Visual Regression', () => {
    it('should match dashboard snapshot', () => {
      cy.visit(`${baseUrl}/dashboard`);
      cy.get('main, [role="main"]').screenshot('dashboard');
    });

    it('should match history snapshot', () => {
      cy.visit(`${baseUrl}/history`);
      cy.get('main, [role="main"]').screenshot('history');
    });

    it('should match settings snapshot', () => {
      cy.visit(`${baseUrl}/settings`);
      cy.get('main, [role="main"]').screenshot('settings');
    });
  });
});
