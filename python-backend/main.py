import os
import json
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
from supabase import create_client, Client
from prompt import get_prompt_template, format_prompt
from pathlib import Path
from twilio.rest import Client 

# -------------------------------------------------
# Load environment variables
# -------------------------------------------------
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
AUDIO_FILES_ENV = os.getenv("AUDIO_FILES")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")


# Parse phone numbers from .env (comma-separated list)
PHONE_NUMBERS = eval(PHONE_NUMBER) if PHONE_NUMBER else []

if AUDIO_FILES_ENV and AUDIO_FILES_ENV != "[]":
    AUDIO_FILES = eval(AUDIO_FILES_ENV)
else:
    AUDIO_FILES = [f"AudioStuffs/EPS-Sample{i+1}.wav" for i in range(len(PHONE_NUMBERS))]

# Validate that counts match
if len(PHONE_NUMBERS) != len(AUDIO_FILES):
    print(f"⚠️ Warning: {len(PHONE_NUMBERS)} phone numbers but {len(AUDIO_FILES)} audio files. They should match!")

print(f"Loaded {len(PHONE_NUMBERS)} phone numbers")
print(f"Loaded {len(AUDIO_FILES)} audio files")

if not OPENAI_API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY in .env")

if not SUPABASE_URL:
    raise RuntimeError("Missing SUPABASE_URL in .env")

if not SUPABASE_KEY:
    raise RuntimeError("Missing SUPABASE_KEY in .env")

# -------------------------------------------------
# Initialize API Clients
# -------------------------------------------------
client = OpenAI(base_url=AZURE_ENDPOINT, api_key=OPENAI_API_KEY)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize Twilio client if credentials are available
twilio_client = None
if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
    try:
        twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    except Exception as e:
        print(f"⚠️ Twilio initialization failed: {e}")


GEN_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # Default to gpt-4o-mini, can be overridden

CATEGORY_DESCRIPTIONS = {
    "Youth / First-time Voter": "Age roughly 18–22, voting for the first time. Focus on education, employment opportunities, digital access, and social infrastructure. Energetic, tech-savvy, and looking for opportunities to build their future.",
    "Working Professional": "Employed professionals, typically age 25–55. Focus on transportation, connectivity, power supply, urban infrastructure, housing, and cost of living. Value efficiency, quality of life, and work-life balance.",
    "Women": "Female voters of all ages. Primary concerns include safety (road, pedestrian, public safety), health, education, social infrastructure, family welfare, and women's rights. Focus on creating safe and supportive environments.",
    "Senior Citizens": "Age 60+ voters. Focus on water supply, groundwater management, health services, pensions, healthcare, social infrastructure, and quality of life in their golden years. Value stability and care.",
    "Daily Wage / Service Worker": "Daily wage earners and service workers. Focus on affordable transportation, housing, rentals, urban cost of living, and basic infrastructure. Need accessible and affordable services for daily life.",
}

# -------------------------------------------------
# FastAPI Setup
# -------------------------------------------------
app = FastAPI(
    title="Election Campaign API",
    description="API for generating personalized election campaign messages",
    version="1.0.0"
)

# CORS configuration - allow frontend origins
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add exception handler for 404
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={
                "error": "Not Found",
                "message": f"The endpoint {request.url.path} was not found.",
                "available_endpoints": [
                    "/api/health",
                    "/api/voters",
                    "/api/voters/filters/options",
                    "/api/voters/{voter_id}",
                    "/api/generate-campaign-from-ids",
                    "/api/classify-voter",
                    "/api/generate-campaign"
                ]
            }
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

