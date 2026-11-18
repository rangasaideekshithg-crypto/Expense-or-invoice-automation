# AI-Powered Expense & Invoice Automation System

An enterprise-grade, full-stack financial automation platform that accelerates accounts payable, extracts invoice data via OCR and Google Gemini Generative AI, validates mathematical consistency, detects duplicates, stores records in MySQL, visualizes spend analytics, and provides an AI Financial Assistant.

---

## 🌟 Key Features

1. **Multi-Format Ingestion**: Supports PDF documents, scans, and images (JPG, JPEG, PNG). Handles digital vector PDFs and scanned documents.
2. **Hybrid OCR Engine**: PyMuPDF (`fitz`) for instant native digital text extraction paired with Tesseract OCR & Pillow image processing for scanned receipts.
3. **Google Gemini GenAI Extraction**: Employs Google GenAI Python SDK (`google-genai`) with structured JSON schema output to parse vendor details, line items, taxes, and dates.
4. **Deterministic Fallback Pipeline**: Fallback regex and heuristic engine guarantees zero downtime and reliable offline performance.
5. **Intelligent Expense Categorization**: Categorizes expenses into 10 industry-standard categories (Software & IT, Travel, Office Supplies, Utilities, etc.) with user override capabilities.
6. **Financial Validation & Sanity Checking**: Validates required fields, date formats, and checks mathematical identity ($\text{Subtotal} + \text{Tax} = \text{Total Amount}$) with rounding tolerance.
7. **Multi-Vector Duplicate Detection**: Identifies duplicate bills across Invoice Number, Vendor Name, Invoice Date, and Total Amount before saving.
8. **MySQL Database with SQLAlchemy ORM**: Relational schema storing Users, Vendors, Invoices, line-item Expenses, and Processing Audit Logs with Decimal precision.
9. **Executive Streamlit SaaS Frontend**: Clean SaaS UI with dark navy navigation, responsive KPI cards, and Plotly charts.
10. **Financial Statement Reports**: Export period-filtered reports to styled Excel (`.xlsx` via OpenPyXL) and PDF (`.pdf` via ReportLab).
11. **Grounded AI Financial Assistant**: Natural-language conversational chatbot answering questions on monthly expenses, top vendors, GST totals, and unusual outliers—grounded strictly in MySQL records without hallucination.

---

## 🏗️ System Architecture

```
User / Accountant
       │
       ▼
Streamlit Frontend (Port 8501)
  ├── 📊 Dashboard (Plotly & Real-time KPIs)
  ├── 📤 Drag-and-Drop Ingestion Workbench
  ├── 📜 Searchable Invoice Audit History
  ├── 🏷️ Expense Management & Categorization
  ├── 📈 Deep Analytics & Trend Charts
  ├── 📋 Report Generator (Excel / PDF)
  └── 🤖 AI Financial Assistant (Chatbot)
       │
       ▼  HTTP REST APIs
FastAPI Backend (Port 8000)
  ├── POST /invoices/upload
  ├── POST /invoices/{id}/process
  ├── POST /invoices/{id}/confirm
  ├── GET  /invoices & PUT /invoices/{id}
  ├── GET  /expenses & PUT /expenses/{id}/category
  ├── GET  /analytics/summary
  ├── GET  /reports/monthly, /reports/export/pdf, /reports/export/excel
  └── POST /ai/chat
       │
       ├──► Hybrid OCR: PyMuPDF + Tesseract OCR + Pillow
       ├──► Generative AI: Google Gemini GenAI SDK (`gemini-2.5-flash`)
       ├──► Validation & Duplicate Detection Engine
       └──► MySQL Database (`invoice_db`) via SQLAlchemy ORM
```

---

## 📁 Project Structure

