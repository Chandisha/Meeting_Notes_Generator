RENA: Meeting Intelligence System

RENA (Responsive Enterprise Note Assistant) is an advanced AI-powered meeting intelligence system that converts raw meeting audio into structured, actionable insights.

Developed by: Chandisha Das

KEY FEATURES
• High-fidelity transcription using faster-whisper
• Hybrid AI engine with Google Gemini (cloud) and Ollama (local fallback)
• Automatic action item extraction
• Bilingual summaries (English & Hindi)
• Professional PDF report generation

TECH STACK
Python 3.9+, Streamlit, faster-whisper, Google Gemini, Ollama, reportlab

INSTALLATION
1. Install Python 3.9+
2. Install FFmpeg
3. Clone repository
4. Create virtual environment
5. Install dependencies

USAGE
Run UI:
streamlit run app.py

Run CLI:
python meeting_notes_generator.py "audio.wav"

PROJECT STRUCTURE
fonts/
meeting_outputs/
meeting_notes_generator.py
app.py
requirements.txt

CONFIGURATION
Add Gemini API key in meeting_notes_generator.py

FUTURE ROADMAP
Real-time transcription
Speaker diarization
Calendar integration
Cloud deployment

Author: Chandisha Das

