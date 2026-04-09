# Developer Setup Guide

## Prerequisites

Before starting development, ensure you have:

- **Node.js:** v18+ (check with `node --version`)
- **npm:** v9+ (check with `npm --version`)
- **Angular CLI:** v19+ (install with `npm install -g @angular/cli`)
- **Git:** For version control
- **Backend:** FastAPI app running on localhost:8000

## Project Setup

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/doc-intelligence.git
cd doc-intelligence
```

### 2. Navigate to UI Directory

```bash
cd UI
```

### 3. Install Dependencies

```bash
npm install
```

This installs all packages defined in `package.json`:
- Angular 19 framework
- Tailwind CSS 3
- TypeScript 5.7
- Testing libraries (Jasmine, Karma, Cypress)
- Development tools

### 4. Start Development Server

```bash
npm start
# or
ng serve
```

The application will be available at `http://localhost:4200`

**Development Features:**
- Hot Module Replacement (HMR) enabled
- Automatic browser reload on file changes
- Source maps for debugging

### 5. Verify Backend Connection

Before using the app, start the backend API:

```bash
# In a separate terminal, from project root
source .venv/bin/activate
python main.py
# Backend runs on http://localhost:8000
```

## Project Structure

```
UI/
├── projects/doc-intelligence-ui/src/app/
│   ├── features/
│   │   ├── upload/              # Document upload component
│   │   ├── process/             # Processing pipeline visualization
│   │   ├── results/             # Results display component
│   │   ├── history/             # Document history component
│   │   ├── comparison/          # Document comparison component
│   │   ├── dashboard/           # Analytics dashboard component
│   │   └── settings/            # Settings component
│   │
│   ├── shared/
│   │   ├── services/
│   │   │   ├── api.service.ts           # Backend API communication
│   │   │   ├── document.service.ts      # State management
│   │   │   └── notification.service.ts  # Toast notifications
│   │   ├── models/              # TypeScript interfaces
│   │   ├── components/
│   │   │   └── layout.component.ts      # Header & Footer
│   │   └── pipes/               # Custom pipes
│   │
│   ├── app.routes.ts            # Route definitions
│   ├── app.component.ts         # Root component
│   └── app.config.ts            # App configuration
│
├── src/
│   ├── styles.scss              # Global styles
│   ├── main.ts                  # Entry point
│   ├── index.html               # HTML template
│   └── environments/            # Environment configs
│
├── angular.json                 # Angular CLI config
├── tailwind.config.js           # Tailwind configuration
├── postcss.config.js            # PostCSS configuration
├── tsconfig.json                # TypeScript config
├── package.json                 # Dependencies
└── README.md                    # Project documentation
```

## Available Scripts

### Development

```bash
# Start dev server with HMR
npm start

# Build for production
npm run build

# Production build with optimization
npm run build:prod
```

### Testing

```bash
# Run unit tests (watch mode)
npm test

# Run tests once
npm test -- --watch=false

# Run E2E tests
npm run e2e

# Run tests with code coverage
npm test -- --code-coverage
```

### Code Quality

```bash
# Lint TypeScript files
npm run lint

# Format code with Prettier
npm run format

# Check formatting
npm run format:check
```

### Build & Analysis

```bash
# Production build
ng build --configuration production

# Build with stats
ng build --stats-json

# Analyze bundle size
npx webpack-bundle-analyzer dist/doc-intelligence-ui/stats.json
```

## Development Workflows

### Creating a New Component

```bash
# Generate component in features
ng generate component features/my-feature

# This creates:
# - my-feature.component.ts
# - my-feature.component.html
# - my-feature.component.scss
# - my-feature.component.spec.ts
```

### Creating a New Service

```bash
# Generate service in shared
ng generate service shared/services/my-service

# This creates:
# - my-service.service.ts
# - my-service.service.spec.ts
```

### Running Specific Tests

```bash
# Test specific file
ng test --include='**/dashboard.component.spec.ts'

# Test with specific pattern
ng test --include='**/services/**'

# E2E test specific suite
npx cypress run --spec "cypress/e2e/main.cy.ts"
```

## Code Style Guide

### TypeScript Conventions

```typescript
// Use strict typing
interface User {
  id: string;
  name: string;
}

// Use const for immutability
const user: User = { id: '1', name: 'John' };

// Use observables for async operations
observable$.pipe(
  debounceTime(300),
  distinctUntilChanged()
).subscribe(value => {});
```

### HTML Templates

