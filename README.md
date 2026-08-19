# 🏫 SNKKV School Dress Management System

A modern, full-stack Django web application designed for managing school dress orders, student records, standard-wise pricing matrices (Std 1–12), real-time calculations, and multi-format reporting (Excel Spreadsheet & Formatted PDF Exports).

---

## ✨ Features

- **🧑‍🎓 Student Order Management**:
  - Student Name, Standard (Std 1 to 12), and Medium (Gujarati / English).
  - Customizable package selections: Base Dress, Dupatta, Extra Dress, and Extra Dupatta.
  - Real-time automatic price calculation based on standard rates.
- **🏷️ Section Filtering**:
  - **Primary**: Standards 1 to 8
  - **Secondary**: Standards 9 and 10
  - **Higher Secondary**: Standards 11 and 12
- **📊 Live Excel Viewer & Data Sheet**:
  - Instant searchable & filterable table.
  - Metric summary cards (Total Students, Gujarati / English count, Section breakdown, Total Amount).
- **📄 Exporting Capabilities**:
  - **PDF Export**: Clean, branded PDF reports generated using ReportLab with summary totals.
  - **Excel Export**: Structured `.xlsx` spreadsheets generated using OpenPyXL.
- **💰 Standard-wise Pricing Master**:
  - Configurable pricing for Base Dress, Extra Dress, Dupatta, and Extra Dupatta across all standards (1–12).
- **🔐 Role-Based Access Control**:
  - **Admin Users**: Full rights to add, edit, delete, modify pricing, and export.
  - **View-Only Users**: View-only access to records, search, filter, and export reports without edit/delete permissions.
- **🌐 Global Hosting & Cloud Database Ready**:
  - Dynamic `DATABASE_URL` parsing via `dj-database-url`.
  - Supports **PostgreSQL** (Neon, Supabase, Railway, Render, AWS RDS), **MySQL**, and **SQLite**.
  - Production static files served via **Whitenoise**.
  - Production WSGI web server with **Gunicorn** and `Procfile`.

---

## 🛠️ Tech Stack
- **Framework**: Django 5.x / 6.x
- **Database**: PostgreSQL / SQLite (Configurable via `DATABASE_URL`)
- **Reporting**: ReportLab (PDF) & Openpyxl (Excel)
- **Styling**: Modern Responsive CSS & FontAwesome Icons
- **Static Files & Server**: Whitenoise & Gunicorn