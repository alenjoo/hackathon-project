# Hackathon Full-Stack Project

This is a full-stack web application built with **React (frontend)** and **Django (backend)**. It includes linting and formatting tools (ESLint + Prettier) for consistent code quality and a `/health` route to verify backend status.
## 🚀 Setup Instructions

### 🔹 Frontend (React)

#### Install dependencies
```bash
cd frontend
npm install

Run development server
npm start

Lint & Format
npm run lint     # Run ESLint
npm run format   # Run Prettier

Build for production
npm run build

Backend (Django)

Create virtual environment
cd backend
python -m venv venv
venv\Scripts\activate

python manage.py runserver

Visit: http://localhost:8000/health
GET /health
Response: { "status": "ok" }
