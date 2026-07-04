import os
import re
from dotenv import load_dotenv

# Load env variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Gracefully import Groq client
use_groq = False
if GROQ_API_KEY:
    try:
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)
        use_groq = True
    except ImportError:
        print("[MENTOR] Groq SDK not installed. Running in offline/rule-based mode.")

# --- Fallback Static Engines ---
def fallback_diagnose_language(text: str) -> str:
    text_lower = text.lower()
    
    # Check for some common spelling errors
    english_errors = {
        "bureaucracy": "bureaucracy",
        "bureacracy": "bureaucracy",
        "receve": "receive",
        "recieve": "receive",
        "accommodate": "accommodate",
        "acomodate": "accommodate",
        "occured": "occurred",
        "occurred": "occurred",
        "seperate": "separate",
        "separate": "separate",
    }
    
    hindi_errors = {
        "कवि": "कवि",
        "कवी": "कवि",
        "आशीर्वाद": "आशीर्वाद",
        "अशीर्वाद": "आशीर्वाद",
        "उज्वल": "उज्ज्वल",
        "उज्ज्वल": "उज्ज्वल",
        "श्रीमती": "श्रीमती",
        "श्रीमति": "श्रीमती",
    }

    # Search for English matches
    found_eng = None
    for err, correct in english_errors.items():
        if err in text_lower:
            found_eng = correct
            break
            
    # Search for Hindi matches
    found_hin = None
    for err, correct in hindi_errors.items():
        if err in text:
            found_hin = correct
            break

    if found_eng:
        syllables = {
            "bureaucracy": "Bu-reau-cra-cy",
            "receive": "Re-ceive",
            "accommodate": "Ac-com-mo-date",
            "occurred": "Oc-curred",
            "separate": "Sep-a-rate"
        }.get(found_eng, found_eng)
        
        rules = (
            "1. **I before E except after C** (e.g., receive, ceiling).\n"
            "2. **Double consonants** after short vowels (e.g., occurred, accommodate).\n"
            "3. **Silent 'e' dropping** when adding suffix starting with vowel (e.g., separating).\n"
            "4. **Pluralization rules** ('y' to 'ies' when preceded by consonant)."
        )
        
        return (
            f"### 🔍 Language Lab Diagnostic\n\n"
            f"**Spelling Match Detected:** Found potential issue with English spelling.\n\n"
            f"* **Correct Word:** `{found_eng.upper()}`\n"
            f"* **Syllable Parsing:** `{syllables}`\n\n"
            f"#### 📜 Core English Spelling Rules:\n{rules}"
        )
        
    elif found_hin:
        details = {
            "कवि": "कवि (Short 'इ' sound - short pronunciation time) vs कवी (Incorrect long 'ई' pronunciation).",
            "आशीर्वाद": "आशीर्वाद (correct placement of 'र' ref on 'वा') vs अशीर्वाद (vowel shortening error).",
            "उज्ज्वल": "उज्ज्वल (double half 'ज' due to sandhi उत् + ज्वल) vs उज्वल (incorrect phonetic spelling).",
            "श्रीमती": "श्रीमती (Long 'ती' sound - long pronunciation time) vs श्रीमति (Incorrect short 'ति')."
        }.get(found_hin, found_hin)
        
        return (
            f"### 🕉️ Hindi Orthography Diagnostic (वर्तनी शुद्धि)\n\n"
            f"**Phonetic Error Detected:** Matra (मात्रा) alignment error.\n\n"
            f"* **Correct Spelling:** `{found_hin}`\n"
            f"* **Phonetic Isolation:** {details}\n\n"
            f"#### 💡 Orthography Principle:\n"
            f"Short vowel phonetics (इ, उ) require swift, low-duration vocalization. "
            f"Long vowel phonetics (ई, ऊ) require prolonged vocalization. Incorrect pronunciation directly generates spelling errors."
        )
    
    # Generic offline diagnostic
    return (
        "### 🔍 Zero-Error Language Lab (Offline)\n\n"
        "Input analyzed. No specific rule-matched errors detected in standard offline dictionary.\n\n"
        "#### 💡 Core Spelling Reminder:\n"
        "* **English:** Remember *I before E except after C* (e.g., *Receipt* vs *Believe*).\n"
        "* **Hindi:** Matra (मात्रा) placement (इ vs ई, उ vs ऊ) directly mirrors pronunciation duration."
    )