# -------------------------------------------------
# Health Check Endpoint
# -------------------------------------------------
@app.get("/")
@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    try:
        # Test Supabase connection
        test_query = supabase.table("voters_master").select("voter_id").limit(1).execute()
        db_status = "connected" if test_query.data is not None else "no_data"
        db_count = len(test_query.data) if test_query.data else 0
    except Exception as e:
        db_status = f"error: {str(e)}"
        db_count = 0
    
    return {
        "status": "healthy",
        "database": db_status,
        "database_records": db_count,
        "openai_configured": bool(OPENAI_API_KEY),
        "supabase_configured": bool(SUPABASE_URL and SUPABASE_KEY),
        "audio_enabled": False,  # Audio generation removed
        "endpoints": {
            "health": "/api/health",
            "voters": "/api/voters",
            "filter_options": "/api/voters/filters/options",
            "generate_campaign": "/api/generate-campaign-from-ids"
        }
    }

# -------------------------------------------------
# Data Models
# -------------------------------------------------
class VoterProfileIn(BaseModel):
    name: str
    age: int
    gender: str
    location: str
    booth_number: str
    ward: str
    area: str
    street: str
    village: str
    district: str
    voter_category: str
    issue_category: str
    issue_description: str



class BulkVoterRequest(BaseModel):
    voters: List[VoterProfileIn]


class VoterFilterRequest(BaseModel):
    voter_category: Optional[str] = None
    issue_category: Optional[str] = None
    gender: Optional[str] = None
    village: Optional[str] = None
    district: Optional[str] = None
    ward: Optional[str] = None
    age_min: Optional[int] = None
    age_max: Optional[int] = None
    limit: Optional[int] = 100
    offset: Optional[int] = 0
    search: Optional[str] = None  # Search in voter_name or voter_id

# -------------------------------------------------
# Helper: Voter Classification
# -------------------------------------------------
def classify_with_openai(v: Dict[str, Any]) -> Dict[str, Any]:
    system_prompt = (
        "You are a Tamil Nadu political strategist.\n"
        "Return ONLY JSON: { 'category': string, 'confidence': float }\n\n"
        "Categories:\n"
        + "\n".join([f"- {k}: {v}" for k, v in CATEGORY_DESCRIPTIONS.items()])
    )

    user_prompt = {
        "voter_profile": v,
        "instructions": [
            "Pick exactly one category.",
            "Confidence between 0 and 1."
        ]
    }

    try:
        resp = client.chat.completions.create(
            model=GEN_MODEL,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(user_prompt)},
            ],
        )
        return json.loads(resp.choices[0].message.content)

    except Exception as e:
        print("⚠️ Classification fallback:", e)
        # Simple fallback based on prompt.py categories
        age = v.get("age", 0)
        gender = str(v.get("gender", "")).lower()
        occupation = str(v.get("occupation", "")).lower()
        
        if age <= 22:
            return {"category": "Youth / First-time Voter", "confidence": 0.8}
        if age >= 60:
            return {"category": "Senior Citizens", "confidence": 0.8}
        if gender == "female":
            return {"category": "Women", "confidence": 0.7}
        if occupation in ["daily wage", "service worker", "laborer", "worker"]:
            return {"category": "Daily Wage / Service Worker", "confidence": 0.7}
        # Default to Working Professional for employed adults
        if age >= 25 and age < 60:
            return {"category": "Working Professional", "confidence": 0.6}
        return {"category": "Youth / First-time Voter", "confidence": 0.5}


@app.post("/api/classify-voter")
def classify_voter(req: BulkVoterRequest):
    results = []

    for v in req.voters:
        voter_dict = v.model_dump()
        
        # Use existing voter_category from database if available
        existing_category = voter_dict.get("voter_category", "").strip()
        
        if existing_category:
            # Category already exists in DB, use it
            results.append({
                **voter_dict,
                "category": existing_category,
                "confidence": 1.0  # Full confidence since it's from DB
            })
        else:
            # Only classify if category is missing
            classification = classify_with_openai(voter_dict)
            results.append({
                **voter_dict,
                "category": classification.get("category", "Working Professional"),
                "confidence": round(classification.get("confidence", 0.5), 3)
            })

    return {"results": results}


