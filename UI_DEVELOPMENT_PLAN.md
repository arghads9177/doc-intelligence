# Document Intelligence UI - Angular 19 Development Plan

**Last Updated:** April 7, 2026  
**Status:** Planning Phase  
**Framework:** Angular 19  
**Styling:** Tailwind CSS 3.x  
**Backend API:** FastAPI (localhost:8000)

---

## 📋 Executive Summary

This document outlines the complete development plan for an Angular 19 web UI that consumes the Document Intelligence API. The UI will provide users with an intuitive interface to:
- Upload and process documents (PDF, images, plain text)
- View extracted structured data with confidence scores
- Review validation results (rule-based and AI-powered)
- Read AI-generated summaries
- Track processing history

Built with **Tailwind CSS** for utility-first, responsive styling.

**Development Timeline:** 4-5 Phases (estimated 6-8 weeks)

---

## 🎯 Requirements Overview

### Functional Requirements
- **Document Upload:** Single/batch upload with drag-and-drop support
- **Processing Pipeline Visualization:** Real-time progress tracking through 5 stages
- **Results Display:** Organized presentation of extracted data, validation, and summaries
- **Document History:** Track and manage previously processed documents
- **Validation Management:** Review and resolve validation issues
- **Export:** Download results in JSON, CSV, or PDF formats

### Non-Functional Requirements
- **Responsive Design:** Work on desktop, tablet, mobile (Tailwind CSS mobile-first)
- **Performance:** Handle 100+ document uploads efficiently
- **Accessibility:** WCAG 2.1 AA compliant with Tailwind utilities
- **Error Handling:** Graceful error messages and recovery
- **State Management:** Proper handling of async operations

---

## 🏗️ Project Structure

```
doc-intelligence/
├── app/                          (existing backend)
├── UI/                           (NEW - Angular app root)
│   ├── angular.json
│   ├── tsconfig.json
│   ├── package.json
│   ├── package-lock.json
│   ├── src/
│   │   ├── main.ts
│   │   ├── index.html
│   │   ├── styles.scss
│   │   ├── app/
│   │   │   ├── app.component.ts
│   │   │   ├── app.component.html
│   │   │   ├── app.component.scss
│   │   │   ├── app.routes.ts
│   │   │   ├── app.config.ts
│   │   │   │
│   │   │   ├── shared/
│   │   │   │   ├── services/
│   │   │   │   │   ├── api.service.ts         (API communication)
│   │   │   │   │   ├── document.service.ts    (document state mgmt)
│   │   │   │   │   └── notification.service.ts
│   │   │   │   ├── models/
│   │   │   │   │   ├── document.ts
│   │   │   │   │   ├── extraction.ts
│   │   │   │   │   ├── validation.ts
│   │   │   │   │   └── api-response.ts
│   │   │   │   ├── components/
│   │   │   │   │   ├── header/
│   │   │   │   │   ├── footer/
│   │   │   │   │   ├── loading-spinner/
│   │   │   │   │   └── error-alert/
│   │   │   │   └── pipes/
│   │   │   │       ├── format-currency.pipe.ts
│   │   │   │       ├── format-date.pipe.ts
│   │   │   │       └── highlight-confidence.pipe.ts
│   │   │   │
│   │   │   └── features/
│   │   │       ├── upload/
│   │   │       │   ├── upload.component.ts
│   │   │       │   ├── upload.component.html
│   │   │       │   └── upload.component.scss
│   │   │       │
│   │   │       ├── process/
│   │   │       │   ├── process.component.ts
│   │   │       │   ├── process.component.html
│   │   │       │   ├── process.component.scss
│   │   │       │   └── pipeline-progress/
│   │   │       │       └── pipeline-progress.component.ts
│   │   │       │
│   │   │       ├── results/
│   │   │       │   ├── results.component.ts
│   │   │       │   ├── results.component.html
│   │   │       │   ├── results.component.scss
│   │   │       │   ├── extracted-data/
│   │   │       │   │   └── extracted-data.component.ts
│   │   │       │   ├── validation-report/
│   │   │       │   │   └── validation-report.component.ts
│   │   │       │   └── summary/
│   │   │       │       └── summary.component.ts
│   │   │       │
│   │   │       ├── history/
│   │   │       │   ├── history.component.ts
│   │   │       │   ├── history.component.html
│   │   │       │   └── history.component.scss
│   │   │       │
│   │   │       ├── dashboard/
│   │   │       │   ├── dashboard.component.ts
│   │   │       │   ├── dashboard.component.html
│   │   │       │   └── dashboard.component.scss
│   │   │       │
│   │   │       └── settings/
│   │   │           ├── settings.component.ts
│   │   │           ├── settings.component.html
│   │   │           └── settings.component.scss
│   │   │
│   │   └── assets/
│   │       ├── images/
│   │       ├── icons/
│   │       └── fonts/
│   │
│   └── .angular-eslintrc.json
│
├── docker-compose.yml           (optional - full stack)
└── [other root files...]
```

