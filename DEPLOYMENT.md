# Cloud Deployment Guide

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Prerequisites](#prerequisites)
4. [Environment Variables](#environment-variables)
5. [Local Development Setup](#local-development-setup)
6. [Cloud Deployment Options](#cloud-deployment-options)
7. [Database Setup](#database-setup)
8. [API Endpoints](#api-endpoints)
9. [Security Considerations](#security-considerations)
10. [Monitoring & Troubleshooting](#monitoring--troubleshooting)

---

## Project Overview

**Tamil Nadu Election Campaign Platform** - A full-stack web application for generating hyper-personalized campaign messages using AI. The platform enables political campaigns to:

- Browse and filter voter data from Supabase
- Generate personalized Tamil and English campaign messages using OpenAI
- Send SMS messages via Twilio to selected voters
- Manage voter categories and issue-based messaging

### Technology Stack

**Frontend:**
- React 19.2.0
- React Scripts 5.0.1
- XLSX for data processing

**Backend:**
- FastAPI (Python)
- Uvicorn ASGI server
- OpenAI API (via Azure endpoint)
- Supabase (PostgreSQL database)
- Twilio (SMS messaging)

**Infrastructure:**
- Database: Supabase (PostgreSQL)
- AI Service: OpenAI (via Azure endpoint)
- SMS Service: Twilio

---

## Architecture

```
┌─────────────────┐
│   React App     │  (Frontend - Static Hosting)
│   (Port 3000)   │
└────────┬────────┘
         │
         │ HTTP Requests
         │
┌────────▼────────┐
│   FastAPI       │  (Backend - Serverless/Container)
│   (Port 8000)   │
└────────┬────────┘
         │
    ┌────┴────┬──────────┬──────────┐
    │         │          │          │
┌───▼───┐ ┌──▼───┐  ┌───▼────┐ ┌───▼────┐
│Supabase│ │OpenAI│  │ Twilio │ │ Azure  │
│   DB   │ │ API  │  │  SMS   │ │Endpoint│
└────────┘ └──────┘  └────────┘ └────────┘
```

### Data Flow

1. **Voter Data**: Stored in Supabase `voters_master` table
2. **Message Generation**: 
   - User selects 6 voters → Frontend sends voter IDs to backend
   - Backend fetches voter data from Supabase
   - Backend generates personalized messages using OpenAI (via Azure)
   - Messages returned to frontend
3. **SMS Sending**:
   - User clicks "Send Message" → Frontend sends 6 messages to backend
   - Backend sends each message to corresponding phone number from `.env`
   - Twilio handles SMS delivery

---

## Prerequisites

### Required Services

1. **Supabase Account**
   - PostgreSQL database
   - Table: `voters_master` with voter data

2. **OpenAI Account**
   - API key for message generation
   - Azure endpoint configured (optional, for Azure OpenAI)

3. **Twilio Account**
   - Account SID and Auth Token
   - Phone number for sending SMS

4. **Cloud Provider Account** (choose one)
   - Vercel (recommended for serverless)
   - AWS (Lambda + API Gateway or ECS)
   - Azure (App Service or Functions)
   - Google Cloud (Cloud Run or App Engine)

### Required Tools

- **Node.js** 14+ and npm (for frontend)
- **Python** 3.8+ and pip (for backend)
- **Git** (for version control)

---

## Environment Variables

### Backend Environment Variables

Create a `.env` file in `python-backend/` directory:

```env
# Required - Database
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key

# Required - AI Service
OPENAI_API_KEY=sk-...
AZURE_ENDPOINT=https://your-resource.openai.azure.com  # Optional, for Azure OpenAI

# Required - SMS Service
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# Required - SMS Recipients (exactly 6 numbers, comma-separated)
PHONE_NUMBER=+919876543210,+919876543211,+919876543212,+919876543213,+919876543214,+919876543215

# Optional
OPENAI_MODEL=gpt-4o-mini
ALLOWED_ORIGINS=*
```

### Frontend Environment Variables

Create a `.env` file in `web-interface/` directory:

```env
REACT_APP_API_BASE_URL=https://your-backend-url.vercel.app
# or
REACT_APP_API_BASE_URL=http://localhost:8000  # for local development
```

---

## Local Development Setup

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd python-backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file** with all required variables (see above)

5. **Run the server:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Verify backend:**
   ```bash
   curl http://localhost:8000/api/health
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd web-interface
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Create `.env` file:**
   ```env
   REACT_APP_API_BASE_URL=http://localhost:8000
   ```

4. **Run the development server:**
   ```bash
   npm start
   ```

5. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

---

## Cloud Deployment Options

### Option 1: Vercel (Recommended - Serverless)

#### Backend Deployment on Vercel

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Navigate to backend directory:**
   ```bash
   cd python-backend
   ```

3. **Deploy:**
   ```bash
   vercel
   ```

4. **Set environment variables in Vercel Dashboard:**
   - Go to Project Settings → Environment Variables
   - Add all variables from `.env` file

5. **The `vercel.json` is already configured:**
   ```json
   {
     "version": 2,
     "builds": [
       { "src": "main.py", "use": "@vercel/python" }
     ],
     "routes": [
       { "src": "/(.*)", "dest": "/main.py" }
     ]
   }
   ```

#### Frontend Deployment on Vercel

1. **Navigate to frontend directory:**
   ```bash
   cd web-interface
   ```

2. **Build the app:**
   ```bash
   npm run build
   ```

3. **Deploy:**
   ```bash
   vercel
   ```

4. **Set environment variable:**
   - `REACT_APP_API_BASE_URL` = your backend Vercel URL

**Note:** Vercel automatically detects React apps and configures build settings.

---

### Option 2: AWS Deployment

#### Backend on AWS Lambda + API Gateway

1. **Create deployment package:**
   ```bash
   cd python-backend
   pip install -r requirements.txt -t .
   zip -r lambda-deployment.zip . -x "*.pyc" "__pycache__/*" "*.git*"
   ```

2. **Create Lambda function:**
   - Upload `lambda-deployment.zip`
   - Set handler: `main.handler`
   - Set runtime: Python 3.9+
   - Set environment variables

3. **Create API Gateway:**
   - Create REST API
   - Create resource: `{proxy+}`
   - Create method: ANY
   - Integration: Lambda Proxy
   - Deploy API

#### Frontend on AWS S3 + CloudFront

1. **Build frontend:**
   ```bash
   cd web-interface
   npm run build
   ```

2. **Upload to S3:**
   ```bash
   aws s3 sync build/ s3://your-bucket-name --delete
   ```

3. **Configure CloudFront:**
   - Create distribution
   - Origin: S3 bucket
   - Default root object: `index.html`
   - Error pages: 404 → `/index.html` (for React Router)

---

### Option 3: Azure Deployment

#### Backend on Azure App Service

1. **Create App Service:**
   ```bash
   az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name myAppName --runtime "PYTHON|3.9"
   ```

2. **Deploy code:**
   ```bash
   cd python-backend
   az webapp up --resource-group myResourceGroup --name myAppName
   ```

3. **Set environment variables:**
   ```bash
   az webapp config appsettings set --resource-group myResourceGroup --name myAppName --settings @.env
   ```

#### Frontend on Azure Static Web Apps

1. **Create Static Web App:**
   ```bash
   az staticwebapp create --name myAppName --resource-group myResourceGroup
   ```

2. **Deploy:**
   ```bash
   cd web-interface
   npm run build
   az staticwebapp deploy --name myAppName --resource-group myResourceGroup --app-location "./" --output-location "build"
   ```

---

### Option 4: Docker Deployment

#### Create Dockerfile for Backend

Create `python-backend/Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Create Dockerfile for Frontend

Create `web-interface/Dockerfile`:
```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

#### Deploy with Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  backend:
    build: ./python-backend
    ports:
      - "8000:8000"
    environment:
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_KEY=${SUPABASE_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      # ... other env vars
    env_file:
      - ./python-backend/.env

  frontend:
    build: ./web-interface
    ports:
      - "80:80"
    depends_on:
      - backend
    environment:
      - REACT_APP_API_BASE_URL=http://localhost:8000
```

Deploy:
```bash
docker-compose up -d
```

---

## Database Setup

### Supabase Configuration

1. **Create Supabase Project:**
   - Go to https://supabase.com
   - Create new project
   - Note your project URL and anon key

2. **Create `voters_master` Table:**

   Run this SQL in Supabase SQL Editor:

   ```sql
   CREATE TABLE voters_master (
     voter_id TEXT PRIMARY KEY,
     voter_name TEXT,
     father_or_husband_name TEXT,
     gender TEXT,
     age INTEGER,
     door_no TEXT,
     booth_number TEXT,
     assembly_constituency TEXT,
     source_file TEXT,
     raw_data JSONB,
     ward TEXT,
     area TEXT,
     street TEXT,
     village TEXT,
     district TEXT,
     voter_category TEXT,
     issue_category TEXT,
     issue_description TEXT,
     phone_number TEXT,
     mobile TEXT,
     contact TEXT
   );

   -- Create indexes for better query performance
   CREATE INDEX idx_voter_category ON voters_master(voter_category);
   CREATE INDEX idx_issue_category ON voters_master(issue_category);
   CREATE INDEX idx_gender ON voters_master(gender);
   CREATE INDEX idx_village ON voters_master(village);
   CREATE INDEX idx_district ON voters_master(district);
   CREATE INDEX idx_ward ON voters_master(ward);
   CREATE INDEX idx_age ON voters_master(age);
   ```

3. **Import Data:**
   - Use Supabase Dashboard → Table Editor → Import CSV
   - Or use Supabase API to bulk insert

---

## API Endpoints

### Health Check
- `GET /` or `GET /api/health`
- Returns API status and database connection

### Voters
- `GET /api/voters` - Fetch voters with filtering
  - Query params: `voter_category`, `issue_category`, `gender`, `village`, `district`, `ward`, `age_min`, `age_max`, `limit`, `offset`, `search`
- `GET /api/voters/{voter_id}` - Get specific voter
- `GET /api/voters/filters/options` - Get filter dropdown values

### Campaign Generation
- `POST /api/generate-campaign-from-ids` - Generate messages from voter IDs
  - Body: `{ "voter_ids": ["id1", "id2", ...] }`
  - Returns: Array of results with generated messages

### Voter Classification
- `POST /api/classify-voter` - Classify voters into categories
  - Body: `{ "voters": [...] }`

### SMS
- `POST /api/send-sms` - Send single SMS
  - Body: `{ "phone_number": "+1234567890", "message": "text", "voter_id": "optional" }`
- `POST /api/send-bulk-sms` - Send 6 SMS to 6 phone numbers
  - Body: `{ "messages": [{"voter_id": "id1", "message": "msg1"}, ...] }`
  - Requires exactly 6 messages and 6 phone numbers in `PHONE_NUMBER` env var

---

## Security Considerations

### Environment Variables
- **Never commit `.env` files** to version control
- Use environment variable management in cloud platforms
- Rotate API keys regularly
- Use separate keys for development/production

### CORS Configuration
- Set `ALLOWED_ORIGINS` to specific domains in production
- Avoid using `*` in production

### Database Security
- Use Supabase Row Level Security (RLS) policies
- Limit API key permissions (use anon key, not service role key)
- Enable database backups

### API Security
- Implement rate limiting (consider using FastAPI middleware)
- Add authentication if needed (JWT tokens)
- Validate all input data
- Use HTTPS only in production

### SMS Security
- Validate phone numbers before sending
- Implement rate limiting for SMS endpoints
- Monitor Twilio usage to prevent abuse

---

## Monitoring & Troubleshooting

### Health Check Monitoring

Set up monitoring for:
- `GET /api/health` endpoint
- Check database connection status
- Verify API key configurations

### Common Issues

#### Backend Issues

**Issue: "Missing OPENAI_API_KEY in .env"**
- Solution: Ensure all environment variables are set in cloud platform

**Issue: Supabase connection errors**
- Check: Supabase URL and key are correct
- Check: Table `voters_master` exists
- Check: Network connectivity

**Issue: Twilio SMS fails**
- Check: Twilio credentials are valid
- Check: Phone number format (must include country code)
- Check: Twilio account has sufficient credits

**Issue: CORS errors**
- Solution: Set `ALLOWED_ORIGINS` to your frontend domain
- Check: Backend CORS middleware configuration

#### Frontend Issues

**Issue: API calls fail**
- Check: `REACT_APP_API_BASE_URL` is set correctly
- Check: Backend is accessible from frontend domain
- Check: CORS is configured on backend

**Issue: Build fails**
- Check: Node.js version (14+)
- Clear `node_modules` and reinstall: `rm -rf node_modules && npm install`

### Logging

**Backend Logging:**
- FastAPI automatically logs requests
- Add custom logging for errors:
  ```python
  import logging
  logging.error(f"Error: {e}")
  ```

**Frontend Logging:**
- Use browser console for debugging
- Consider adding error tracking (Sentry, etc.)

### Performance Optimization

1. **Database:**
   - Add indexes on frequently filtered columns
   - Use pagination for large datasets
   - Consider caching filter options

2. **API:**
   - Implement response caching where appropriate
   - Use async operations for I/O-bound tasks
   - Monitor API response times

3. **Frontend:**
   - Optimize bundle size (code splitting)
   - Use lazy loading for components
   - Implement proper error boundaries

---

## Deployment Checklist

### Pre-Deployment

- [ ] All environment variables configured
- [ ] Database schema created and data imported
- [ ] API keys tested and working
- [ ] Frontend builds successfully
- [ ] Backend runs locally without errors
- [ ] All API endpoints tested

### Deployment

- [ ] Backend deployed and accessible
- [ ] Frontend deployed and accessible
- [ ] Environment variables set in cloud platform
- [ ] CORS configured correctly
- [ ] Health check endpoint responding

### Post-Deployment

- [ ] Test all major workflows:
  - [ ] Fetch voters
  - [ ] Filter voters
  - [ ] Generate messages (exactly 6 voters)
  - [ ] Send SMS messages
- [ ] Monitor error logs
- [ ] Set up uptime monitoring
- [ ] Configure backups (database)

---

## Support & Resources

- **Backend Documentation:** `python-backend/README.md`
- **Frontend Documentation:** `web-interface/README.md`
- **Supabase Docs:** https://supabase.com/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **Vercel Docs:** https://vercel.com/docs
- **Twilio Docs:** https://www.twilio.com/docs

---

## Version History

- **v1.0.0** - Initial deployment guide
  - Support for Vercel, AWS, Azure, Docker
  - Complete environment variable documentation
  - Security best practices
  - Troubleshooting guide


