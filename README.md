# Vulnerability Scanner & Security Dashboard

A full-stack vulnerability scanner and dashboard built with Flask, React, Nmap, and SQLite.

## Features
- Nmap-based service and port discovery
- TLS configuration checks
- Rule-based vulnerability detection
- CVE reference support
- Severity dashboard
- Historical scan storage
- CSV and PDF reporting
- Encrypted scan-result storage

## Tech Stack
- Backend: Python, Flask, SQLAlchemy, SQLite
- Frontend: React, Vite, Axios, Recharts
- Scanner: Nmap, Python probes
- Security: JWT authentication, encrypted result storage

## Legal Notice
This tool must only be used against systems you own or have explicit written authorization to test.

## Setup
### Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python wsgi.py

### Frontend
cd frontend
npm install
npm run dev