def check_academic_isolation(text: str) -> str:
    """Check if the user is mentioning undergraduate semester/college exams."""
    triggers = [
        r"\bsemester\b", r"\bsem\b", r"\bcollege exam", r"\buniversity exam",
        r"\bmidsem\b", r"\bendsem\b", r"\bcollege paper\b", r"\buniversity paper\b",
        r"\bundergrad\b", r"\bgraduation exam\b", r"सेमेस्टर", r"कॉलेज परीक्षा", r"यूनिवर्सिटी"
    ]
    for trigger in triggers:
        if re.search(trigger, text, re.IGNORECASE):
            return (
                "### 🚨 ACADEMIC BANK ISOLATION PROTOCOL ACTIVATED\n\n"
                "**DIRECTIVE:** Impending undergraduate university/college semester examinations detected.\n\n"
                "You are commanded to **HALT** all competitive exam routines (UPSC, CGL, CDS, SI) immediately "
                "**10 to 15 days prior** to your college exam start date.\n\n"
                "👉 **Priority Priority:** Secure your university degree with high marks first. "
                "The competitive grid will remain locked for you until your semester papers are cleared. "
                "Resume your competitive preparation only after your college exams conclude. Focus entirely on college modules now."
            )
    return ""

def check_ambiguity(text: str) -> str:
    """If the input is too brief or ambiguous, return 3 clear choices to narrow it down."""
    text_clean = text.strip()
    if len(text_clean) < 8 or text_clean.lower() in ["hi", "hello", "doubt", "help", "study", "exam", "upsc", "ssc"]:
        return (
            "### ⚙️ Context Preservation Protocol\n\n"
            "Your query is too ambiguous. To provide clinical, data-driven mentorship, please select one of the following concrete pathways:\n\n"
            "1. **Core GS Mentorship:** Submit a specific topic doubt (e.g., 'Explain Laxmikanth's Article 21' or 'Mrunal's view on Repo Rate').\n"
            "2. **Productivity Design:** Specify your scheduling constraint (e.g., 'Design an 8-hour schedule using Eat the Frog').\n"
            "3. **Career Asset Compilation:** Type `/makeresume` to begin your 6-stage ATS Resume build."
        )
    return ""

# --- Groq Integration ---
def get_groq_response(system_prompt: str, user_prompt: str) -> str:
    """Query Groq API with Llama-3-8b model."""
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=1024
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"*(Groq API Error: {str(e)}. Falling back to local offline logic.)*\n\n"

# --- Main Exposed Services ---
def diagnose_language(text: str) -> str:
    """Zero-Error Language Correction Lab."""
    if not use_groq:
        return fallback_diagnose_language(text)
        
    system_prompt = (
        "You are the 'Zero-Error Language Correction Lab' module of AstraAI Hub. "
        "Analyze the user's input text for English spellings or Hindi writing (वर्तनी) correctness. "
        "Strictly adhere to these guidelines:\n"
        "1. Identify spelling errors.\n"
        "2. If English spelling is wrong, use the 'Syllable Parsing Technique' (e.g. break Bureaucracy into Bu-reau-cra-cy) "
        "and supply the 4 core linguistic spelling rules (like 'I before E except after C').\n"
        "3. If Hindi spelling (वर्तनी) is wrong, diagnose Matra (मात्रा) placement errors by isolating short vowel vs. long vowel "
        "phonetics (इ vs. ई, उ vs. ऊ), and explain how incorrect pronunciation causes it.\n"
        "4. Tone: authoritative, clinical, professional, zero fluff.\n"
        "5. Output formatting: Use bold headers (###), bullet points, and code blocks for words. No conversational chatter."
    )
    
    return get_groq_response(system_prompt, text)

def solve_academic_doubt(text: str) -> str:
    """Mentorship doubt-clearing engine."""
    # 1. Enforce Academic Bank Isolation Rule first
    isolation_msg = check_academic_isolation(text)
    if isolation_msg:
        return isolation_msg
        
    # 2. Enforce Context Preservation for brief/ambiguous inputs
    ambiguity_msg = check_ambiguity(text)
    if ambiguity_msg:
        return ambiguity_msg
        
    if not use_groq:
        # Static mock doubt solver
        return (
            f"### 📚 Mentorship Board (Offline Mode)\n\n"
            f"Your query: *\"{text}\"*\n\n"
            f"**Academic Guidance:**\n"
            f"- For Indian Polity: Reference M. Laxmikanth's latest edition chapters on Fundamental Rights and Parliament.\n"
            f"- For Macroeconomics: Anchor concepts in Mrunal's Pillar 1 (Banking, Monetary Policy, Repo Rate).\n"
            f"- For History: Check Spectrum's chronological tables for Modern India.\n\n"
            f"*(Connect to the Groq API by adding GROQ_API_KEY in .env to enable AI doubt-solving.)*"
        )
        
    system_prompt = (
        "You are AstraAI Hub, an elite enterprise-grade academic mentor for competitive exams (UPSC, SSC CGL, CDS).\n"
        "Your tone: highly authoritative, ultra-professional, encouraging yet disciplined. Eliminate conversational fillers.\n"
        "Use scannable mobile-first formatting: bolding, clear hierarchy (###), bullet points, and code snippets.\n"
        "Answer doubts across General Studies (Polity, History, Geography, Economy, Science), Quant, and English Comprehension.\n"
        "Reference expert materials (Laxmikanth, Mrunal, Spectrum, NCERT) where appropriate.\n"
        "Keep answers concise (under 250 words) and high-yield. Do not make apologies."
    )
    
    return get_groq_response(system_prompt, text)
