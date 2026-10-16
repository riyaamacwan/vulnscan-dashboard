# Vulnerability Scanner & Security Dashboard

A full-stack vulnerability scanner and security dashboard built with Python, Flask, React, Nmap, and SQLite.

The application performs authorized network and service discovery, applies a rule-based vulnerability engine, stores findings in SQLite, and presents results through an interactive React dashboard.

## Features

- Nmap-based port and service discovery
- TLS certificate and protocol checks
- Rule-based vulnerability detection
- CVE reference support
- Severity-based dashboard
- Individual scan reports
- Historical scan storage
- CSV and PDF report export
- JWT authentication
- Encrypted scan-result storage
- Docker Compose setup
- GitHub Actions CI

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask, SQLAlchemy |
| Database | SQLite |
| Scanner | Nmap, Python probes |
| Frontend | React, Vite, Axios, React Router |
| Reports | ReportLab, CSV |
| Security | JWT, password hashing, encrypted storage |
| DevOps | Docker Compose, GitHub Actions |

## Architecture

```text
React Dashboard
      ↓
Flask REST API
      ↓
Scan Service
      ↓
Nmap Scanner + TLS Probe + Rules Engine
      ↓
SQLite Database
      ↓
Findings, Reports, Dashboard
```

## Legal Disclaimer

This project is intended for educational use and security testing in controlled environments.

Only scan systems that you own or for which you have explicit written authorization. Unauthorized scanning may be illegal.

## Local Setup

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python wsgi.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Docker

```bash
docker compose up --build
```

## API Overview

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Health check |
| POST | `/api/scans` | Start a scan |
| GET | `/api/scans/<id>` | Get scan details |
| GET | `/api/findings` | List findings |
| GET | `/api/reports/<id>/csv` | Download CSV report |
| GET | `/api/reports/<id>/pdf` | Download PDF report |
| POST | `/api/auth/register` | Register user |
| POST | `/api/auth/login` | Login user |

## Screenshots

![Dashboard](docs/screenshots/dashboard.png)

![Scan Details](docs/screenshots/scan-details.png)

## Roadmap

- Historical scan comparison
- CVE enrichment using NVD data
- CVSS scoring
- Web application security probes
- Role-based access control
- Scheduled scans
- Email alerts