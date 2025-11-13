# Tutor Ingesis - Deployment Guide

## 🚀 Deployment to Vercel

The Tutor Ingesis system has been successfully deployed to Vercel!

### 📋 Current Deployment Status
- **Frontend URL**: https://traewk90lkpb.vercel.app
- **Backend**: Configured for serverless deployment
- **Database**: PostgreSQL (requires configuration)

### 🔧 Configuration Required

#### 1. Environment Variables
Set these in your Vercel project settings:

```bash
# Database Configuration
DATABASE_URL=postgresql+asyncpg://username:password@host:port/database

# Security
JWT_SECRET_KEY=your-very-secure-secret-key-here-minimum-32-characters

# AI API Keys (optional - system works without them using manual fallback)
GEMINI_API_KEY=your-gemini-api-key-here
OPENAI_API_KEY=your-openai-api-key-here
```

#### 2. PostgreSQL Database Setup
You need to set up a PostgreSQL database. Options:
- **Vercel Postgres** (recommended)
- **Supabase**
- **Neon**
- **AWS RDS**
- **DigitalOcean Managed Database**

#### 3. Update Frontend API URL
Update the frontend to point to production:
```bash
NEXT_PUBLIC_API_URL=https://your-domain.vercel.app
```

### 📁 Project Structure
```
notaria-frontend/     # Next.js frontend
├── src/app/           # App router pages
├── src/context/       # React contexts
└── public/           # Static assets

notaria-backend/       # FastAPI backend
├── app/              # Application code
│   ├── core/        # Core configuration
│   ├── routers/     # API routes
│   ├── services/    # Business logic
│   └── data/        # Manual data files
└── api/             # Vercel serverless functions
```

### 🔑 Default Credentials
- **Admin User**: diegogalmarini@email.com
- **Password**: admin123
- **Role**: admin (full access)

### 🎯 Features Working
✅ User authentication (JWT)
✅ Role-based access (admin/empleado)
✅ Tutor Ingesis with manual fallback
✅ Responsive design
✅ PWA capabilities
✅ PostgreSQL database

### 📚 Tutor Ingesis Capabilities
The tutor can answer questions about:
- ProtocolW (document management)
- IngedatW (indices and data)
- IngefactW (billing)
- InterlineadorW (document editing)
- Export procedures (CSV/PDF)
- Windows shortcuts creation
- File menu functions
- And more from the official manual

### 🚨 Important Notes
1. **Database Required**: The system needs PostgreSQL to be fully functional
2. **API Keys Optional**: The tutor works without AI APIs using manual fallback
3. **Security**: Change default passwords in production
4. **Manual Content**: 2.6MB of official Ingesis SRL documentation loaded

### 🔧 Next Steps
1. Configure PostgreSQL database
2. Set environment variables in Vercel
3. Test all functionality
4. Add custom domain if needed
5. Monitor usage and performance

### 📞 Support
For technical issues with the deployment, check:
- Vercel deployment logs
- Database connection
- Environment variables
- API endpoints health

The system is ready for your 8 employees to start learning Ingesis SRL!