```
AI_Invoice_Automation/
│
├── backend/
│   ├── main.py                  # FastAPI application entry point, CORS & lifecycle
│   ├── config.py                # Environment and configuration settings
│   ├── database.py              # SQLAlchemy database engine, session & auto-creation
│   │
│   ├── models/                  # SQLAlchemy ORM Data Models
│   │   ├── __init__.py
│   │   ├── user.py              # Users table (auth & audit)
│   │   ├── vendor.py            # Vendors table
│   │   ├── invoice.py           # Invoices master table
│   │   ├── expense.py           # Expenses line-item breakdown table
│   │   └── processing_log.py    # Audit trail and OCR/AI processing log
│   │
│   ├── schemas/                 # Pydantic Request & Response Schemas
│   │   ├── __init__.py
│   │   ├── invoice_schema.py    # Invoice Pydantic schemas (V2 ConfigDict)
│   │   └── expense_schema.py    # Expense schemas
│   │
│   ├── routes/                  # Modular REST API Endpoints
│   │   ├── __init__.py
│   │   ├── invoice_routes.py    # Upload, process, confirm, query, update, delete
│   │   ├── expense_routes.py    # Expense filtering, reclassification, status updates
│   │   ├── report_routes.py     # Aggregated reports, PDF & Excel export endpoints
│   │   └── chatbot_routes.py    # Financial assistant chatbot with DB grounding
│   │
│   ├── services/                # Core Business & AI Logic
│   │   ├── __init__.py
│   │   ├── ocr_service.py       # PyMuPDF digital extraction + Tesseract OCR
│   │   ├── gemini_service.py    # Google Gemini GenAI structured extraction & chat
│   │   ├── invoice_extraction.py# Master extractor (Gemini + Deterministic Fallback)
│   │   ├── expense_categorization.py # 10-category classification engine
│   │   ├── validation_service.py# Field and mathematical sanity validation
│   │   ├── duplicate_detection.py # Multi-attribute duplicate invoice detection
│   │   ├── analytics_service.py # Database KPI calculations & Plotly dataset aggregation
│   │   └── report_service.py    # Excel (openpyxl) and PDF (ReportLab) generators
│   │
│   └── utils/
│       ├── __init__.py
│       ├── file_handler.py      # Secure file upload, extension & size validation
│       └── helpers.py           # Date ISO normalizer, currency cleaner, JSON parser
│
├── frontend/
│   ├── app.py                   # Streamlit multi-page application entry point
│   ├── styles.py                # SaaS styling, custom CSS, metric cards, badges
│   ├── api_client.py            # Centralized HTTP API client for backend
│   └── pages/
│       ├── dashboard.py         # Page 1: Executive KPI Cards & Plotly Charts
│       ├── upload_invoice.py    # Page 2: Drag & drop ingestion, review & confirm
│       ├── invoice_history.py   # Page 3: Searchable table, audit trail, edit/delete
│       ├── expense_management.py# Page 4: Category reclassification & payment status
│       ├── analytics.py         # Page 5: Deep visual analytics & trend breakdowns
│       ├── reports.py           # Page 6: Period report generator (PDF & Excel download)
│       └── ai_assistant.py      # Page 7: Conversational AI financial assistant
│
├── sample_data/                 # Generated realistic sample invoices for tests
│   ├── create_sample_invoices.py
│   ├── aws_cloud_invoice.pdf
│   ├── staples_office_supplies.pdf
│   ├── indigo_flight_travel.pdf
│   ├── tata_power_utility.pdf
│   └── google_cloud_receipt.png
│
├── uploads/                     # Secure storage for uploaded invoice files
├── reports/                     # Output directory for exported PDF/Excel statements
├── tests/                       # Automated Pytest Test Suite (20 Tests)
│   ├── test_ocr_service.py
│   ├── test_gemini_parsing.py
│   ├── test_validation.py
│   ├── test_duplicate_detection.py
│   ├── test_report_service.py
│   └── test_api_endpoints.py
│
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Prerequisites

### 1. Python Environment (Windows 11)
Make sure Python 3.11+ is installed. Clone or navigate to the project directory:

```bash
cd "c:\Users\USER\OneDrive\Desktop\Expense or invoice automation"
```

Install all required Python libraries:
```bash
pip install -r requirements.txt
```

---

### 2. Tesseract OCR Installation (Windows)

1. Download the Windows installer from UB-Mannheim:
   https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer (default install path: `C:\Program Files\Tesseract-OCR\tesseract.exe`).
3. Add `C:\Program Files\Tesseract-OCR` to your Windows Environment `PATH`, or set `TESSERACT_CMD` in your `.env` file:
   ```env
   TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
   ```

*Note: For digital vector PDFs (e.g. AWS invoices, flight tickets, utility bills), the system uses PyMuPDF native extraction directly without requiring Tesseract.*

---

### 3. MySQL Database Setup

1. Open MySQL Command Line Client or MySQL Workbench:
```sql
CREATE DATABASE invoice_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. Create a dedicated user (or use `root`):
```sql
CREATE USER 'invoice_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON invoice_db.* TO 'invoice_user'@'localhost';
FLUSH PRIVILEGES;
```