---

## 📦 Setup & Scaffolding Process

### Step 1: Create UI Folder & Initialize Angular Project

```bash
# From project root (/doc-intelligence)
mkdir UI
cd UI

# Create Angular 19 project with standalone components
ng new . --skip-git --routing --skip-package-manager --strict --package-manager npm
```

**Flags Explanation:**
- `--skip-git`: Don't reinitialize git (already in parent repo)
- `--routing`: Enable Angular Router for multi-page navigation
- `--skip-package-manager`: Install deps manually after configuration
- `--strict`: Enable strict TypeScript mode
- `--package-manager npm`: Use npm for dependency management

### Step 2: Configure Angular for Standalone Components (Modern Best Practice)

Angular 19 defaults to standalone components (no NgModules needed). The scaffolding will already set this up.

### Step 3: Install Core Dependencies

```bash
# From UI folder
npm install

# Install Tailwind CSS and required dependencies
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Install additional utility packages
npm install \
  rxjs@7 \
  axios@1 \
  highlight.js@11 \
  marked@11 \
  date-fns@3

# Development dependencies
npm install --save-dev \
  @angular/eslint@19 \
  eslint@8 \
  prettier@3 \
  tailwind-prettier-plugin@0
```

### Step 4: Configure Tailwind CSS

Update `tailwind.config.js`:
```javascript
module.exports = {
  content: [
    "./src/**/*.{html,ts}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#1f2937',
        secondary: '#6366f1',
      }
    },
  },
  plugins: [],
}
```

Add to `src/styles.scss`:
```scss
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### Step 5: Configure Environment & API Integration

**Environment files** (`src/environments/`):
```typescript
// environment.ts (development)
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000'
};

