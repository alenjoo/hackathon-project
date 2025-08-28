# 🏛️ GovTech Citizen Service Requests & Payments

A comprehensive full-stack web application designed for government technology services, enabling citizens to submit service requests, make secure payments, and allowing officers/administrators to manage approvals and generate reports.

## 🚀 Tech Stack

- **Frontend**: React.js with modern JavaScript (ES6+)
- **Backend**: Django REST Framework
- **Database**: PostgreSQL
- **Payment Gateway**: Razorpay Integration
- **Authentication**: JWT-based authentication

## ✨ Features

### Citizen Portal
- 📋 Submit service requests with document uploads
- 💳 Secure payment processing via Razorpay
- 🔐 User authentication

### Admin Panel
- 🏢 System-wide configuration management


## 🛠️ Installation & Setup

### Prerequisites
- Node.js (v14 or higher)
- Python 3.8+
- PostgreSQL 12+
- Git

### Database Setup
```sql
-- Connect to PostgreSQL as superuser
CREATE DATABASE hackathon;
CREATE USER govtech_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE hackathon TO govtech_user;
```

### Backend Setup

1. **Clone and navigate to backend directory**
```bash
git clone <repository-url>
cd backend
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment Configuration**
Create a `.env` file in the `backend/` directory:
```env
# Django Configuration
SECRET_KEY=your-highly-secure-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database Configuration
DB_NAME=hackathon
DB_USER=govtech_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

# Razorpay Configuration (Sandbox)
RAZORPAY_KEY_ID=rzp_test_your_key_id
RAZORPAY_KEY_SECRET=your_razorpay_secret



# CORS Configuration
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

5. **Database Migration**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create Superuser (Optional)**
```bash
python manage.py createsuperuser
```

7. **Start Development Server**
```bash
python manage.py runserver
```

**Backend Health Check**: Visit `http://localhost:8000/health`
```json
{
    "status": "ok",
    "timestamp": "2024-01-15T10:30:00Z",
    "database": "connected",
    "version": "1.0.0"
}
```

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd ../frontend
```

2. **Install dependencies**
```bash
npm install
```


3. **Start Development Server**
```bash
npm start
```

**Frontend Application**: Visit `http://localhost:3000`

## 📝 Available Scripts

### Frontend Scripts
```bash
# Development
npm start              # Start development server
npm run dev            # Alternative development command

# Code Quality
npm run lint           # Run ESLint
npm run lint:fix       # Fix ESLint issues automatically
npm run format         # Format code with Prettier
npm run format:check   # Check formatting without fixing



### Backend Scripts
```bash
# Development
python manage.py runserver              # Start development server
python manage.py runserver 0.0.0.0:8000 # Run on all interfaces

# Database
python manage.py makemigrations         # Create migrations
python manage.py migrate               # Apply migrations
python manage.py showmigrations        # Show migration status

```

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login


### Service Requests
- `GET /api/requests/` - List service requests
- `POST /api/requests/` - Create new request

### Payments
- `POST /api/payments/create/` - Create payment order




## 🏗️ Project Structure

```
govtech-service-app/
├── backend/
│   ├── govtech_project/
│   │   ├── settings/
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── api/
│   │   ├── views.py
│   │   ├── commands/
│   │   ├── models.py
│   │   └── migrations/
│   ├── requirements.txt
│   ├── manage.py
│   └── .env
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── utils/
│   │   └── App.js
│   ├── package.json
│   └── .env
├── docs/
├── README.md
└── .gitignore
```







## 📊 Performance Monitoring

- **Backend**: Django Debug Toolbar for development
- **Frontend**: React DevTools and Lighthouse audits
- **Database**: PostgreSQL performance monitoring
- **Payments**: Razorpay webhook monitoring

## 🔐 Security Features

- JWT-based authentication
- CORS configuration
- SQL injection protection (Django ORM)
- XSS protection
- CSRF protection
- Secure payment processing
- Environment variable protection



## 📄 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.



## 🙏 Acknowledgments

- React.js community for excellent documentation
- Django REST Framework for robust API development
- Razorpay for seamless payment integration
- PostgreSQL for reliable data management

---
