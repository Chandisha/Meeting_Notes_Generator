# 🎙️ RENA: Meeting Intelligence System

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)
[![Ollama](https://img.shields.io/badge/Local%20AI-Ollama-black?logo=ollama&logoColor=white)](https://ollama.com/)

**RENA (Responsive Enterprise Note Assistant)** is an advanced AI-powered meeting intelligence system that converts raw meeting audio into structured, actionable insights. It automates the role of a meeting secretary by transcribing audio, generating multilingual summaries, extracting action items, and producing professional PDF reports.

The system is built on a **Hybrid AI Architecture** — prioritizing fast cloud-based inference while seamlessly falling back to local LLMs when internet connectivity is unavailable, ensuring **100% reliability and privacy**.

**Developed by:** Chandisha Das

---

## 🚀 Key Features

- 🎧 **High-Fidelity Transcription**  
  Accurate offline speech-to-text conversion using `faster-whisper` with Voice Activity Detection (VAD).

- 🧠 **Hybrid AI Engine**
  - **Primary (Cloud):** Google Gemini for fast, high-quality reasoning and summarization.
  - **Fallback (Local):** Ollama-powered local LLM for offline and privacy-preserving inference.

- 📊 **Action Plan Extraction**  
  Automatically identifies Tasks, Owners, and Deadlines from meeting conversations.

- 🌐 **Bilingual Executive Summaries**  
  Generates summaries in **English** and **Hindi**, with full Devanagari script support in PDFs.

- 📄 **Professional PDF Reports**  
  Auto-generated reports containing Minutes of Meeting (MoM), Action Item Tables, Executive Summaries, and Full Transcripts.

---

## 🛠️ Tech Stack

- **Programming Language:** Python 3.9+
- **UI Framework:** Streamlit
- **AI & Machine Learning**
  - Speech-to-Text: `faster-whisper`
  - Cloud LLM: Google Gemini (`google-genai`)
  - Local LLM: Ollama
- **Report Generation:** `reportlab`
- **Utilities:** `loguru`, `pathlib`

---

## ⚙️ Installation & Setup

### 1️⃣ Prerequisites

- Python 3.9 or higher
- **FFmpeg** (required for audio processing)

**Install FFmpeg**
- **Windows:** Download from https://ffmpeg.org/download.html and add to PATH
- **macOS:** `brew install ffmpeg`
- **Linux:** `sudo apt install ffmpeg`

---

### 2️⃣ Clone the Repository

git clone https://github.com/Chandisha/RENA-Meeting-Intelligence-System.git  
cd RENA-Meeting-Intelligence-System

---

### 3️⃣ Create a Virtual Environment (Recommended)

python -m venv venv  

Windows:  
venv\Scripts\activate  

macOS / Linux:  
source venv/bin/activate

---

### 4️⃣ Install Dependencies

pip install -r requirements.txt  

Ensure `requirements.txt` includes:  
faster-whisper, google-genai, ollama, reportlab, loguru, streamlit

---

### 5️⃣ Setup Local AI (Optional – Offline Mode)

Install Ollama from https://ollama.com  

Pull the recommended model:  
ollama pull qwen2.5:32b

---

## 🏃‍♂️ Usage

### Option A: Run Web UI (Streamlit)

streamlit run app.py  

Upload an audio file, click **Generate Report**, and download the PDF.

---

### Option B: Run via Command Line (CLI)

python meeting_notes_generator.py "path/to/your/audio_file.wav"  

Generated PDFs are saved in the `meeting_outputs/` directory.

---

## 📂 Project Structure

RENA-Meeting-Intelligence-System/  
├── fonts/  
│   └── NotoSansDevanagari-Regular.ttf  
├── meeting_outputs/  
├── meeting_notes_generator.py  
├── app.py  
├── requirements.txt  
└── README.md  

---

## 🔑 Configuration

### Google Gemini API Key

Open `meeting_notes_generator.py` and replace:  

GEMINI_API_KEY = "YOUR_OWN_GOOGLE_API_KEY"  

For production, use environment variables or Streamlit secrets.

---

### Hindi Font Support

Place `NotoSansDevanagari-Regular.ttf` inside the `fonts/` directory to enable Hindi text rendering in PDFs.

---

## 🔮 Future Roadmap

- Real-time meeting transcription
- Speaker diarization (Who said what)
- Calendar integration for follow-ups
- Dockerized cloud deployment (AWS / GCP)

---

## 👤 Author

**Chandisha Das**  
B.Tech Computer Science Engineering  
AI / ML | Speech Intelligence | LLM Systems  