// environment.prod.ts (production)
export const environment = {
  production: true,
  apiUrl: 'https://api.example.com'  // To be updated
};
```

### Step 6: Configure CORS Proxy (Development)

**proxy.conf.json** for local development:
```json
{
  "/api": {
    "target": "http://localhost:8000",
    "secure": false,
    "changeOrigin": true,
    "pathRewrite": {
      "^/api": "/api"
    }
  }
}
```

### Step 7: Update Angular Build Configuration

Modify `angular.json`:
```json
{
  "projects": {
    "doc-intelligence-ui": {
      "architect": {
        "serve": {
          "options": {
            "proxyConfig": "proxy.conf.json"
          }
        }
      }
    }
  }
}
```

---

## 📚 Dependencies & Libraries

### Core Framework
| Package | Version | Purpose |
|---------|---------|---------|
| @angular/core | 19 | Core framework |
| @angular/common | 19 | Common directives |
| @angular/router | 19 | Routing |
| @angular/forms | 19 | Reactive forms |
| rxjs | 7+ | Reactive programming |

### UI & Styling
| Package | Version | Purpose |
|---------|---------|---------|
| tailwindcss | 3.x | Utility-first CSS framework |
| postcss | 8+ | CSS processing |
| autoprefixer | 10+ | Vendor prefixes |

### Utilities
| Package | Version | Purpose |
|---------|---------|---------|
| axios | 1+ | HTTP client alternative |
| date-fns | 3+ | Date formatting |
| highlight.js | 11+ | Code highlighting |
| marked | 11+ | Markdown rendering |

### Development Tools
| Package | Version | Purpose |
|---------|---------|---------|
| @angular/eslint | 19 | Linting |
| eslint | 8+ | Code quality |
| prettier | 3+ | Code formatting |
| typescript | 5.5+ | Language (installed with Angular) |

---

## 🔄 Development Phases

### Phase 1: Foundation & Infrastructure (Week 1-2)
**Objective:** Set up architecture and core services

#### Tasks:
1. **Project Setup**
   - ✓ Scaffold Angular project
   - ✓ Install dependencies
   - ✓ Configure environments
   - ✓ Set up CORS proxy

2. **TypeScript Models** (`shared/models/`)
   - Create interface for API request/response
   - Define `Document`, `Extraction`, `Validation`, `Summary` models
   - Create `ProcessingStatus` enum

3. **API Service** (`shared/services/api.service.ts`)
   - Setup HttpClientModule
   - Create method: `analyzeDocuments(documents: File[])`
   - Implement request/response interceptors
   - Handle error responses from API

4. **Document Service** (`shared/services/document.service.ts`)
   - Manage document state (RxJS BehaviorSubject)
   - Track current/selected document
   - Manage processing history
   - Implement local storage persistence

5. **Routing Setup**
   - Define routes: `/upload`, `/process/:id`, `/results/:id`, `/history`, `/settings`
   - Create route guards for authenticated flows
   - Setup lazy loading structure

6. **Base Layout**
   - Header component with navigation
   - Footer component
   - Tailwind CSS color scheme and spacing configuration
   - Global styles (SCSS)
   - Responsive grid system setup

#### Deliverables:
- Working project structure with routing
- API service consuming backend
- Models for all data structures
- Base shell application

---

### Phase 2: Upload & Processing UI (Week 2-3)
**Objective:** Implement document upload and processing visualization

#### Components:

1. **Upload Component** (`features/upload/`)
   - File input with validation (PDF, image, text)
   - Drag & drop support
   - File preview thumbnails
   - Batch upload capability
   - Progress bar for upload
   - Validation messages

2. **Process Component** (`features/process/`)
   - Real-time pipeline progress display
   - 5-stage visualization:
     - Stage 1: Ingestion (reading file)
     - Stage 2: Classification (detecting type)
     - Stage 3: Extraction (pulling data)
     - Stage 4: Validation (checking quality)
     - Stage 5: Summarization (generating summary)
   - Processing time display
   - Cancel/retry buttons
   - Document preview panel

3. **Pipeline Progress Component** (`features/process/pipeline-progress/`)
   - Visual timeline of stages
   - Status indicators (pending, processing, complete, error)
   - Animated transitions
   - Percentage completion

#### Services:
- Polling service for real-time updates (WebSocket alternative)
- File conversion utilities
- Image preview service

#### Deliverables:
- Full upload workflow
- Real-time processing visualization
- Error handling during upload/processing

---

### Phase 3: Results Display (Week 3-4)
**Objective:** Present extracted data, validation, and summaries

#### Components:

1. **Results Component** (parent - `features/results/`)
   - Tab-based navigation: Data | Validation | Summary
   - Export buttons (JSON, CSV, PDF)
   - Print functionality
   - Share/compare documents toggle

2. **Extracted Data Component** (`features/results/extracted-data/`)
   - **Tabular view:**
     - Field name | Extracted Value | Confidence | Notes
     - Color-code by confidence (red <60%, yellow 60-80%, green >80%)
   
   - **Document-type specific displays:**
     - **Invoice:** Company, Date, Items table, Total, Currency
     - **Receipt:** Store, Items, Subtotal, Tax, Total
     - **Contract:** Parties, Dates, Obligations, Terms
   
   - **Confidence badges:**
     - Visual indicators for confidence scores
     - Hover tooltip with explanation
   
   - **Edit capability (Phase 4):**
     - Inline edit buttons
     - Validation on edit

3. **Validation Report Component** (`features/results/validation-report/`)
   - Two-column layout: Issues | Statistics
   - **Issues section:**
     - Filter by severity (Low, Medium, High)
     - Filter by source (Rule-based, AI-layer)
     - Expandable issue descriptions
     - Suggested corrections
   
   - **Statistics section:**
     - Total issues count
     - Validation confidence %
     - Issue distribution (pie chart)
     - Rule vs AI layer breakdown

4. **Summary Component** (`features/results/summary/`)
   - Formatted AI-generated summary
   - Text selection & copy support
   - Markdown rendering if applicable
   - Summary metadata (confidence, tokens used)

#### Services:
- Data formatting service (currency, dates)
- Export service (JSON, CSV, PDF generation)
- Confidence calculation utilities

#### Deliverables:
- Complete results visualization
- Document-type specific displays
- Export functionality
- Print-friendly layouts

---

### Phase 4: Advanced Features (Week 4-6)
**Objective:** Add history, editing, comparison, and settings

#### Components:

1. **History Component** (`features/history/`)
   - Table view of processed documents
   - Columns: Filename | Type | Date | Status | Actions
   - Search/filter by filename, type, date range
   - Pagination (10-50 items per page)
   - Sort by name, date, status
   - Delete document from history
   - Reprocess document button
   - View details link

   **Features:**
   - Local storage persistence
   - Session-based storage
   - JSON export of entire history

2. **Dashboard Component** (`features/dashboard/`)
   - Statistics widgets:
     - Total documents processed
     - Success rate %
     - Average processing time
     - Document type distribution (chart)
   - Recent documents (last 5)
   - Quick actions (New Upload, View History)
   - Processing stats chart (time-series)

3. **Settings Component** (`features/settings/`)
   - **API Configuration:**
     - API endpoint URL (if flexible backend)
     - Timeout settings
   - **Display Preferences:**
     - Theme (light/dark)
     - Font size
     - Layout density
   - **Processing Options:**
     - Include summaries toggle
     - Include validation toggle
     - Confidence threshold setting
   - **Data Management:**
     - Clear history button
     - Export all history
     - Delete all local data

#### Services:
- Comparison service (for document comparison)
- Chart/statistics service
- Settings persistence service

#### Enhancement Areas:
- **Phase 4a: Document Comparison**
  - Side-by-side view of two documents
  - Diff highlighting
  - Field-by-field comparison

- **Phase 4b: Batch Processing**
  - Upload multiple files at once
  - Monitor all jobs
  - Download all results as zip

- **Phase 4c: User Preferences**
  - Save user preferences (localStorage)
  - Theme customization
  - Language localization (i18n)

#### Deliverables:
- Full history management
- Dashboard analytics
- Settings management
- Advanced document features

---

### Phase 5: Polish & Deployment (Week 6-8)
**Objective:** Testing, optimization, deployment preparation

#### Tasks:

1. **Testing**
   - Unit tests (Jasmine/Karma) - target 80% coverage
   - Component tests
   - Service tests
   - E2E tests (Cypress/Playwright)

2. **Performance Optimization**
   - Lazy load route modules
   - Implement OnPush change detection
   - Optimize bundle size
   - Image optimization
   - Caching strategies

3. **Accessibility**
   - WCAG 2.1 AA compliance
   - Keyboard navigation
   - Screen reader testing
   - Color contrast validation

4. **Documentation**
   - Component documentation
   - API integration guide
   - User manual
   - Developer setup guide

5. **Deployment Preparation**
   - Production build configuration
   - Docker containerization (optional)
   - CI/CD pipeline setup
   - Environment-specific configs

#### Deliverables:
- Production-ready Angular application
- Complete test suite
- Deployment documentation
- Performance metrics

---

## 🛠️ Development Tools & Commands

### Running the Development Server

```bash
# Start Angular dev server (from UI folder)
npm start
# or
ng serve

