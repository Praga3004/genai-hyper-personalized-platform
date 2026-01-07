# Quick Deployment Checklist

## Pre-Deployment Setup

### 1. Service Accounts & API Keys
- [ ] Supabase project created
- [ ] Supabase URL and anon key obtained
- [ ] OpenAI API key obtained
- [ ] Azure endpoint URL (if using Azure OpenAI)
- [ ] Twilio account created
- [ ] Twilio Account SID and Auth Token obtained
- [ ] Twilio phone number obtained
- [ ] 6 recipient phone numbers identified (for PHONE_NUMBER env var)

### 2. Database Setup
- [ ] Supabase `voters_master` table created
- [ ] Database indexes created (voter_category, issue_category, gender, village, district, ward, age)
- [ ] Voter data imported to Supabase
- [ ] Database connection tested

### 3. Local Testing
- [ ] Backend runs locally (`uvicorn main:app --reload`)
- [ ] Frontend runs locally (`npm start`)
- [ ] Health check endpoint works (`/api/health`)
- [ ] Can fetch voters from database
- [ ] Can generate messages for 6 voters
- [ ] Can send SMS (test with one message)

---

## Cloud Platform Selection

Choose one deployment option:

- [ ] **Vercel** (Recommended - Easiest)
- [ ] **AWS** (Lambda + S3/CloudFront)
- [ ] **Azure** (App Service + Static Web Apps)
- [ ] **Docker** (Any container platform)

---

## Backend Deployment

### Environment Variables Required
```env
SUPABASE_URL=...
SUPABASE_KEY=...
OPENAI_API_KEY=...
AZURE_ENDPOINT=...  # Optional
TWILIO_ACCOUNT_SID=...
TWILIO_AUTH_TOKEN=...
TWILIO_PHONE_NUMBER=...
PHONE_NUMBER=+91xxx,+91xxx,+91xxx,+91xxx,+91xxx,+91xxx
OPENAI_MODEL=gpt-4o-mini  # Optional
ALLOWED_ORIGINS=*  # Set to your frontend domain in production
```

### Vercel Deployment
- [ ] Install Vercel CLI: `npm i -g vercel`
- [ ] Navigate to `python-backend/`
- [ ] Run `vercel` and follow prompts
- [ ] Set all environment variables in Vercel dashboard
- [ ] Note the backend URL (e.g., `https://your-app.vercel.app`)

### AWS Deployment
- [ ] Create Lambda function
- [ ] Upload deployment package (zip with dependencies)
- [ ] Set environment variables in Lambda
- [ ] Create API Gateway
- [ ] Deploy and note API Gateway URL

### Azure Deployment
- [ ] Create App Service
- [ ] Deploy code via Azure CLI or Git
- [ ] Set application settings (environment variables)
- [ ] Note App Service URL

### Docker Deployment
- [ ] Build Docker image: `docker build -t backend .`
- [ ] Run container with environment variables
- [ ] Expose port 8000
- [ ] Note container URL

### Backend Verification
- [ ] Health check works: `curl https://your-backend-url/api/health`
- [ ] Database connection shows as "connected"
- [ ] All endpoints accessible

---

## Frontend Deployment

### Environment Variables Required
```env
REACT_APP_API_BASE_URL=https://your-backend-url
```

### Vercel Deployment
- [ ] Navigate to `web-interface/`
- [ ] Run `vercel` and follow prompts
- [ ] Set `REACT_APP_API_BASE_URL` environment variable
- [ ] Note the frontend URL

### AWS S3 + CloudFront
- [ ] Build frontend: `npm run build`
- [ ] Upload `build/` folder to S3 bucket
- [ ] Configure CloudFront distribution
- [ ] Set error page 404 → `/index.html`
- [ ] Note CloudFront URL

### Azure Static Web Apps
- [ ] Build frontend: `npm run build`
- [ ] Deploy via Azure CLI or GitHub Actions
- [ ] Set `REACT_APP_API_BASE_URL` in configuration
- [ ] Note Static Web App URL

### Docker Deployment
- [ ] Build Docker image: `docker build -t frontend .`
- [ ] Run container with environment variable
- [ ] Expose port 80
- [ ] Note container URL

### Frontend Verification
- [ ] Frontend loads in browser
- [ ] Can see voter list
- [ ] Can filter voters
- [ ] Can select exactly 6 voters
- [ ] Can generate messages
- [ ] Can send SMS messages

---

## Post-Deployment Testing

### Functional Tests
- [ ] **Voter Fetching**: Can load voters from database
- [ ] **Filtering**: All filters work (category, issue, gender, location, age)
- [ ] **Selection**: Can select exactly 6 voters (no more, no less)
- [ ] **Message Generation**: Generates 6 personalized messages
- [ ] **SMS Sending**: Sends 6 messages to 6 phone numbers correctly
- [ ] **Error Handling**: Shows appropriate errors for invalid inputs

### Integration Tests
- [ ] Frontend can communicate with backend
- [ ] Backend can connect to Supabase
- [ ] Backend can call OpenAI API
- [ ] Backend can send SMS via Twilio
- [ ] CORS is configured correctly

### Performance Tests
- [ ] Page load time < 3 seconds
- [ ] API response time < 2 seconds
- [ ] Message generation completes in reasonable time
- [ ] SMS sending completes successfully

---

## Security Checklist

- [ ] All `.env` files are in `.gitignore`
- [ ] No API keys committed to repository
- [ ] `ALLOWED_ORIGINS` set to specific domain (not `*`)
- [ ] HTTPS enabled for all endpoints
- [ ] Database RLS policies configured (if needed)
- [ ] API rate limiting considered
- [ ] Error messages don't expose sensitive information

---

## Monitoring Setup

- [ ] Health check endpoint monitored
- [ ] Error logging configured
- [ ] Uptime monitoring set up
- [ ] Database backup configured
- [ ] API usage monitoring (OpenAI, Twilio)

---

## Documentation

- [ ] Deployment guide reviewed
- [ ] Environment variables documented
- [ ] API endpoints documented
- [ ] Troubleshooting guide accessible
- [ ] Team members have access to deployment info

---

## Rollback Plan

- [ ] Previous version tagged in Git
- [ ] Database backup available
- [ ] Rollback procedure documented
- [ ] Team knows how to rollback if needed

---

## Final Verification

- [ ] Application is accessible to end users
- [ ] All features working in production
- [ ] No critical errors in logs
- [ ] Performance is acceptable
- [ ] Team notified of deployment

---

## Quick Commands Reference

### Backend
```bash
# Local development
cd python-backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

# Vercel deployment
vercel

# Health check
curl https://your-backend-url/api/health
```

### Frontend
```bash
# Local development
cd web-interface
npm install
npm start

# Build for production
npm run build

# Vercel deployment
vercel
```

### Testing
```bash
# Test backend endpoints
cd python-backend
python test_endpoints.py
```

---

**Last Updated:** [Current Date]
**Deployment Version:** v1.0.0