3. Configure your `.env` file:
```env
DATABASE_URL=mysql+pymysql://invoice_user:your_password@localhost:3306/invoice_db
```

*Note: If MySQL is temporarily offline, the system automatically detects port availability via non-blocking socket probes and falls back to a local SQLite database (`invoice_db.db`), allowing zero-friction demonstrations and tests.*

---

### 4. Google Gemini API Setup

1. Visit [Google AI Studio](https://aistudio.google.com/) and create a free API key.
2. Create a `.env` file from `.env.example`:
```env
GEMINI_API_KEY=AIzaSy...your_actual_key_here
GEMINI_MODEL=gemini-2.5-flash
```

---

## 🚀 Running the Application

### Step 1: Start FastAPI Backend
Open a terminal in the project directory:
```bash
uvicorn backend.main:app --reload --port 8000
```
- Backend Service: http://127.0.0.1:8000
- Interactive Swagger API Docs: http://127.0.0.1:8000/docs
- ReDoc Documentation: http://127.0.0.1:8000/redoc

### Step 2: Start Streamlit Frontend
Open a second terminal in the project directory:
```bash
streamlit run frontend/app.py
```
- Web Application UI: http://localhost:8501

---

## 🧪 Running Automated Tests

A comprehensive test suite of 20 unit and integration tests verifies the entire pipeline:

```bash
python -m pytest tests -v
```

### Test Coverage Highlights:
- `tests/test_ocr_service.py`: PDF digital text extraction, multi-line parsing, handling corrupted/empty files.
- `tests/test_gemini_parsing.py`: JSON parsing from markdown code blocks, date normalization, currency parsing, fallback rule-based pipeline.
- `tests/test_validation.py`: Mathematical consistency ($\text{Subtotal} + \text{Tax} = \text{Total}$), rounding tolerance, missing fields, negative amount detection.
- `tests/test_duplicate_detection.py`: Exact duplicate detection, candidate date/vendor/amount matches, non-duplicate validation.
- `tests/test_report_service.py`: Aggregation logic, PDF generation with ReportLab, Excel spreadsheet generation with OpenPyXL.
- `tests/test_api_endpoints.py`: Health check, invoice upload, process pipeline, user confirmation, search, expenses synchronization, chatbot grounded database retrieval.

---

## 📑 Verification & Demo Workflow

1. **Ingest Sample Invoices**:
   - Go to **📤 Upload Invoice** in the sidebar.
   - Click "Browse files" and choose files from `sample_data/` (e.g. `aws_cloud_invoice.pdf`, `staples_office_supplies.pdf`, `indigo_flight_travel.pdf`, `tata_power_utility.pdf`, `google_cloud_receipt.png`).
   - Click **🚀 Ingest & Upload Files**.
2. **Review & Confirm**:
   - Select an invoice from the workbench dropdown.
   - Click **⚡ Run OCR & AI Extraction**.
   - Review extracted Vendor, Date, Subtotal, Tax, Total, and Category.
   - Click **💾 Confirm & Save to Database**.
3. **Explore Dashboard & Analytics**:
   - Navigate to **📊 Dashboard** to view real-time KPI cards, monthly trends, and category distribution.
   - Check **📈 Analytics & Trends** for deep spending breakdowns and tax deductions.
4. **Download Financial Reports**:
   - Navigate to **📋 Financial Reports**.
   - Select period (Monthly / Quarterly / Category-wise).
   - Click **📄 Download PDF Report** or **📊 Download Excel (.xlsx)**.
5. **Chat with AI Financial Assistant**:
   - Open **🤖 AI Financial Assistant**.
   - Click any chip or ask: *"What is my total expense this month?"*, *"Which vendor has the highest expenses?"*, *"What is the total GST paid?"*.
   - Expand the **📊 Verified Database Records** drawer below the answer to inspect exact ground-truth query data.
