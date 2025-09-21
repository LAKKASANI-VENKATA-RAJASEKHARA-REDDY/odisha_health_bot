from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
from langdetect import detect
from googletrans import Translator
from config import GEMINI_API_KEY, GEMINI_API_URL

app = Flask(__name__)
translator = Translator()

# ---------- Embedded "Database" ----------

vaccines = [
    {"name": "BCG", "age_group": "Newborn", "schedule": "At birth", "notes": "Protects against tuberculosis"},
    {"name": "OPV", "age_group": "0-5 years", "schedule": "Birth, 6, 10, 14 weeks", "notes": "Polio vaccine"},
    {"name": "DPT", "age_group": "0-5 years", "schedule": "6, 10, 14 weeks", "notes": "Diphtheria, Pertussis, Tetanus"}
]

diseases = [
    {"name": "Dengue", "symptoms": "Fever, headache, joint pain, rash", "prevention": "Avoid mosquito bites, remove stagnant water"},
    {"name": "Malaria", "symptoms": "Fever, chills, sweating", "prevention": "Use mosquito nets, anti-malarial prophylaxis"},
    {"name": "Diabetes", "symptoms": "Frequent urination, excessive thirst, fatigue", "prevention": "Balanced diet, exercise, medication"}
]

hospitals = [
    {"name": "SCB Medical College", "district": "Cuttack", "block": "Cuttack Sadar", "contact": "0671-2301234", "specialty": "General, Emergency"},
    {"name": "MKCG Medical College", "district": "Berhampur", "block": "Berhampur Sadar", "contact": "0680-2221234", "specialty": "General, Pediatrics"},
    {"name": "District Hospital Bhubaneswar", "district": "Khordha", "block": "Bhubaneswar Sadar", "contact": "0674-2551234", "specialty": "General, Maternity"}
]

outbreaks = [
    {"disease": "Dengue", "district": "Cuttack", "start_date": "2025-06-01", "end_date": "2025-06-15", "severity": "Medium"},
    {"disease": "Malaria", "district": "Bhubaneswar", "start_date": "2025-07-10", "end_date": "2025-07-25", "severity": "High"}
]

health_programs = [
    {"name": "National Immunization Program", "description": "Free vaccination for children and pregnant women", "start_date": "2025-01-01", "end_date": "2025-12-31"},
    {"name": "Ayushman Bharat", "description": "Health insurance and preventive care for underprivileged", "start_date": "2025-01-01", "end_date": "2025-12-31"}
]

# ---------- Helper Functions ----------

def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"

def translate_to_english(text):
    lang = detect_language(text)
    if lang != "en":
        return translator.translate(text, src=lang, dest='en').text
    return text

def translate_to_user_lang(text, user_lang):
    if user_lang != "en":
        return translator.translate(text, src='en', dest=user_lang).text
    return text

def build_gemini_prompt(user_query):
    context = f"Vaccines: {vaccines}\nDiseases: {diseases}\nHospitals: {hospitals}\nOutbreaks: {outbreaks}\nHealth Programs: {health_programs}"
    prompt = f"""
You are an AI healthcare assistant for Odisha, India. Use the following data to answer queries accurately:
{context}

User question: {user_query}

Answer clearly, concisely, and accurately.
"""
    return prompt

def call_gemini(prompt):
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gemini-1.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }
    response = requests.post(GEMINI_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    return "Sorry, I am unable to process your request at the moment."

# ---------- Flask Route ----------

@app.route("/whatsapp", methods=['POST'])
def whatsapp_bot():
    incoming_msg = request.values.get('Body', '').strip()
    user_lang = detect_language(incoming_msg)
    english_query = translate_to_english(incoming_msg)

    prompt = build_gemini_prompt(english_query)
    response_text = call_gemini(prompt)
    response_text_translated = translate_to_user_lang(response_text, user_lang)

    resp = MessagingResponse()
    resp.message(response_text_translated)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