# -------------------------------------------------
# Supabase Voter Fetching Endpoints
# -------------------------------------------------
@app.get("/api/voters")
def get_voters(
    voter_category: Optional[str] = Query(None, description="Filter by voter category"),
    issue_category: Optional[str] = Query(None, description="Filter by issue category"),
    gender: Optional[str] = Query(None, description="Filter by gender"),
    village: Optional[str] = Query(None, description="Filter by village"),
    district: Optional[str] = Query(None, description="Filter by district"),
    ward: Optional[str] = Query(None, description="Filter by ward"),
    age_min: Optional[int] = Query(None, description="Minimum age"),
    age_max: Optional[int] = Query(None, description="Maximum age"),
    limit: int = Query(100, description="Limit results"),
    offset: int = Query(0, description="Offset for pagination"),
    search: Optional[str] = Query(None, description="Search in voter_name or voter_id")
):
    """Fetch voters from Supabase with filtering"""
    try:
        print(f" GET /api/voters called with filters: category={voter_category}, limit={limit}")
        
        query = supabase.table("voters_master").select("*")
        
        # Apply filters
        if voter_category and voter_category != "ALL":
            query = query.eq("voter_category", voter_category)
        if issue_category and issue_category != "ALL":
            query = query.eq("issue_category", issue_category)
            print(f"issue_category: {issue_category}")
            print(f"query: {query}")
        if gender and gender != "ALL":
            query = query.eq("gender", gender)
        if village and village != "ALL":
            query = query.eq("village", village)
        if district and district != "ALL":
            query = query.eq("district", district)
        if ward and ward != "ALL":
            query = query.eq("ward", ward)
        if age_min is not None:
            query = query.gte("age", age_min)
        if age_max is not None:
            query = query.lte("age", age_max)
        
        # Search functionality - search in voter_name (Supabase OR requires different syntax)
        if search:
            # For now, search in voter_name. For voter_id search, client can search by ID directly
            query = query.ilike("voter_name", f"%{search}%")
        
        # Pagination
        query = query.range(offset, offset + limit - 1)
        
        print(f"🔍 Executing Supabase query...")
        response = query.execute()
        print(f"✅ Query successful, found {len(response.data)} records")
        
        return {"results": response.data, "count": len(response.data)}
    
    except Exception as e:
        print(f"❌ Error fetching voters: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error fetching voters: {str(e)}")


