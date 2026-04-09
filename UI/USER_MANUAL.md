# Document Intelligence UI - User Manual

## Welcome to Document Intelligence

Document Intelligence is an AI-powered document analysis platform that automatically extracts, validates, and summarizes information from your documents.

## 🚀 Getting Started

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection
- Backend API running on localhost:8000

### Accessing the Application
1. Open your browser
2. Navigate to `http://localhost:4200`
3. You'll be redirected to the Upload page

## 📖 Features Overview

### 1. 📤 Upload Documents

**Purpose:** Submit documents for analysis

**How to Use:**
1. Click "📤 Upload" in the navigation
2. Choose upload method:
   - **Drag & Drop:** Drag files directly into the drop zone
   - **Select Files:** Click the drop zone to browse files
3. Select 1-5 documents (PDF, images, or text files)
4. Maximum file size: 50MB per file
5. Click "Upload Documents" button
6. Monitor progress bar

**Supported Formats:**
- PDF (.pdf)
- Images (.png, .jpg, .jpeg, .gif)
- Text (.txt)

**What Happens Next:**
- Documents are sent to the backend
- Real-time processing begins
- You'll be redirected to Processing page

### 2. 📊 Dashboard

**Purpose:** View analytics and statistics about your documents

**Sections:**

#### Stat Cards
- **Total Documents:** Count of all processed documents
- **Success Rate:** Percentage of successful analyses
- **Avg Processing:** Average time to process documents
- **Document Types:** Number of different document types

#### Document Type Distribution
- Visual breakdown of invoice, receipt, and contract documents
- Percentage and count for each type
- Icon representation

#### Processing Activity Chart
- 7-day history of document processing
- Bar chart showing daily activity
- Peak day and weekly total

#### Recent Documents
- Last 5 processed documents
- Quick access links to details
- Processing time displayed

**Quick Actions:**
- **Upload Documents:** Start a new analysis
- **View History:** See all processed documents

### 3. 🔄 Processing Pipeline

**Purpose:** Real-time visualization of document processing

**What You'll See:**
- Overall progress percentage
- Blue progress bar
- Stats showing completed stages
- Current processing stage highlighted

**Five Processing Stages:**
1. **Text Extraction** (⏳) - Reading document content
2. **Classification** (⏳) - Detecting document type
3. **Field Extraction** (⏳) - Pulling structured data
4. **Validation** (⏳) - Checking data quality
5. **Summarization** (⏳) - Generating summary

**Status Indicators:**
- ⏳ Processing (in progress)
- ✓ Completed (green checkmark)
- ✕ Error (red X)

**When Complete:**
- All stages show completion times
- "View Results" button becomes active
- Results are ready to review

### 4. 📋 Results

**Purpose:** Review extracted data, validation results, and AI summary

**Three Tabs:**

#### Data Tab
Shows extracted information for your document type:

**Invoice/Receipt:**
- Company name
- Date
- Amount
- Items
- Currency

**Contract:**
- Parties involved
- Start/End dates
- Obligations
- Key terms

**Features:**
- Color-coded confidence scores:
  - 🟢 Green (>80%): High confidence
  - 🟡 Yellow (60-80%): Medium confidence
  - 🔴 Red (<60%): Low confidence
- Hover for detailed information
- Edit field values (future feature)
- Copy values to clipboard

#### Validation Tab
Shows data quality checks:

**Issues Display:**
- Issue description
- Severity level (Low, Medium, High)
- Suggested correction
- Filter by severity or type

**Statistics:**
- Total issues count
- Validation confidence percentage
- Issue distribution chart

#### Summary Tab
AI-generated executive summary:

**Features:**
- 2-3 sentence professional summary
- Key information highlighted
- Select and copy summary text
- Print-friendly format

**Export Options:**
- **JSON:** Raw extracted data
- **CSV:** Tabular format for spreadsheets
- **PDF:** Formatted report

### 5. 📜 History

**Purpose:** Track all processed documents

**Table Columns:**
- **Filename:** Document name and icon
- **Type:** Invoice, Receipt, or Contract
- **Date:** Processing date and time
- **Status:** Completed or Processing
- **Score:** Validation confidence
- **Actions:** View, Delete, Reprocess

**Features:**
- Sort by any column
- Filter by document type
- Search by filename
- Pagination (10-50 items per page)
- View document details
- Delete from history
- Reprocess document

**Statistics Footer:**
- Total documents processed
- Successful analyses
- Processing documents
- Average confidence score

### 6. 🔍 Document Comparison

**Purpose:** Compare two documents side-by-side

**How to Compare:**
1. Click "🔍 Compare" in navigation
2. Select two documents from dropdown menus
3. View comparison results:
   - Field-by-field comparison
   - Confidence scores for each
   - Highlighted differences

**Comparison Features:**
- Overall similarity percentage
- Side-by-side view
- Highlight differences only (toggle)
- Export comparison as CSV
- Detailed match statistics

**Useful For:**
- Verifying document authenticity
- Identifying data inconsistencies
- Comparing similar documents
- Audit trail validation

### 7. ⚙️ Settings

**Purpose:** Configure application preferences

**Settings Sections:**

#### API Configuration
- API Endpoint URL (customizable for different backends)
- Connection timeout (in seconds)
- Retry attempts for failed requests

#### Processing Options
- Include summaries (toggle)
- Include validation checks (toggle)
- Confidence threshold (0-100%)
- Processing timeout

