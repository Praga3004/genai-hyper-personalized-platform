import os
import json
import random
import uuid
from typing import List, Dict, Any
import base64
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import time
import threading
from openai import OpenAI
from fish_audio_sdk import Session, TTSRequest

# -------------------------------------------------
# Load environment variables
# -------------------------------------------------
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FISH_AUDIO_API_KEY = os.getenv("FISH_AUDIO_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY in .env")

if not FISH_AUDIO_API_KEY:
    raise RuntimeError("Missing FISH_AUDIO_API_KEY in .env")

# -------------------------------------------------
# Initialize API Clients
# -------------------------------------------------
client = OpenAI(api_key=OPENAI_API_KEY)
AudioFish = Session(FISH_AUDIO_API_KEY)

# Use a safe directory for audio storage

AUDIO_DIR = "/tmp/audio"
IMAGE_DIR = "/tmp/images"

os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)


def cleanup_old_files():
    now = time.time()
    max_age = 3600  # 1 hour

    folders = [AUDIO_DIR, IMAGE_DIR]

    for folder in folders:
        if not os.path.exists(folder):
            continue

        for filename in os.listdir(folder):
            path = os.path.join(folder, filename)

            try:
                if os.path.isfile(path):
                    age = now - os.path.getmtime(path)
                    if age > max_age:
                        os.remove(path)
                        print("🗑️ Deleted old file:", path)
            except Exception as e:
                print("⚠️ Cleanup error:", e)


def start_cleanup_scheduler():
    def loop():
        while True:
            cleanup_old_files()
            time.sleep(1800)  # Run every 30 minutes

    thread = threading.Thread(target=loop, daemon=True)
    thread.start()


start_cleanup_scheduler()

GEN_MODEL = "gpt-4.1-mini"

CATEGORY_DESCRIPTIONS = {
    "First-Time Voter": "Age roughly 18–22, voting for the first time...",
    "Apathetic Voter": "Low interest in politics...",
    "Swing Voter": "Not loyal to any party...",
    "Women Voter": "Focus on safety, family welfare...",
    "Senior Voter": "Age 60+, cares about pensions, healthcare...",
}

# -------------------------------------------------
# FastAPI Setup
# -------------------------------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Data Models
# -------------------------------------------------
class VoterProfileIn(BaseModel):
    id: str
    name: str
    age: int
    gender: str
    location: str
    voter_history: str
    interests: List[str]
    pain_points: List[str]


class BulkVoterRequest(BaseModel):
    voters: List[VoterProfileIn]

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
        # Simple fallback
        if v["age"] <= 22:
            return {"category": "First-Time Voter", "confidence": 0.8}
        if v["age"] >= 60:
            return {"category": "Senior Voter", "confidence": 0.8}
        if v["gender"].lower() == "female":
            return {"category": "Women Voter", "confidence": 0.7}
        return {"category": "Swing Voter", "confidence": 0.6}


@app.post("/api/classify-voter")
def classify_voter(req: BulkVoterRequest):
    results = []

    for v in req.voters:
        voter_dict = v.model_dump()
        classification = classify_with_openai(voter_dict)

        results.append({
            **voter_dict,
            "category": classification.get("category", "Unknown"),
            "confidence": round(classification.get("confidence", 0.5), 3)
        })

    return {"results": results}

# -------------------------------------------------
# Audio Fetch Endpoint (Stable)
# -------------------------------------------------
@app.get("/api/audio/{audio_id}")
def get_audio(audio_id: str):
    audio_path = os.path.join(AUDIO_DIR, f"{audio_id}.mp3")

    if not os.path.exists(audio_path):
        raise HTTPException(status_code=404, detail="Audio file not found")

    def iterfile():
        with open(audio_path, "rb") as f:
            yield from f

    return StreamingResponse(iterfile(), media_type="audio/mpeg")
@app.get("/api/image/{image_id}")
def get_image(image_id: str):
    IMAGE_DIR = "/tmp/images"
    image_path = os.path.join(IMAGE_DIR, f"{image_id}.png")

    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")

    def iterfile():
        with open(image_path, "rb") as f:
            yield from f

    return StreamingResponse(iterfile(), media_type="image/png")