# Access at http://localhost:4200
# API proxy will forward to http://localhost:8000
```

### Build for Production

```bash
# Optimized production build
ng build --configuration production

# Output: dist/doc-intelligence-ui/
```

### Testing

```bash
# Run unit tests
ng test

# Run E2E tests
ng e2e

# Generate coverage report
ng test --code-coverage
```

### Code Quality

```bash
# Lint code
ng lint

# Format code with Prettier
npm run format

# Fix linting issues
npm run lint:fix
```

---

## 📊 Feature Matrix

| Feature | Phase | Status | Priority |
|---------|-------|--------|----------|
| Project scaffolding | 1 |📋 Planned | HIGH |
| API integration | 1 | 📋 Planned | HIGH |
| Document upload | 2 | 📋 Planned | HIGH |
| Pipeline visualization | 2 | 📋 Planned | HIGH |
| Results display | 3 | 📋 Planned | HIGH |
| Validation report | 3 | 📋 Planned | HIGH |
| Export functionality | 3 | 📋 Planned | MEDIUM |
| Processing history | 4 | 📋 Planned | MEDIUM |
| Dashboard | 4 | 📋 Planned | MEDIUM |
| Settings | 4 | 📋 Planned | MEDIUM |
| Testing suite | 5 | 📋 Planned | MEDIUM |
| Deployment | 5 | 📋 Planned | HIGH |

---

## 🚀 Success Metrics

- ✅ Application loads and connects to API
- ✅ Users can upload documents and see progress
- ✅ Results display accurately with confidence scores
- ✅ Validation issues display with explanations
- ✅ Export functionality works for multiple formats
- ✅ History persists and is queryable
- ✅ Dashboard shows meaningful statistics
- ✅ 80%+ unit test coverage
- ✅ Lighthouse score >90
- ✅ WCAG 2.1 AA compliant

---

## 📝 Next Steps

When ready to begin implementation:
1. Start Phase 1 with project scaffolding
2. Set up Git workflow for UI folder
3. Configure pre-commit hooks (lint + format)
4. Establish component naming conventions
5. Begin Phase 1 development (1-2 weeks)

---

**Created:** April 7, 2026  
**Plan Version:** 1.0  
**Revision Status:** Ready for Implementation