@app.get("/api/voters/{voter_id}")
def get_voter_by_id(voter_id: str):
    """Get a specific voter by ID"""
    try:
        response = supabase.table("voters_master").select("*").eq("voter_id", voter_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Voter not found")
        return {"result": response.data[0]}
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error fetching voter: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/voters/filters/options")
def get_filter_options():
    """Get unique values for filter dropdowns"""
    try:
        # Get unique values for each filter field (limit to avoid memory issues)
        # Use distinct() or get all and filter in Python
        categories = supabase.table("voters_master").select("voter_category").limit(5000).execute()
        issue_categories = supabase.table("voters_master").select("issue_category").limit(5000).execute()
        genders = supabase.table("voters_master").select("gender").limit(5000).execute()
        villages = supabase.table("voters_master").select("village").limit(5000).execute()
        districts = supabase.table("voters_master").select("district").limit(5000).execute()
        wards = supabase.table("voters_master").select("ward").limit(5000).execute()
        
        # Extract unique values and filter out None/empty values
        def get_unique_values(data_list, key):
            unique_set = set()
            for r in data_list.data:
                val = r.get(key)
                if val is not None and str(val).strip():
                    unique_set.add(str(val).strip())
            return sorted(list(unique_set))
        
        return {
            "voter_categories": get_unique_values(categories, "voter_category"),
            "issue_categories": get_unique_values(issue_categories, "issue_category"),
            "genders": get_unique_values(genders, "gender"),
            "villages": get_unique_values(villages, "village"),
            "districts": get_unique_values(districts, "district"),
            "wards": get_unique_values(wards, "ward")
        }
    except Exception as e:
        print(f"❌ Error fetching filter options: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error fetching filter options: {str(e)}")

# -------------------------------------------------
# Image Fetch Endpoint
# -------------------------------------------------
# Prompt templates are now imported from prompt.py
# This allows for category-specific prompts based on voter_category and issue_category
# -------------------------------------------------
# Helper: Map Supabase voter data to campaign format
# -------------------------------------------------
def map_supabase_voter_to_campaign(voter_data: Dict[str, Any]) -> Dict[str, Any]:
    """Convert Supabase voter record to campaign generation format"""
    # Use voter_category from database if available, otherwise map based on profile
    age = voter_data.get("age", 0)
    gender = str(voter_data.get("gender", "")).strip()
    voter_category = str(voter_data.get("voter_category", "")).strip()
    occupation = str(voter_data.get("occupation", "")).lower() if voter_data.get("occupation") else ""
    
    # Use existing voter_category if it matches prompt.py categories, otherwise map
    valid_categories = [
        "Youth / First-time Voter",
        "Working Professional", 
        "Women",
        "Senior Citizens",
        "Daily Wage / Service Worker"
    ]
    
    if voter_category in valid_categories:
        message_category = voter_category
    elif age <= 22:
        message_category = "Youth / First-time Voter"
    elif age >= 60:
        message_category = "Senior Citizens"
    elif gender.lower() == "female":
        message_category = "Women"
    elif occupation in ["daily wage", "service worker", "laborer", "worker"]:
        message_category = "Daily Wage / Service Worker"
    else:
        message_category = "Working Professional"
    
    # Construct location string
    location_parts = []
    if voter_data.get("village"):
        location_parts.append(str(voter_data["village"]).strip())
    elif voter_data.get("area"):
        location_parts.append(str(voter_data["area"]).strip())
    if voter_data.get("ward"):
        location_parts.append(f"வார்ட் {str(voter_data['ward']).strip()}")
    location = ", ".join(location_parts) if location_parts else "உங்கள் பகுதி"
    
    # Get pain points from issue
    pain_points = []
    if voter_data.get("issue_category"):
        pain_points.append(str(voter_data["issue_category"]).strip())
    if voter_data.get("issue_description"):
        pain_points.append(str(voter_data["issue_description"]).strip())
    
    return {
        "id": voter_data.get("voter_id", ""),
        "name": str(voter_data.get("voter_name", "")).strip(),
        "age": age,
        "gender": gender,
        "location": location,
        "voter_history": "Unknown",
        "interests": [],
        "pain_points": pain_points,
        "category": message_category,
        "issue_category": voter_data.get("issue_category", ""),
        "issue_description": voter_data.get("issue_description", ""),
    }


# -------------------------------------------------
# Campaign Generation + Audio
# -------------------------------------------------
# -------------------------------------------------
# Generate Campaign from Voter IDs (Supabase)
# -------------------------------------------------
class GenerateCampaignFromIdsRequest(BaseModel):
    voter_ids: List[str]


@app.post("/api/generate-campaign-from-ids")
def generate_campaign_from_ids(req: GenerateCampaignFromIdsRequest):
    """Generate campaigns for voters by their IDs from Supabase"""
    results = []
    
    for voter_id in req.voter_ids:
        try:
            # Fetch voter from Supabase
            response = supabase.table("voters_master").select("*").eq("voter_id", voter_id).execute()
            
            if not response.data:
                results.append({
                    "voter_id": voter_id,
                    "error": "Voter not found in database"
                })
                continue
            
            voter_data = response.data[0]
            v = map_supabase_voter_to_campaign(voter_data)
            
            # Get voter category and issue category from database
            voter_category = str(voter_data.get("voter_category", "")).strip()
            issue_category = str(voter_data.get("issue_category", "")).strip()
            issue_description = str(voter_data.get("issue_description", "")).strip()
            
            # Get prompt template based on voter_category and issue_category
            template = get_prompt_template(voter_category, issue_category)
            base_msg = format_prompt(
                template,
                name=v["name"],
                location=v["location"],
                issue_description=issue_description if issue_description else f"{issue_category} பிரச்சனை"
            )
            
            # Generate message with OpenAI
            pain_points_str = ", ".join(v.get("pain_points", [])) if v.get("pain_points") else ""
            prompt = (
                f"Generate a Tamil political message.\n"
                f"Base message: {base_msg}\n"
                f"Pain points: {pain_points_str}\n"
                f"Specific issue: {v.get('issue_description', '')}\n\n"
                f"Respond ONLY in valid JSON format:\n"
                f"{{\n"
                f"  \"content_tamil\": \"string\",\n"
                f"  \"content_english\": \"same Tamil text spelled using English letters make sure add punctual and other perfectly \"\n"
                f"}}"
            )
            
            try:
                resp = client.chat.completions.create(
                    model=GEN_MODEL,
                    response_format={"type": "json_object"},
                    messages=[
                        {"role": "system", "content": "Tamil political message expert."},
                        {"role": "user", "content": prompt},
                    ],
                )
                data = json.loads(resp.choices[0].message.content)
                tamil_msg = data.get("content_tamil", base_msg)
                english_msg = data.get("content_english", base_msg)
            except Exception as e:
                print(f"⚠️ Error generating message: {e}")
                tamil_msg = base_msg
                english_msg = base_msg
            
            # Include all voter data and issue information
            results.append({
                **v,
                "id": voter_data.get("voter_id", ""),
                "voter_id": voter_data.get("voter_id", ""),
                "name": voter_data.get("voter_name", ""),
                "voter_name": voter_data.get("voter_name", ""),
                "age": voter_data.get("age", 0),
                "gender": voter_data.get("gender", ""),
                "village": voter_data.get("village", ""),
                "district": voter_data.get("district", ""),
                "ward": voter_data.get("ward", ""),
                "voter_category": voter_data.get("voter_category", ""),
                "issue_category": voter_data.get("issue_category", ""),
                "issue_description": voter_data.get("issue_description", ""),
                "phone_number": voter_data.get("phone_number") or voter_data.get("mobile") or voter_data.get("contact") or "",
                "base_message": base_msg,
                "final_message_tamil": tamil_msg,
                "final_message_english": english_msg
            })
            
        except Exception as e:
            print(f"❌ Error processing voter {voter_id}: {e}")
            results.append({
                "voter_id": voter_id,
                "error": str(e)
            })
    
    return {"results": results}


# -------------------------------------------------
# Send SMS via Twilio
# -------------------------------------------------
class SendSMSRequest(BaseModel):
    phone_number: str
    message: str
    voter_id: Optional[str] = None


@app.post("/api/send-sms")
def send_sms(req: SendSMSRequest):
    """Send SMS message via Twilio"""
    if not twilio_client:
        raise HTTPException(
            status_code=500, 
            detail="Twilio not configured. Please set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER in .env"
        )
    
    if not TWILIO_PHONE_NUMBER:
        raise HTTPException(
            status_code=500,
            detail="TWILIO_PHONE_NUMBER not configured in .env"
        )
    
    # Validate phone number format (basic validation)
    phone_number = req.phone_number.strip()
    if not phone_number:
        raise HTTPException(status_code=400, detail="Phone number is required")
    
    # Ensure phone number starts with + for international format
    if not phone_number.startswith("+"):
        # Assume Indian number if no country code
        if phone_number.startswith("0"):
            phone_number = "+91" + phone_number[1:]
        elif len(phone_number) == 10:
            phone_number = "+91" + phone_number
        else:
            phone_number = "+" + phone_number
    
    try:
        # Send SMS via Twilio
        message = twilio_client.messages.create(
            body=req.message,
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        
        return {
            "success": True,
            "message_sid": message.sid,
            "status": message.status,
            "phone_number": phone_number,
            "voter_id": req.voter_id
        }
    except Exception as e:
        print(f"❌ Twilio error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send SMS: {str(e)}"
        )


# -------------------------------------------------
# Bulk Send SMS to 6 numbers from .env
# -------------------------------------------------
class BulkSendSMSRequest(BaseModel):
    messages: List[Dict[str, str]]  # List of {voter_id, message}


@app.post("/api/send-bulk-sms")
def send_bulk_sms(req: BulkSendSMSRequest):
    """Send SMS messages with audio to phone numbers from .env"""
    if not twilio_client:
        raise HTTPException(
            status_code=500, 
            detail="Twilio not configured. Please set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER in .env"
        )
    
    if not TWILIO_PHONE_NUMBER:
        raise HTTPException(
            status_code=500,
            detail="TWILIO_PHONE_NUMBER not configured in .env"
        )
    
    if len(PHONE_NUMBERS) == 0:
        raise HTTPException(
            status_code=500,
            detail="No phone numbers configured in .env. Please set PHONE_NUMBER as a list."
        )

    if len(PHONE_NUMBERS) != len(AUDIO_FILES):
        raise HTTPException(
            status_code=500,
            detail=f"Phone numbers ({len(PHONE_NUMBERS)}) and audio files ({len(AUDIO_FILES)}) count mismatch. They must match!"
        )

    if len(req.messages) != len(PHONE_NUMBERS):
        raise HTTPException(
            status_code=400,
            detail=f"Must send exactly {len(PHONE_NUMBERS)} messages to match configured phone numbers. Received {len(req.messages)}"
        )
    
    results = []
    
    for i, msg_data in enumerate(req.messages):
        voter_id = msg_data.get("voter_id", "")
        message_text = msg_data.get("message", "")
        phone_number = PHONE_NUMBERS[i]
        audio_file = AUDIO_FILES[i]
        
        # Format phone number
        formatted_phone = phone_number.strip()
        if not formatted_phone.startswith("+"):
            if formatted_phone.startswith("0"):
                formatted_phone = "+91" + formatted_phone[1:]
            elif len(formatted_phone) == 10:
                formatted_phone = "+91" + formatted_phone
            else:
                formatted_phone = "+" + formatted_phone
        
        try:
            # Check if audio file exists and get absolute path
            has_audio = False
            audio_url = None
            
            if audio_file and audio_file.strip():
                audio_path = Path(audio_file)
                if audio_path.exists():
                    audio_url = f"file://{audio_path.absolute()}"
                    has_audio = True
                    print(f"Audio file found: {audio_file}")
                else:
                    print(f"Audio file not found: {audio_file}")
            
            # Send message via Twilio (with or without audio)
            if has_audio and audio_url:
                # Send MMS with audio
                twilio_message = twilio_client.messages.create(
                    body=message_text,
                    from_=TWILIO_PHONE_NUMBER,
                    to=formatted_phone,
                    media_url=[audio_url]
                )
                
                results.append({
                    "voter_id": voter_id,
                    "success": True,
                    "message_sid": twilio_message.sid,
                    "status": twilio_message.status,
                    "phone_number": formatted_phone,
                    "audio_file": audio_file,
                    "has_audio": True
                })
            else:
                # Send SMS without audio
                twilio_message = twilio_client.messages.create(
                    body=message_text,
                    from_=TWILIO_PHONE_NUMBER,
                    to=formatted_phone
                )
                
                results.append({
                    "voter_id": voter_id,
                    "success": True,
                    "message_sid": twilio_message.sid,
                    "status": twilio_message.status,
                    "phone_number": formatted_phone,
                    "audio_file": audio_file,
                    "has_audio": False,
                    "warning": "Audio file not found"
                })
                
        except Exception as e:
            print(f"Twilio error for {voter_id}: {e}")
            results.append({
                "voter_id": voter_id,
                "success": False,
                "error": str(e),
                "phone_number": formatted_phone,
                "audio_file": audio_file
            })
    
    return {
        "results": results,
        "total_sent": sum(1 for r in results if r.get("success")),
        "total_failed": sum(1 for r in results if not r.get("success")),
        "with_audio": sum(1 for r in results if r.get("has_audio", False)),
        "without_audio": sum(1 for r in results if r.get("success") and not r.get("has_audio", False))
    }