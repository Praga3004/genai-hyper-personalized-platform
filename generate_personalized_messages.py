"""
Script to generate personalized messages for voters 00 on their data from Supabase
Usage: Provide 5 voter IDs or names when prompted
"""

import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from supabase import create_client, Client

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY in .env file")

if not SUPABASE_URL:
    raise RuntimeError("Missing SUPABASE_URL in .env file")

if not SUPABASE_KEY:
    raise RuntimeError("Missing SUPABASE_KEY in .env file")

client = OpenAI(api_key=OPENAI_API_KEY)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
GEN_MODEL = "gpt-4o-mini"  # or "gpt-4.1-mini" depending on what's available

# Category templates for message generation
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


def map_voter_category_to_message_category(voter_category, age, gender):
    """Map CSV voter_category to message category"""
    if age <= 21:
        return "First-Time Voter"
    if age >= 60:
        return "Senior Voter"
    if gender and str(gender).strip().lower() == "female":
        return "Women Voter"
    # Default to Swing Voter for Working Professional, Daily Wage, etc.
    return "Swing Voter"


def get_location_string(voter_data):
    """Construct location string from voter data"""
    location_parts = []
    village = voter_data.get('village')
    area = voter_data.get('area')
    ward = voter_data.get('ward')
    
    if village and str(village).strip():
        location_parts.append(str(village).strip())
    elif area and str(area).strip():
        location_parts.append(str(area).strip())
    if ward and str(ward).strip():
        location_parts.append(f"வார்ட் {str(ward).strip()}")
    
    return ", ".join(location_parts) if location_parts else "உங்கள் பகுதி"


def generate_personalized_message(voter_data):
    """Generate personalized message for a voter using OpenAI"""
    name = str(voter_data.get('voter_name', '')).strip()
    age = voter_data.get('age', 0)
    gender = voter_data.get('gender', '')
    voter_category = str(voter_data.get('voter_category', '')).strip()
    issue_category = str(voter_data.get('issue_category', '')).strip()
    issue_description = str(voter_data.get('issue_description', '')).strip()
    
    # Map to message category
    message_category = map_voter_category_to_message_category(
        voter_category, age, gender
    )
    
    # Get location
    location = get_location_string(voter_data)
    
    # Get base template
    base_template = CATEGORY_TEMPLATES.get(message_category, CATEGORY_TEMPLATES["Swing Voter"])
    base_msg = base_template.format(name=name, location=location)
    
    # Create pain points from issue
    pain_points = []
    if issue_category:
        pain_points.append(issue_category)
    if issue_description:
        pain_points.append(issue_description)
    
    # Generate enhanced message with OpenAI
    prompt = (
        f"Generate a Tamil political message.\n"
        f"Base message: {base_msg}\n"
        f"Specific issue category: {issue_category}\n"
        f"Specific issue: {issue_description}\n"
        f"Voter category: {voter_category}\n\n"
        f"Create a personalized message that addresses their specific concern ({issue_description}) "
        f"while maintaining the base message tone. The message should be natural, empathetic, and "
        f"focused on their specific issue.\n\n"
        f"Respond ONLY in valid JSON format:\n"
        f"{{\n"
        f"  \"content_tamil\": \"string (Tamil message)\",\n"
        f"  \"content_english\": \"string (same Tamil text spelled using English letters with proper punctuation)\"\n"
        f"}}"
    )
    
    try:
        resp = client.chat.completions.create(
            model=GEN_MODEL,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a Tamil political message expert. Generate authentic, empathetic messages in Tamil."},
                {"role": "user", "content": prompt},
            ],
        )
        
        data = json.loads(resp.choices[0].message.content)
        tamil_msg = data.get("content_tamil", base_msg)
        english_msg = data.get("content_english", base_msg)
        
        return {
            "tamil": tamil_msg,
            "english": english_msg,
            "category": message_category,
            "issue": issue_description
        }
    except Exception as e:
        print(f"⚠️ Error generating message with OpenAI: {e}")
        return {
            "tamil": base_msg,
            "english": base_msg,
            "category": message_category,
            "issue": issue_description
        }


def find_voter_by_id_or_name(identifier):
    """Find voter by ID or name from Supabase"""
    identifier = str(identifier).strip()
    
    try:
        # Try exact match on voter_id
        response = supabase.table("voters_master").select("*").eq("voter_id", identifier).execute()
        if response.data:
            return response.data[0]
        
        # Try partial match on voter_name (case-insensitive search)
        response = supabase.table("voters_master").select("*").ilike("voter_name", f"%{identifier}%").limit(1).execute()
        if response.data:
            return response.data[0]
        
        return None
    except Exception as e:
        print(f"Error searching for voter: {e}")
        return None


def main():
    """Main function to generate messages for 5 contacts"""
    print("=" * 60)
    print("Personalized Message Generator for Voters")
    print("=" * 60)
    print("\nConnected to Supabase database...")
    
    # Get 5 contacts from user
    print("Please provide 5 voter identifiers (voter_id or name):")
    print("(You can enter them one by one, or all at once separated by commas)\n")
    
    contacts = []
    while len(contacts) < 5:
        identifier = input(f"Contact {len(contacts) + 1}/5: ").strip()
        if not identifier:
            print("⚠️ Please enter a valid identifier")
            continue
        
        # Handle comma-separated input
        identifiers = [id.strip() for id in identifier.split(',')]
        for ident in identifiers:
            if len(contacts) >= 5:
                break
            if ident:
                contacts.append(ident)
    
    print("\n" + "=" * 60)
    print("Generating personalized messages...")
    print("=" * 60 + "\n")
    
    results = []
    for i, contact_id in enumerate(contacts[:5], 1):
        print(f"Processing contact {i}/5: {contact_id}...")
        voter = find_voter_by_id_or_name(contact_id)
        
        if voter is None:
            print(f"  ❌ Voter not found: {contact_id}\n")
            results.append({
                "identifier": contact_id,
                "error": "Voter not found"
            })
            continue
        
        message_data = generate_personalized_message(voter)
        
        results.append({
            "identifier": contact_id,
            "voter_name": voter.get('voter_name', ''),
            "voter_id": voter.get('voter_id', ''),
            "age": voter.get('age', ''),
            "gender": voter.get('gender', ''),
            "location": get_location_string(voter),
            "issue_category": voter.get('issue_category', ''),
            "issue_description": voter.get('issue_description', ''),
            "message_category": message_data['category'],
            "tamil_message": message_data['tamil'],
            "english_message": message_data['english']
        })
        
        print(f"  ✓ Generated message for {voter.get('voter_name', 'Unknown')}\n")
    
    # Display results
    print("\n" + "=" * 60)
    print("GENERATED PERSONALIZED MESSAGES")
    print("=" * 60 + "\n")
    
    for i, result in enumerate(results, 1):
        if "error" in result:
            print(f"\n[Contact {i}] {result['identifier']}")
            print(f"Error: {result['error']}\n")
            continue
        
        print(f"\n{'='*60}")
        print(f"[Contact {i}] {result['voter_name']} (ID: {result['voter_id']})")
        print(f"{'='*60}")
        print(f"Age: {result['age']} | Gender: {result['gender']}")
        print(f"Location: {result['location']}")
        print(f"Issue: {result['issue_description']}")
        print(f"Category: {result['message_category']}")
        print(f"\n--- Tamil Message ---")
        print(result['tamil_message'])
        print(f"\n--- English Transliteration ---")
        print(result['english_message'])
        print()
    
    # Save to file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, "personalized_messages_output.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Results saved to {output_file}")
    print("\nDone!")


if __name__ == "__main__":
    main()