#### Appearance
- Theme preference (Light/Dark)
- Font size (Small, Medium, Large)
- Compact mode toggle

#### Data Management
- Clear processing history
- Export all history as JSON
- Delete all cached data
- LocalStorage usage

## 💡 Tips & Best Practices

### Document Preparation
1. **PDF Quality:** Ensure PDFs are clear and not scanned at low resolution
2. **Image Quality:** Use high-resolution images (300+ DPI recommended)
3. **File Size:** Keep files under 50MB
4. **Format:** Use supported formats (PDF, PNG, JPG, TXT)

### Batch Processing
- Upload up to 5 documents at once
- Ideal for: Processing similar documents together
- Useful for: Date/time efficiency

### Data Accuracy
- Review extracted data carefully
- Check validation issues before accepting results
- Flag incorrect extractions for feedback

### Organization
- Regularly clean up processing history
- Use document names that clearly identify type
- Export results for archival storage

### Performance
- Close browser tabs to free memory
- Clear cache if experiencing slowness
- Avoid uploading very large files (>40MB)

## ❌ Troubleshooting

### Upload Issues

**Problem:** "File too large"
- **Solution:** Maximum file size is 50MB. Check file size and try smaller files.

**Problem:** "Unsupported file format"
- **Solution:** Only PDF, PNG, JPG, JPEG, GIF, and TXT files are supported.

**Problem:** "Upload failed - Connection error"
- **Solution:** Check internet connection and ensure backend is running.

### Processing Issues

**Problem:** "Processing timeout"
- **Solution:** Very large files take longer. Wait or retry with smaller files.

**Problem:** "Low confidence scores"
- **Solution:** Document quality may be poor. Try clearer images/PDFs.

### Results Issues

**Problem:** "Data seems incomplete"
- **Solution:** Document may be complex or non-standard. Check validation issues.

**Problem:** "Wrong classification"
- **Solution:** Document type was misidentified. This helps train the system.

### General Issues

**Problem:** "Page not loading"
- **Solution:** 
  1. Refresh page (Ctrl+R or Cmd+R)
  2. Clear browser cache
  3. Ensure localhost:4200 is accessible

**Problem:** "Buttons not responding"
- **Solution:** 
  1. Wait for current operation to complete
  2. Clear browser cache
  3. Try different browser

**Problem:** "Cannot connect to backend"
- **Solution:** 
  1. Verify backend is running on :8000
  2. Check firewall settings
  3. Verify CORS configuration

## 🎨 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Tab | Navigate through form elements |
| Enter | Submit form or activate button |
| Escape | Close dialogs or cancel operations |
| Ctrl+Z | Undo last action (when available) |

## ♿ Accessibility

This application is designed to be accessible to all users:

- **Keyboard Navigation:** All features accessible via keyboard
- **Screen Readers:** Compatible with NVDA, JAWS, VoiceOver
- **Color Contrast:** Meets WCAG AA standards
- **Focus Indicators:** Clear visual focus for interactive elements
- **Form Labels:** All inputs properly labeled

**For Accessibility Help:**
- Use keyboard to navigate instead of mouse
- Enable screen reader for audio descriptions
- If experiencing issues, contact support

## 📞 Support & Feedback

### Getting Help
1. Check this manual for your question
2. Review error messages carefully
3. Check troubleshooting section
4. Contact support team

### Reporting Issues
When reporting a bug, include:
- Browser name and version
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if helpful

### Feature Requests
We welcome suggestions! Tell us what features would help you:
- Email: support@yourdomain.com
- Create issue in repository
- Use in-app feedback form (future)

## 🔒 Data Privacy

- Documents are processed securely
- Data not shared with third parties
- Delete history to remove local data
- All communications are encrypted
- See Privacy Policy for details

## 📱 Mobile & Responsive

The app works on all device sizes:
- **Desktop:** Full features
- **Tablet:** Optimized layout
- **Mobile:** Essential features, simplified UI

**Note:** File uploads work best on desktop browsers.

## ⚡ Performance Tips

1. **Clear Cache Regularly**
   - Settings → Data Management → Clear Cache
   - Frees up storage and improves speed

2. **Minimize Browser Tabs**
   - Close unnecessary tabs
   - Reduces memory usage

3. **Update Browser**
   - Latest browser versions are faster

4. **Check Internet**
   - Stable connection recommended
   - 5+ Mbps is ideal

## 📚 Additional Resources

- **Backend API Docs:** See `API_INTEGRATION.md`
- **Accessibility Guide:** See `ACCESSIBILITY.md`
- **Performance Tips:** See `PERFORMANCE_OPTIMIZATION.md`
- **Developer Guide:** See project README

## Glossary

- **Batch ID:** Unique identifier for document upload session
- **Confidence Score:** AI confidence in extracted data (0-100%)
- **Classification:** Document type identification  
- **Extraction:** Process of pulling structured data
- **Validation:** Quality checking of extracted data
- **Summarization:** AI-generated brief overview

## Version Info

- **Application:** Document Intelligence UI
- **Version:** 1.0.0
- **Last Updated:** April 2024
- **Framework:** Angular 19
- **Build:** Optimized with Tailwind CSS

---

**Last Updated:** April 9, 2024
**For Latest Version:** Visit repository

🎉 Thank you for using Document Intelligence!
