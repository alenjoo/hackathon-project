🚀 Citizen Service Requests & Payments – GovTech Simulation

This is a full-stack web application built with:

Frontend: React

Backend: Django REST Framework

Database: PostgreSQL

Payments: Razorpay

It simulates a GovTech citizen service request system where users can raise service requests, pay associated fees securely, and officers/admins can manage approvals and reports.

cd frontend
npm install

#Run development server
npm start

#Lint & Format
npm run lint     # Run ESLint
npm run format   # Run Prettier

#Build for production
npm run build

Backend (Django)

#Create virtual environment
cd backend
python -m venv venv
venv\Scripts\activate

#Create a .env file inside backend/
# Django
SECRET_KEY=your-django-secret
DEBUG=True
ALLOWED_HOSTS=*

# Database
DB_NAME=hackathon
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432

# Payment Gateway (choose Razorpay/Stripe/Paytm sandbox)
RAZORPAY_KEY_ID=your-key-id
RAZORPAY_KEY_SECRET=your-key-secret

#Apply Migrations
python manage.py makemigrations
python manage.py migrate

python manage.py runserver

Visit: http://localhost:8000/health
GET /health
Response: { "status": "ok" }
