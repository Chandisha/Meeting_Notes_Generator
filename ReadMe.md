# 🎙️ RENA: Meeting Intelligence System

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)
[![Ollama](https://img.shields.io/badge/Local%20AI-Ollama-black?logo=ollama&logoColor=white)](https://ollama.com/)

**RENA (Responsive Enterprise Note Assistant)** is an advanced AI-powered tool designed to transform raw meeting audio into structured, actionable intelligence. It automates the role of a meeting secretary by transcribing audio, summarizing discussions in multiple languages, extracting action items, and generating professional PDF reports.

This system features a robust **Hybrid AI Architecture**: it prioritizes cloud-based processing for speed but intelligently switches to local models if internet connectivity fails, ensuring 100% reliability.

**Developed by:** Chandisha Das

---

## 🚀 Key Features

* **🎧 High-Fidelity Transcription:** Uses `faster-whisper` for accurate, offline speech-to-text conversion with Voice Activity Detection (VAD).
* **🧠 Hybrid AI Engine:**
    * **Primary (Cloud):** Leverages **Google Gemini** for high-speed, sophisticated reasoning and summarization.
    * **Fallback (Local):** Automatically switches to **Ollama (local LLM)** if internet/cloud services are unavailable, ensuring data privacy.
* **📊 Action Plan Extraction:** Intelligent parsing of conversation to identify specific Tasks, Owners, and Deadlines.
* **🌐 Bilingual Support:** Generates Executive Summaries in both **English** and **Hindi** (Devanagari script supported in PDF).
* **📄 Professional PDF Reports:** Auto-generates clean, formatted PDF reports including Minutes of Meeting (MOM), Action Tables, and Full Transcripts.

---

## 🛠️ Tech Stack

* **Language:** Python 3.9+
* **UI Framework:** Streamlit (for Web Interface)
* **AI & Machine Learning:**
    * **ASR (Audio):** `faster-whisper` (OpenAI Whisper implementation)
    * **LLM (Cloud):** Google GenAI (`google-genai` SDK)
    * **LLM (Local):** Ollama (`ollama` Python library)
* **Report Generation:** `reportlab` (PDF creation engine)
* **Utilities:** `loguru` (Logging), `pathlib`

---

## ⚙️ Installation & Setup

### 1. Prerequisites
Ensure you have Python installed. You will also need **FFmpeg** installed on your system for audio processing.
* **Windows:** [Download FFmpeg](https://ffmpeg.org/download.html) and add it to your system PATH.
* **Mac:** `brew install ffmpeg`
* **Linux:** `sudo apt install ffmpeg`

### 2. Clone the Repository

git clone [https://github.com/Chandisha/RENA-Meeting-Intelligence-System.git](https://github.com/Chandisha/RENA-Meeting-Intelligence-System.git)
cd RENA-Meeting-Intelligence-System
3. Create a Virtual Environment (Recommended)
Bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
4. Install Dependencies
Bash
pip install -r requirements.txt
(Note: Ensure your requirements.txt includes: faster-whisper, google-genai, ollama, reportlab, loguru, streamlit)

5. Setup Local AI (Optional)
If you wish to use the Local AI fallback feature:

Download and install Ollama.

Pull the recommended model:

Bash
ollama pull qwen2.5:32b
🏃‍♂️ Usage
Option A: Running the UI (Streamlit)
To launch the interactive web interface:

Bash
streamlit run app.py
(Upload your audio file, click "Generate Report", and download the resulting PDF)

Option B: Running the Script (CLI)
You can run the generator directly on an audio file without the UI:

Bash
python meeting_notes_generator.py "path/to/your/audio_file.wav"
📂 Project Structure
RENA-Meeting-Intelligence-System/
├── fonts/                       # Folder containing fonts (e.g., NotoSansDevanagari)
│   └── NotoSansDevanagari-Regular.ttf
├── meeting_outputs/             # Generated PDF reports are saved here
├── meeting_notes_generator.py   # Core logic class (Transcription + AI Pipeline)
├── app.py                       # Streamlit UI entry point
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
🔑 Configuration
Google Gemini API Key: Open meeting_notes_generator.py and replace the placeholder API key:

Python
GEMINI_API_KEY = "YOUR_OWN_GOOGLE_API_KEY"
Tip: For production, it is recommended to use Environment Variables or Streamlit Secrets.

Hindi Font Support: Ensure NotoSansDevanagari-Regular.ttf is placed inside the fonts/ directory to enable Hindi text rendering in PDFs.

🔮 Future Roadmap
Real-time Transcription: Integration for live meeting support.

Speaker Diarization: Advanced identification of "Who said what".

Calendar Integration: Auto-schedule follow-up meetings based on Action Plans.

Cloud Deployment: Docker support for AWS/GCP deployment.

👤 Author
Chandisha Das
