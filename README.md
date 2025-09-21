# Odisha Healthcare WhatsApp AI Bot

## Overview
A WhatsApp chatbot for Odisha healthcare queries. Supports Odia, Hindi, English.
Provides info on vaccines, diseases, hospitals, outbreaks, and government programs.

## Setup

1. **Twilio Sandbox**
   - Get Twilio sandbox WhatsApp number.
   - Copy `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_WHATSAPP_NUMBER` into `config.py`.
   - Set webhook to `/whatsapp` on Render.

2. **Gemini API**
   - Replace `GEMINI_API_KEY` in `config.py` with your key.

3. **Deployment on Render**
   - Push this repo to GitHub.
   - Create a **Python Web Service**.
   - Set build command: `pip install -r backend/requirements.txt`
   - Start command: `python backend/app.py`
   - Environment variables for Twilio/Gemini can be set in Render dashboard.

4. **Testing**
   - Send WhatsApp messages to your Twilio sandbox number.
   - Bot replies in the same language as the input (Odia/Hindi/English).