CATEGORY_TEMPLATES = {
        "First-Time Voter": (
            "அன்புள்ள {name}, உங்கள் போன்ற இளைஞர்கள் தான் நம் நாட்டின் எதிர்காலம்! "
            "வேலை வாய்ப்புகள், இலவச AI பயிற்சி மற்றும் லேப்டாப் வழங்கல் போன்ற "
            "திட்டங்களால் உங்கள் வாழ்க்கையை முன்னேற்ற முடியும். "
            "{location} தொகுதியில் இளைஞர்களுக்கான வளர்ச்சி வாய்ப்புகளை உருவாக்க நாங்கள் உறுதியளிக்கிறோம். "
            "உங்கள் வாக்கு நம் புதிய மாற்றத்தின் ஆரம்பம்!"
        ),
        "Women Voter": (
            "அன்புள்ள {name}, பெண்களின் பாதுகாப்பு, குழந்தை பராமரிப்பு மையங்கள், "
            "சுய உதவி குழுக்களுக்கு நிதி உதவி, பெண்கள் கல்வி ஆகியவற்றில் "
            "நாம் அதிக கவனம் செலுத்துகிறோம். {location} தொகுதியில் பெண்களுக்கு "
            "முன்னேற்றம் அளிக்கும் திட்டங்கள் உருவாக்கப்பட்டுள்ளன. "
            "உங்கள் வாக்கு ஒரு பெண் மாறுதலின் அடையாளம்!"
        ),
        "Swing Voter": (
            "அன்புள்ள {name}, கடந்த தேர்தல்களில் நீங்கள் பல்வேறு கட்சிகளுக்கு வாக்களித்திருக்கலாம். "
            "{location} பகுதியில் நீர், சாலை, பள்ளி, கழிவுநீர் போன்ற பிரச்சனைகளை "
            "தீர்க்க நாங்கள் உறுதியளிக்கிறோம். மக்கள் நலனே நம் கொள்கை. "
            "இந்த முறை மாற்றத்தை உங்களால் தொடங்குங்கள்!"
        ),
        "Apathetic Voter": (
            "அன்புள்ள {name}, உங்கள் வாக்கு மிக முக்கியமானது. "
            "நீங்கள் அரசியலுக்கு விருப்பமில்லாமல் இருந்தாலும், "
            "நீங்கள் தேர்ந்தெடுக்கும் ஒரே வாக்கே உங்கள் வாழ்க்கை தரத்தை மாற்றும் சக்தி உடையது. "
            "{location} பகுதியில் அடிப்படை வசதிகள் மற்றும் வேலை வாய்ப்புகளை மேம்படுத்த "
            "நாங்கள் பணியாற்றி வருகிறோம். உங்கள் நம்பிக்கை நம் வலிமை!"
        ),
        "Senior Voter": (
            "அன்புள்ள {name}, உங்கள் வாழ்க்கை அனுபவம் நம் சமூகத்தின் அடித்தளம். "
            "மூத்த குடிமக்களுக்கு மாதாந்திர ஓய்வூதியம், சுகாதார பாதுகாப்பு மற்றும் "
            "சந்தை விலைகளை கட்டுப்படுத்தும் திட்டங்கள் {location} பகுதியில் விரைவில் அமலாகும். "
            "உங்கள் வாக்கு நம் தலைமுறையின் நல்வாழ்வுக்கு வழிகாட்டும்!"
        ),
    }
# -------------------------------------------------
# Campaign Generation + Audio
# -------------------------------------------------
@app.post("/api/generate-campaign")
def generate_campaign(req: BulkVoterRequest):

    

    results = []

    for voter in req.voters:
        v = voter.model_dump()
        category = v.get("category", "Swing Voter")

        base_msg = CATEGORY_TEMPLATES.get(category).format(
            name=v["name"],
            location=v["location"]
        )

        # -------------------------------------------------
        # 1️⃣ Ask OpenAI to return Tamil + English transliteration in JSON
        # -------------------------------------------------
        prompt = (
            f"Generate a Tamil political message.\n"
            f"Base message: {base_msg}\n"
            f"Pain points: {', '.join(v['pain_points'])}\n\n"
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
            print("⚠️ Error:", e)
            tamil_msg = base_msg
            english_msg = base_msg

        try:
            dalle_prompt = (
                "A vibrant, abstract illustration inspired by Tamil Nadu culture, "
        "including festive patterns, traditional textures, artistic gradients, "
        "and decorative motifs. No text, no people, no logos, no political symbols. "
                f"Theme: {category}. "
                f"Message in English letters (not Tamil script): {english_msg}. "
                f"Style: professional, sharp, high-contrast, Indian-election theme."
            )

            img_resp = client.images.generate(
                model="gpt-image-1",
                prompt=dalle_prompt,
                size="1024x1024",
                n=1,
            )

            b64 = img_resp.data[0].b64_json
            image_data = base64.b64decode(b64)

            # Save image
            image_id = str(uuid.uuid4())
            IMAGE_DIR = "/tmp/images"
            os.makedirs(IMAGE_DIR, exist_ok=True)

            image_path = os.path.join(IMAGE_DIR, f"{image_id}.png")
            with open(image_path, "wb") as f:
                f.write(image_data)

            image_url = f"/api/image/{image_id}"

        except Exception as e:
            print("⚠️ Image generation failed:", e)
            image_url = None
        audio_id = str(uuid.uuid4())
        audio_path = os.path.join(AUDIO_DIR, f"{audio_id}.mp3")

        try:
            with open(audio_path, "wb") as f:
                for chunk in AudioFish.tts(
                    TTSRequest(
                        text=english_msg,
                        reference_id="03e679752fa54b778a189c9f4e9d1889"
                    )
                ):
                    f.write(chunk)

        except Exception as e:
            print("⚠️ Audio gen failed:", e)
            audio_id = None
        print("✅ Generated campaign for:", v["name"])

        results.append({
            **v,
            "category": category,
            "base_message": base_msg,
            "final_message_tamil": tamil_msg,
            "final_message_english": english_msg,
            "audio_url": f"/api/audio/{audio_id}" if audio_id else None,
            "image_url": image_url
        })

    return {"results": results}

