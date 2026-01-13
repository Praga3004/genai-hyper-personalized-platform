# Backend API

FastAPI backend for the Tamil Nadu Election Campaign Platform - generating hyper-personalized campaign messages using AI.

## Prerequisites

1. Python 3.8 or higher
2. pip package manager
3. Supabase account with a database table `voters_master`
4. OpenAI API key

## Installation

1. **Install dependencies:**
   ```bash
   cd python-backend
   pip install -r requirements.txt
   ```

2. **Create environment file:**
   Create a `.env` file in the `python-backend` directory with:
   ```env
   OPENAI_API_KEY=sk-...
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your_supabase_anon_key
   OPENAI_MODEL=gpt-4o-mini
   ALLOWED_ORIGINS=*
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   TWILIO_PHONE_NUMBER=+1234567890
   PHONE_NUMBER=+919876543210,+919876543211,+919876543212,+919876543213,+919876543214,+919876543215
   AUDIO_FILES=['AudioStuffs/EPS-Sample1.wav', 'AudioStuffs/EPS-Sample2.wav', 'AudioStuffs/EPS-Sample3.wav', 'AudioStuffs/EPS-Sample4.wav', 'AudioStuffs/EPS-Sample5.wav', 'AudioStuffs/EPS-Sample6.wav']
   ```

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | Your OpenAI API key for generating messages |
| `SUPABASE_URL` | Yes | Your Supabase project URL |
| `SUPABASE_KEY` | Yes | Your Supabase anon/public key |
| `OPENAI_MODEL` | No | OpenAI model to use (default: `gpt-4o-mini`) |
| `ALLOWED_ORIGINS` | No | Comma-separated CORS origins (default: `*`) |
| `TWILIO_ACCOUNT_SID` | No | Twilio Account SID for SMS functionality |
| `TWILIO_AUTH_TOKEN` | No | Twilio Auth Token for SMS functionality |
| `TWILIO_PHONE_NUMBER` | No | Twilio phone number to send SMS from (format: +1234567890) |
| `PHONE_NUMBER` | No | List of phone numbers in Python list format (e.g., `['+919876543210', '+919876543211', ...]`) |
| `AUDIO_FILES` | No | List of audio file paths matching phone numbers by index (e.g., `['AudioStuffs/EPS-Sample1.wav', 'AudioStuffs/EPS-Sample2 wav', ...]`). Must have same count as phone numbers. |
### Database Setup

The backend expects a Supabase table named `voters_master` with the following columns:

- `voter_id` (primary key)
- `voter_name`
- `gender`
- `age`
- `booth_number`
- `ward`
- `area`
- `street`
- `village`
- `district`
- `voter_category`
- `issue_category`
- `issue_description`

## Running the Server

### Local Development

```bash
# Using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or using Python
python -m uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Production (Vercel)

The backend is configured for Vercel deployment. The `vercel.json` file handles routing.

## API Endpoints

### Health Check
- `GET /` or `GET /api/health` - Returns API status and database connection status

### Voters
- `GET /api/voters` - Fetch voters with filtering (supports: voter_category, issue_category, gender, village, district, ward, age_min, age_max, search, limit, offset)
- `GET /api/voters/{voter_id}` - Get specific voter by ID
- `GET /api/voters/filters/options` - Get unique values for filter dropdowns

### Campaign Generation
- `POST /api/generate-campaign-from-ids` - Generate personalized campaign messages from voter IDs (fetches from Supabase)
- `POST /api/classify-voter` - Classify voters into categories (uses existing voter_category from DB if available)

### SMS
- `POST /api/send-sms` - Send SMS message via Twilio
  - Request body: `{ "phone_number": "+1234567890", "message": "Your message", "voter_id": "optional" }`
- `POST /api/send-bulk-sms` - Send 6 SMS messages to 6 phone numbers from .env
  - Request body: `{ "messages": [{"voter_id": "id1", "message": "msg1"}, ...] }`
  - Requires exactly 6 messages and 6 phone numbers in PHONE_NUMBER env variable

## Testing

### Test Health Check
```bash
curl http://localhost:8000/api/health
```

### Test Filter Options
```bash
curl http://localhost:8000/api/voters/filters/options
```

### Test Voter Fetch
```bash
curl "http://localhost:8000/api/voters?limit=5"
```

### Test Campaign Generation
```bash
curl -X POST http://localhost:8000/api/generate-campaign-from-ids \
  -H "Content-Type: application/json" \
  -d '{"voter_ids": ["XKR0630483"]}'
```

## Troubleshooting

### Issue: "Missing OPENAI_API_KEY in .env"
- **Solution**: Check that `.env` file exists and contains `OPENAI_API_KEY=your_key`

### Issue: "Missing SUPABASE_URL in .env"
- **Solution**: Add your Supabase project URL to `.env` file

### Issue: Supabase connection errors
- **Check**: Your Supabase URL and key are correct
- **Check**: Table `voters_master` exists
- **Check**: Your Supabase key has read permissions

### Issue: CORS errors in browser
- **Solution**: For production, set `ALLOWED_ORIGINS` in `.env` to your frontend domain
- **Example**: `ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com`

## Performance Considerations

1. **Supabase Queries**: Filter options endpoint loads up to 5000 records per field. Consider using Supabase RPC functions for better performance on large datasets.

2. **Database Indexing**: Ensure proper indexes on frequently filtered columns:
   - `voter_category`
   - `issue_category`
   - `gender`
   - `village`
   - `district`
   - `ward`
   - `age`

## Security Notes

1. **Never commit `.env` file** - It contains sensitive API keys
2. **Use environment variables** in production (Vercel, Heroku, etc.)
3. **Restrict CORS origins** in production
4. **Use Supabase RLS (Row Level Security)** to protect voter data
5. **Rate limit API endpoints** to prevent abuse

