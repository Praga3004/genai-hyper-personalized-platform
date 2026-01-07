# prompt.py
# Personalized message templates based on voter_category and issue_category combinations
# These prompts are used to generate targeted political campaign messages

PROMPT_TEMPLATES = {
    # Youth / First-time Voter + Health, Education & Social Infrastructure
    ("Youth / First-time Voter", "Health, Education & Social Infrastructure"): (
        "அன்புள்ள {name}, உங்கள் போன்ற இளைஞர்கள் நம் நாட்டின் எதிர்காலம்! "
        "{location} பகுதியில் கல்வி மற்றும் சுகாதார வசதிகளை மேம்படுத்த நாங்கள் உறுதியளிக்கிறோம். "
        "{issue_description} - இந்த பிரச்சனையை நாங்கள் உடனடியாக சமாளிக்க உறுதியளிக்கிறோம். "
        "இளைஞர்களுக்கான சிறந்த கல்வி வசதிகள், மருத்துவமனைகள் மற்றும் சமூக உள்கட்டமைப்பை "
        "வழங்குவதே எங்கள் முதன்மையான குறிக்கோள். உங்கள் வாக்கு ஒரு மாற்றத்தை உருவாக்கும்!"
    ),
    
    # Youth / First-time Voter + Employment, Skills & Digital Access
    ("Youth / First-time Voter", "Employment, Skills & Digital Access"): (
        "அன்புள்ள {name}, உங்கள் கனவுகளை நனவாக்க நாங்கள் இங்கே இருக்கிறோம்! "
        "{location} பகுதியில் இளைஞர்களுக்கான வேலை வாய்ப்புகள், AI மற்றும் டிஜிட்டல் திறன்கள் "
        "பயிற்சி, மற்றும் இலவச லேப்டாப் வழங்கல் போன்ற திட்டங்களை நாங்கள் தொடங்கியுள்ளோம். "
        "{issue_description} - இந்த பிரச்சனையை தீர்க்க நாங்கள் உறுதியாக இருக்கிறோம். "
        "உங்கள் திறமைகளை வளர்த்து, வேலை வாய்ப்புகளை பெற உங்களுக்கு தேவையான எல்லா உதவிகளையும் "
        "வழங்குவோம். உங்கள் வாக்கு நம் புதிய மாற்றத்தின் ஆரம்பம்!"
    ),
    
    # Working Professional + Transportation, Traffic & Connectivity
    ("Working Professional", "Transportation, Traffic & Connectivity"): (
        "அன்புள்ள {name}, உங்களின் அன்றாட பயணம் எளிதாக இருக்க வேண்டும் என்பது எங்கள் நோக்கம். "
        "{location} பகுதியில் போக்குவரத்து மற்றும் இணைப்பு வசதிகளை மேம்படுத்த நாங்கள் உறுதியளிக்கிறோம். "
        "{issue_description} - இந்த பிரச்சனையை நாங்கள் தீர்க்க உறுதியாக இருக்கிறோம். "
        "சாலைகளை விரிவுபடுத்துதல், கடைசி மைல் இணைப்பு வசதிகள், மற்றும் போக்குவரத்து நெரிசலை "
        "குறைத்தல் போன்ற திட்டங்களை விரைவில் அமலாக்குவோம். உங்கள் வாக்கு நம் வளர்ச்சியின் அடையாளம்!"
    ),
    
    # Working Professional + Power & Urban Infrastructure
    ("Working Professional", "Power & Urban Infrastructure"): (
        "அன்புள்ள {name}, நீங்கள் வாழும் {location} பகுதியில் மின்சாரம் மற்றும் நகர்ப்புற "
        "உள்கட்டமைப்பை மேம்படுத்த நாங்கள் உறுதியளிக்கிறோம். "
        "{issue_description} - இந்த பிரச்சனையை தீர்க்க நாங்கள் நடவடிக்கை எடுக்கிறோம். "
        "வழக்கமான மின்சார வழங்கல், EV சார்ஜிங் வசதிகள், மற்றும் நவீன நகர்ப்புற "
        "உள்கட்டமைப்பை உருவாக்குவோம். உங்கள் வாக்கு ஒரு வளர்ந்த வரவேற்புக்கான உறுதிமொழி!"
    ),
    
    # Working Professional + Housing, Rentals & Urban Cost of Living
    ("Working Professional", "Housing, Rentals & Urban Cost of Living"): (
        "அன்புள்ள {name}, வசதியான வாழ்விடம் உங்களின் அடிப்படை உரிமை. "
        "{location} பகுதியில் வாடகை மற்றும் வீட்டு விலைகளை கட்டுப்படுத்த நாங்கள் உறுதியளிக்கிறோம். "
        "{issue_description} - இந்த பிரச்சனையை நாங்கள் சமாளிக்கிறோம். "
        "மலிவான வாழ்விட திட்டங்கள், வாடகை கட்டுப்பாடுகள், மற்றும் வாழ்க்கை செலவை "
        "குறைக்கும் நடவடிக்கைகளை எடுப்போம். உங்கள் வாக்கு ஒரு சிறந்த வாழ்க்கைக்கான முதல் படி!"
    ),
    
    # Women + Road, Pedestrian & Public Safety
    ("Women", "Road, Pedestrian & Public Safety"): (
        "அன்புள்ள {name}, பெண்களின் பாதுகாப்பு எங்களின் முதன்மையான முன்னுரிமை. "
        "{location} பகுதியில் சாலை, நடைபாதை மற்றும் பொதுப் பாதுகாப்பு வசதிகளை "
        "மேம்படுத்த நாங்கள் உறுதியளிக்கிறோம். "
        "{issue_description} - இந்த பிரச்சனையை நாங்கள் உடனடியாக தீர்க்கிறோம். "
        "CCTV கேமராக்கள், பதற்ற பொத்தான்கள், சரியான தெரு விளக்குகள், மற்றும் "
        "பாதுகாப்பான சாலை வசதிகளை உருவாக்குவோம். உங்கள் வாக்கு ஒரு பாதுகாப்பான எதிர்காலத்திற்கான வாக்குறுதி!"
    ),
    
    # Women + Health, Education & Social Infrastructure
    ("Women", "Health, Education & Social Infrastructure"): (
        "அன்புள்ள {name}, பெண்களின் சுகாதாரம், கல்வி மற்றும் சமூக வளர்ச்சி "
        "எங்களின் முக்கிய குறிக்கோள். "
        "{location} பகுதியில் பெண்களுக்கான சுகாதார மையங்கள், கல்வி வசதிகள் "
        "மற்றும் சமூக உள்கட்டமைப்பை வழங்க நாங்கள் உறுதியளிக்கிறோம். "
        "{issue_description} - இந்த பிரச்சனையை நாங்கள் தீர்க்கிறோம். "
        "முதன்மை சுகாதார மையங்கள், குழந்தை பராமரிப்பு மையங்கள், மற்றும் கல்வி "
        "வாய்ப்புகளை மேம்படுத்துவோம். உங்கள் வாக்கு ஒரு பெண் மாறுதலின் அடையாளம்!"
    ),
    
    # Senior Citizens + Water Supply & Groundwater
    ("Senior Citizens", "Water Supply & Groundwater"): (
        "அன்புள்ள {name}, உங்களின் வாழ்க்கை அனுபவம் நம் சமூகத்தின் அடித்தளம். "
        "{location} பகுதியில் நீர் வழங்கல் மற்றும் நிலத்தடி நீர் பாதுகாப்பை "
        "உறுதிப்படுத்த நாங்கள் உறுதியளிக்கிறோம். "
        "{issue_description} - இந்த பிரச்சனையை நாங்கள் சமாளிக்கிறோம். "
        "தொடர்ச்சியான நீர் வழங்கல், நிலத்தடி நீர் மறுசுழற்சி திட்டங்கள், மற்றும் "
        "நீர் விவகாரங்களை தீர்க்கும் நடவடிக்கைகளை எடுப்போம். உங்கள் வாக்கு நம் தலைமுறையின் நல்வாழ்வுக்கு வழிகாட்டும்!"
    ),
    
    # Senior Citizens + Health, Education & Social Infrastructure
    ("Senior Citizens", "Health, Education & Social Infrastructure"): (
        "அன்புள்ள {name}, மூத்த குடிமக்களின் நல்வாழ்வு எங்களின் முதன்மையான பொறுப்பு. "
        "{location} பகுதியில் சுகாதாரம், கல்வி மற்றும் சமூக உள்கட்டமைப்பை "
        "மேம்படுத்த நாங்கள் உறுதியளிக்கிறோம். "
        "{issue_description} - இந்த பிரச்சனையை நாங்கள் தீர்க்கிறோம். "
        "மாதாந்திர ஓய்வூதியம், மருத்துவ வசதிகள், மற்றும் மூத்த குடிமக்களுக்கான "
        "சிறப்பு திட்டங்களை வழங்குவோம். உங்கள் வாக்கு நம் குடும்பத்தின் கண்ணியத்தை காட்டும்!"
    ),
    
    # Daily Wage / Service Worker + Transportation, Traffic & Connectivity
    ("Daily Wage / Service Worker", "Transportation, Traffic & Connectivity"): (
        "அன்புள்ள {name}, உங்களின் பணியை எளிதாக்குவதே எங்களின் நோக்கம். "
        "{location} பகுதியில் போக்குவரத்து மற்றும் இணைப்பு வசதிகளை "
        "மேம்படுத்த நாங்கள் உறுதியளிக்கிறோம். "
        "{issue_description} - இந்த பிரச்சனையை நாங்கள் தீர்க்கிறோம். "
        "மலிவான போக்குவரத்து வசதிகள், சாலை மேம்பாடுகள், மற்றும் பணிக்கு "
        "எளிதான அணுகலை வழங்குவோம். உங்கள் வாக்கு ஒரு சிறந்த வாழ்க்கைக்கான முயற்சி!"
    ),
    
    # Daily Wage / Service Worker + Housing, Rentals & Urban Cost of Living
    ("Daily Wage / Service Worker", "Housing, Rentals & Urban Cost of Living"): (
        "அன்புள்ள {name}, வசதியான வாழ்விடம் உங்களின் அடிப்படை உரிமை. "
        "{location} பகுதியில் மலிவான வாடகை வீடுகள் மற்றும் வாழ்க்கை "
        "செலவுகளை குறைக்க நாங்கள் உறுதியளிக்கிறோம். "
        "{issue_description} - இந்த பிரச்சனையை நாங்கள் சமாளிக்கிறோம். "
        "மலிவான வாழ்விட திட்டங்கள், வாடகை கட்டுப்பாடுகள், மற்றும் "
        "வாழ்க்கை செலவை குறைக்கும் நடவடிக்கைகளை எடுப்போம். உங்கள் வாக்கு ஒரு நியாயமான வாழ்க்கைக்கான உறுதிமொழி!"
    ),
}


def get_prompt_template(voter_category: str, issue_category: str) -> str:
    """
    Get the appropriate prompt template based on voter_category and issue_category.
    Returns a default template if the combination is not found.
    """
    key = (voter_category, issue_category)
    template = PROMPT_TEMPLATES.get(key)
    
    if not template:
        # Return a generic template if combination not found
        return (
            f"அன்புள்ள {{name}}, {voter_category} பிரிவைச் சேர்ந்த உங்களுக்கு "
            f"{issue_category} பிரச்சனையை தீர்க்க நாங்கள் உறுதியளிக்கிறோம். "
            f"{{location}} பகுதியில் இந்த விஷயத்தில் முன்னேற்றத்தைக் கொண்டு வருவோம். "
            f"{{issue_description}} - இந்த பிரச்சனையை நாங்கள் சமாளிக்கிறோம். "
            f"உங்கள் வாக்கு ஒரு மாற்றத்தை உருவாக்கும்!"
        )
    
    return template


def format_prompt(template: str, name: str, location: str, issue_description: str) -> str:
    """
    Format a prompt template with the given parameters.
    """
    return template.format(
        name=name,
        location=location,
        issue_description=issue_description
    )

