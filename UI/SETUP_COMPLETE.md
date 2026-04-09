# Angular 19 UI - Development Quick Start Guide

## ✅ Setup Complete!

Your Angular 19 UI application has been successfully scaffolded and configured.

### What Was Installed

#### Core Dependencies
- **Angular 19** - Latest Angular framework with standalone components
- **RxJS 7** - Reactive programming library
- **Tailwind CSS 4.2.2** - Utility-first CSS framework
- **Axios** - HTTP client
- **Date-fns** - Date formatting utilities
- **Highlight.js** - Code syntax highlighting
- **Marked** - Markdown rendering

#### Development Tools
- **Angular ESLint** - Linting
- **ESLint 8** - Code quality
- **Prettier 3** - Code formatting

#### Configuration Files Created
- `tailwind.config.js` - Tailwind CSS configuration
- `postcss.config.js` - PostCSS configuration
- `proxy.conf.json` - API proxy for development
- `angular.json` - Updated with proxy configuration
- `styles.scss` - Global styles with Tailwind directives

### Project Structure

```
UI/
├── projects/
│   └── doc-intelligence-ui/
│       ├── src/
│       │   ├── app/                 (Components, services, routes)
│       │   ├── index.html
│       │   ├── main.ts              (Entry point)
│       │   └── styles.scss          (Global styles with Tailwind)
│       ├── tsconfig.app.json
│       └── tsconfig.spec.json
├── angular.json
├── package.json
├── tailwind.config.js
├── postcss.config.js
├── proxy.conf.json
└── node_modules/                    (600+ packages installed)
```

### Available Commands

```bash
# Start development server (runs on http://localhost:4200)
npm start

# Build for production
npm run build

# Run unit tests
npm test

# Run linter
npm run lint

# Format code
npm run format (once Prettier is configured)

# View package.json for full list
cat package.json
```

### Development Server Setup

The development server is configured to:
- Run on `http://localhost:4200`
- Auto-reload on file changes (via `--reload`)
- Proxy API calls to `http://localhost:8000` (backend API)
- Use SCSS for component styles

### Next Steps

1. **Start the development server:**
   ```bash
   cd /home/argha-ds/datascience/projects/gen-ai/doc-intelligence/UI
   npm start
   ```

2. **Open browser:** Navigate to `http://localhost:4200`

3. **Begin Phase 1:** Follow the development plan to build:
   - TypeScript models for API responses
   - API service for backend communication
   - Document service for state management
   - Routing configuration
   - Base layout components

### API Proxy Configuration

The `proxy.conf.json` automatically routes:
- All requests to `/api/*` → `http://localhost:8000/api/*`

This allows you to use relative API URLs in your code:
```typescript
// Instead of: http://localhost:8000/api/analyze
// Use: /api/analyze
```

### Tailwind CSS Usage

Tailwind is fully configured with custom colors:
- `primary: #1f2937` (gray-800)
- `secondary: #6366f1` (indigo-500)
- `success: #10b981` (green-500)
- `warning: #f59e0b` (amber-500)
- `error: #ef4444` (red-500)
- `info: #3b82f6` (blue-500)

Use utility classes in your templates:
```html
<div class="flex flex-col gap-4">
  <button class="bg-primary text-white px-4 py-2 rounded">
    Submit
  </button>
</div>
```

### Troubleshooting

**Port 4200 already in use?**
```bash
npm start -- --port 4300
```

**Need to rebuild node_modules?**
```bash
rm -rf node_modules package-lock.json
npm install
```

**Tailwind styles not applying?**
- Restart the dev server (`npm start`)
- Make sure `proxy.conf.json` is in the root UI folder

### Ready to Build!

Your Angular 19 environment is ready. Refer to `UI_DEVELOPMENT_PLAN.md` for detailed Phase 1-5 requirements.

Start with Phase 1: Creating TypeScript models and API service.

---

**Created:** April 7, 2026  
**Angular Version:** 19  
**Tailwind Version:** 4.2.2  
**Node Packages:** 600+