```html
<!-- Use trackBy for ngFor -->
<div *ngFor="let item of items; trackBy: trackByFn">
  {{ item.name }}
</div>

<!-- Bind to properties directly -->
<button [disabled]="isLoading">Submit</button>

<!-- Use proper spacing -->
<div class="p-6 rounded-lg shadow-md">
  <!-- Content -->
</div>
```

### SCSS/Tailwind

```scss
// Prefer Tailwind utilities over custom CSS
// ✅ Good
<div class="flex gap-4 p-6 rounded-lg">

// ❌ Avoid
<div class="my-custom-container">
  // Then writing custom CSS

// Custom styles only when necessary
@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; }
}
```

## Debugging

### Debug in Browser DevTools

1. Open Chrome DevTools (F12)
2. Sources tab → Webpack → dot
3. Find source file and set breakpoint
4. Reload page to hit breakpoint

### Debug in VS Code

1. Add launch configuration in `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Chrome",
      "type": "chrome",
      "request": "launch",
      "url": "http://localhost:4200",
      "webRoot": "${workspaceRoot}"
    }
  ]
}
```

2. Press F5 to start debugging

### Enable Console Logging

```typescript
// In environment.ts for development
export const environment = {
  production: false,
  enableLogging: true
};

// In service
if (!environment.production) {
  console.log('Debug info:', data);
}
```

## Deployment

### Build for Production

```bash
# Create optimized production build
ng build --configuration production

# Output: dist/doc-intelligence-ui/
# Files include CSS minification, tree-shaking, AOT compilation
```

### Serve Locally

```bash
# Serve dist folder
npx http-server dist/doc-intelligence-ui/ -p 8080
# Access at http://localhost:8080
```

### Deploy to Web Server

```bash
# Copy to nginx/apache
scp -r dist/doc-intelligence-ui/* user@server:/var/www/html/

# Or use Docker
docker build -t doc-intelligence-ui .
docker run -p 80:80 doc-intelligence-ui
```

### Environment Configuration

Update API URL before deployment:

```typescript
// src/environments/environment.prod.ts
export const environment = {
  production: true,
  apiUrl: 'https://your-production-api.com'
};
```

## Troubleshooting

### Node Modules Issues

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# On Windows
rmdir /s /q node_modules
del package-lock.json
npm install
```

### Port Already in Use

```bash
# Use different port
ng serve --port 4201

# Or kill process using port 4200
lsof -ti:4200 | xargs kill -9  # Mac/Linux
netstat -ano | findstr :4200   # Windows
```

### TypeScript Errors

```bash
# Rebuild TypeScript
ng build --aot

# Check compilation
npx tsc --noEmit
```

### CSS Not Applying

```bash
# Rebuild Tailwind CSS
npm run build

# Check if tailwind config is correct
npx tailwindcss -i ./src/styles.scss -o ./dist/styles.css
```

## Useful Commands Reference

```bash
# Development
npm start                    # Start dev server
npm test                     # Run tests
npm run lint                 # Lint code

# Building
npm run build                # Dev build
npm run build:prod           # Production build
ng build --stats-json        # Build with stats

# Formatting
npm run format               # Format with Prettier
npm run format:check         # Check formatting

# Cleanup
npm run clean                # Remove dist folder
rm -rf node_modules          # Remove dependencies

# Version Info
ng version                   # Angular CLI version
npm list                     # All installed packages
npm outdated                 # Check for updates

# Package Management
npm update                   # Update packages
npm install <package>        # Install new package
npm uninstall <package>      # Remove package
```

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes, test, commit
git add .
git commit -m "feat: add my feature"

# Push to remote
git push origin feature/my-feature

# Create Pull Request in GitHub
# After review and approval, merge to main
```

## Performance Profiling

### Angular DevTools

1. Install Angular DevTools extension
2. Open DevTools Elements tab
3. Switch to Profiler tab
4. Record app interactions
5. Analyze performance metrics

### Chrome DevTools

1. Open DevTools (F12)
2. Performance tab
3. Record with Record button
4. Perform actions
5. Stop recording and analyze flame chart

## CI/CD Pipeline

Commands for automated testing (when set up):

```bash
# Run all checks
npm run lint && npm test && npm run e2e

# Build production version
npm run build:prod

# Deploy (example with GitHub Actions)
# See .github/workflows/ for automation
```

## Learning Resources

- [Angular Documentation](https://angular.io/docs)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [RxJS Documentation](https://rxjs.dev)

## Support

For development issues:
1. Check existing code examples in components
2. Review test files for usage patterns
3. Consult this guide
4. Search GitHub issues
5. Ask team members

---

**Last Updated:** April 2024
**Angular Version:** 19.x
**Node Version:** 18+
