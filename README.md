# ASIA Insurance Agency CRM

A comprehensive Customer Relationship Management (CRM) system for ASIA (Amandeep Singh Insurance Agency) built with React TypeScript frontend and FastAPI Python backend.

![ASIA Insurance Agency](frontend/public/lovable-uploads/7b6edfe8-8717-443b-9999-168694fc2142.png)

## 🏢 About ASIA Insurance Agency

**Professional insurance agency offering:**
- Auto Insurance
- Home Insurance  
- Commercial Insurance
- Life Insurance
- Health Insurance

*Coverage you deserve, rates you can afford, from an agency you can trust.*

## 🚀 Tech Stack

### Frontend
- **React 18** with TypeScript
- **Vite** for build tooling
- **Tailwind CSS** for styling
- **Radix UI** for components
- **React Router** for navigation
- **React Query** for data fetching
- **Shadcn/ui** component library

### Backend  
- **FastAPI** for REST API
- **MongoDB** with Motor for database
- **Python 3.8+**
- **JWT Authentication**
- **Pydantic** for data validation
- **Uvicorn** ASGI server

## 📋 Prerequisites

Make sure you have the following installed on your system:

- **Node.js** (v16 or higher) - [Download here](https://nodejs.org/)
- **Python** (v3.8 or higher) - [Download here](https://python.org/)
- **MongoDB** - [Download here](https://www.mongodb.com/try/download/community) or use [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- **Git** - [Download here](https://git-scm.com/)

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/MadhavMadMax37/Asia-prototype.git
cd Asia-prototype
```

### 2. Backend Setup

#### Navigate to backend directory:
```bash
cd backend
```

#### Install Python dependencies:
```bash
pip install -r requirements.txt
```

#### Set up environment variables:
Create a `.env` file in the backend directory with the following variables:

```env
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=asia_insurance_crm

# JWT Configuration  
SECRET_KEY=your-super-secret-jwt-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email Configuration (optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# Redis Configuration (for Celery)
REDIS_URL=redis://localhost:6379
```

#### Initialize the database:
```bash
python init_db.py
```

### 3. Frontend Setup

#### Navigate to frontend directory:
```bash
cd ../frontend
```

#### Install Node.js dependencies:
```bash
npm install
```

## 🚦 Running the Application

### Start the Backend Server

```bash
cd backend
python main.py
```

The backend API will be available at: `http://localhost:8000`

- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Alternative API Docs**: http://localhost:8000/redoc

### Start the Frontend Development Server

In a new terminal window:

```bash
cd frontend  
npm run dev
```

The frontend application will be available at: `http://localhost:5173`

## 📁 Project Structure

```
asia-prototype/
├── README.md
├── .gitignore
│
├── backend/
│   ├── .gitignore
│   ├── requirements.txt
│   ├── main.py                 # FastAPI application entry point
│   ├── database.py             # MongoDB connection
│   ├── models.py               # Pydantic models
│   ├── schemas.py              # Response schemas
│   ├── auth_utils.py           # Authentication utilities
│   ├── email_utils.py          # Email utilities
│   ├── init_db.py              # Database initialization
│   └── routers/
│       ├── __init__.py
│       ├── auth.py             # Authentication routes
│       ├── leads.py            # Lead management routes
│       ├── dashboard.py        # Dashboard routes
│       └── analytics.py        # Analytics routes
│
├── frontend/
│   ├── .gitignore
│   ├── package.json
│   ├── index.html
│   ├── vite.config.ts
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   ├── public/
│   │   ├── favicon.png
│   │   └── lovable-uploads/    # Logo and assets
│   └── src/
│       ├── main.tsx            # React app entry point
│       ├── App.tsx             # Main app component
│       ├── components/         # Reusable components
│       ├── pages/              # Page components
│       ├── hooks/              # Custom React hooks
│       └── assets/             # Static assets
│
└── dashboard.html              # Standalone dashboard
```

## 🔧 Development Scripts

### Backend Commands:
```bash
# Run development server
python main.py

# Run with uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Initialize/reset database
python init_db.py

# Run tests (if available)
pytest
```

### Frontend Commands:
```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## 🌟 Key Features

### Frontend Features:
- 📱 Responsive design for all devices
- 🎨 Modern UI with Tailwind CSS
- 🔐 JWT-based authentication
- 📊 Interactive dashboard
- 📋 Quote request forms
- 🎯 Insurance service pages
- 🔍 Real-time search and filtering

### Backend Features:
- 🚀 High-performance FastAPI framework
- 🔒 Secure JWT authentication
- 📊 MongoDB database integration
- 📧 Email notification system
- 📈 Analytics and reporting
- 🔄 Async/await support
- 📝 Comprehensive API documentation

## 🚀 Deployment

### Backend Deployment (Production):
```bash
# Install production dependencies
pip install -r requirements.txt

# Run with Gunicorn (recommended for production)
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend Deployment (Production):
```bash
# Build for production
npm run build

# The dist/ folder contains the production build
# Upload the contents to your web server
```

## 🛡️ Environment Variables

### Backend (.env):
- `MONGODB_URL`: MongoDB connection string
- `DATABASE_NAME`: Database name
- `SECRET_KEY`: JWT secret key
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time
- `SMTP_SERVER`: Email server (optional)
- `REDIS_URL`: Redis connection for Celery (optional)

### Frontend (.env):
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=ASIA Insurance Agency
```

## 🧪 API Endpoints

### Authentication:
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user

### Leads Management:
- `GET /api/leads` - Get all leads
- `POST /api/leads` - Create new lead
- `GET /api/leads/{id}` - Get lead by ID
- `PUT /api/leads/{id}` - Update lead
- `DELETE /api/leads/{id}` - Delete lead

### Dashboard:
- `GET /api/dashboard/stats` - Get dashboard statistics
- `GET /api/dashboard/recent` - Get recent activities

## 📞 Contact Information

**ASIA - Amandeep Singh Insurance Agency**
- 📧 Email: info@asiainsurance.com
- 📱 Phone: (XXX) XXX-XXXX  
- 🌐 Website: https://asiainsurance.com

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is proprietary software owned by ASIA Insurance Agency.

## 🆘 Troubleshooting

### Common Issues:

1. **MongoDB Connection Error:**
   - Ensure MongoDB is running: `brew services start mongodb-community`
   - Check your `MONGODB_URL` in the `.env` file

2. **Port Already in Use:**
   - Backend: Change port in `main.py` or kill the process using port 8000
   - Frontend: Vite will automatically suggest an alternative port

3. **Module Not Found Errors:**
   - Backend: Make sure you're in the virtual environment and run `pip install -r requirements.txt`
   - Frontend: Run `npm install` in the frontend directory

4. **CORS Errors:**
   - Ensure the backend CORS configuration allows your frontend URL
   - Check that both servers are running on the expected ports

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [MongoDB Documentation](https://docs.mongodb.com/)

---

**Built with ❤️ for ASIA Insurance Agency**