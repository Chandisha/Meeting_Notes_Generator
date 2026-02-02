import os
import json
import warnings
import sys
import time
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# --- AI LIBRARIES ---
from faster_whisper import WhisperModel
from loguru import logger

# 1. Google GenAI (Primary - Cloud)
try:
    from google import genai
    from google.genai import types
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False

# 2. Ollama (Fallback - Local)
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

# --- REPORTLAB (PDF) IMPORTS ---
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

warnings.filterwarnings("ignore")

# ==========================================
# 🔑 CONFIGURATION
# ==========================================
GEMINI_API_KEY = "YOUR_OWN_GOOGLE_API_KEY"

# RECOMMENDATION: Use "qwen2.5:32b" for best intelligence.
OLLAMA_MODEL = "qwen2.5:32b" 

OUTPUT_DIR = Path("meeting_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)
FONTS_DIR = Path(r"C:\Users\admin\Desktop\RENA-Meet\fonts") 

# --- CONFIGURE LOGGER ---
logger.remove()
logger.add(sys.stderr, format="<green>{time:HH:mm:ss}</green> | <level>{message}</level>")

def setup_fonts():
    """Loads Hindi font for PDF support"""
    font_path = FONTS_DIR / "NotoSansDevanagari-Regular.ttf"
    if font_path.exists():
        try:
            pdfmetrics.registerFont(TTFont('HindiFont', str(font_path)))
            return True
        except: return False
    return False

HINDI_AVAILABLE = setup_fonts()

class AdaptiveMeetingNotesGenerator:
    def __init__(self, whisper_model="medium"):
        print("\n" + "="*60)
        logger.info(f"🔧 SYSTEM INIT | Model: {OLLAMA_MODEL}")
        print("="*60)

        # 1. SETUP GOOGLE
        self.google_client = None
        if GOOGLE_AVAILABLE:
            try:
                self.google_client = genai.Client(api_key=GEMINI_API_KEY)
                logger.info("   [Primary] Google Gemini Client Initialized.")
            except: pass

        # 2. SETUP OLLAMA
        if OLLAMA_AVAILABLE:
            try:
                ollama.list()
                logger.info(f"   [Fallback] Local Ollama Ready ({OLLAMA_MODEL}).")
            except:
                logger.warning("⚠️ Ollama not reachable. Run 'ollama serve' in terminal.")

        # 3. SETUP WHISPER
        logger.info(f"   [Audio] Loading Whisper ({whisper_model})...")
        try:
            self.whisper = WhisperModel(whisper_model, device="cpu", compute_type="int8")
            logger.info("   [Status] Whisper Ready.")
        except Exception as e:
            logger.error(f"❌ Whisper Failed: {e}")
            sys.exit(1)

    # --- STEP 1: TRANSCRIPTION ---
    def transcribe(self, audio_path: str) -> Dict:
        print("\n" + "-"*60)
        logger.info("🎙️ STEP 1: TRANSCRIPTION")
        print("-"*60)
        
        if not os.path.exists(audio_path):
            logger.error("Audio file does not exist.")
            return {"transcript": "", "segments": []}

        # Relaxed VAD parameters
        segments, _ = self.whisper.transcribe(
            audio_path,
            beam_size=5,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500) 
        )

        full_text = []
        transcript_segments = []
        
        print("   Processing Timeline: ", end="")
        has_speech = False
        
        for segment in segments:
            has_speech = True
            text = segment.text.strip()
            
            m, s = divmod(int(segment.start), 60)
            timestamp = f"{m:02d}:{s:02d}"
            
            transcript_segments.append({"timestamp": timestamp, "text": text})
            full_text.append(f"[{timestamp}] {text}")
            print("▓", end="", flush=True)
            
        print(" [Done]")
        
        if not has_speech:
            logger.warning("⚠️  NO SPEECH DETECTED.")
            return {"transcript": "", "segments": []}

        return {
            "transcript": "\n".join(full_text), 
            "segments": transcript_segments
        }

    # --- STEP 2: PIPELINE EXECUTION ---
    def analyze_transcript(self, transcript: str) -> Dict:
        print("\n" + "-"*60)
        logger.info("🧠 STEP 2: AI PIPELINE (Sum -> Hindi -> MOM -> Actions)")
        print("-"*60)
        
        if not transcript:
            return {"detected_context": "No Audio", "summary_en": "No speech detected.", "summary_hi": "-", "mom": [], "actions": []}

        # --- UPDATED PROMPT TO CATCH 'HIDDEN' ACTIONS ---
        prompt = f"""
        You are an expert Meeting Secretary. Follow this pipeline STRICTLY:

        SOURCE TRANSCRIPT:
        {transcript[:50000]}
        
        YOUR TASKS (Execute in order):
        1. **Analyze Context**: Identify the main topic and speakers.
        2. **English Summary**: Write a comprehensive executive summary (4-5 sentences).
        3. **Hindi Translation**: Translate the English summary from Step 2 into Hindi (Devanagari).
        4. **MOM (Minutes)**: Extract general discussion points.
        5. **Action Plan (CRITICAL)**: EXTRACT ALL TASKS AND DEADLINES.
           - **IMPORTANT**: If a speaker says "I have to do this by [Date]" or "This is due [Date]", treat it as an ACTION ITEM, not just a minute.
           - Convert implied tasks into clear actions.
           - Extract the Task, the Owner (Speaker/Team), and the Deadline.
           - Example Input: "I have to do it by today." -> Action Output: {{ "task": "Complete the demo project", "owner": "Speaker", "deadline": "Today (2nd Feb)" }}

        OUTPUT FORMAT: Provide ONLY this JSON structure.
        {{
            "detected_context": "Meeting Topic",
            "summary_en": "The meeting focused on...",
            "summary_hi": "बैठक का मुख्य विषय...",
            "mom": ["Point 1", "Point 2", "Point 3"],
            "actions": [
                {{ "task": "Submit Demo Project", "owner": "Student/Speaker", "deadline": "2nd February 2026" }},
                {{ "task": "Review deliverables", "owner": "Team", "deadline": "Immediate" }}
            ]
        }}
        """

        # 1. Try Gemini
        if self.google_client:
            try:
                logger.info("   [Primary] Sending to Google Cloud...")
                response = self.google_client.models.generate_content(
                    model="gemini-1.5-flash-latest",
                    contents=prompt,
                    config=types.GenerateContentConfig(response_mime_type="application/json")
                )
                logger.info("   [Success] Google Cloud responded.")
                return json.loads(response.text)
            except Exception as e:
                logger.error(f"   ❌ Gemini Error: {e}")

        # 2. Try Local Ollama
        if OLLAMA_AVAILABLE:
            logger.info(f"   [Fallback] running on Local GPU ({OLLAMA_MODEL})...")
            try:
                response = ollama.chat(model=OLLAMA_MODEL, messages=[
                    {'role': 'system', 'content': 'You are a JSON-only API. Output ONLY valid JSON.'},
                    {'role': 'user', 'content': prompt},
                ])
                
                raw = response['message']['content']
                clean = self._clean_json(raw)
                logger.info("   [Success] Local AI responded.")
                return json.loads(clean)
            except Exception as e:
                logger.error(f"   ❌ Local AI Error: {e}")

        return {}

    def _clean_json(self, text):
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1:
            return text[start:end+1]
        return text

    # --- STEP 3: PDF REPORT ---
    def generate_pdf(self, intel: Dict, segments: List[Dict], filename: str):
        print("\n" + "-"*60)
        logger.info("📄 STEP 3: GENERATING PDF")
        print("-"*60)
        
        pdf_path = OUTPUT_DIR / f"{filename}.pdf"
        
        try:
            doc = SimpleDocTemplate(str(pdf_path), pagesize=letter)
            styles = getSampleStyleSheet()
            
            # Custom Styles
            style_title = ParagraphStyle('T', parent=styles['Heading1'], fontSize=20, textColor=colors.navy, spaceAfter=20)
            style_h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=14, textColor=colors.black, spaceBefore=15, spaceAfter=5)
            style_body = ParagraphStyle('B', parent=styles['Normal'], fontSize=11, leading=14)
            style_hindi = ParagraphStyle('Hi', parent=styles['Normal'], fontSize=11, fontName='HindiFont' if HINDI_AVAILABLE else 'Helvetica')
            style_action = ParagraphStyle('Act', parent=styles['Normal'], fontSize=11, leading=14, leftIndent=10)

            elements = []

            # HEADER
            elements.append(Paragraph("MEETING INTELLIGENCE REPORT", style_title))
            elements.append(Paragraph(f"<b>Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}", style_body))
            elements.append(Spacer(1, 15))

            # 1. SUMMARY (ENG)
            elements.append(Paragraph("EXECUTIVE SUMMARY (English)", style_h2))
            elements.append(Paragraph(intel.get('summary_en', 'N/A'), style_body))
            
            # 2. SUMMARY (HINDI)
            elements.append(Paragraph("EXECUTIVE SUMMARY (Hindi)", style_h2))
            elements.append(Paragraph(intel.get('summary_hi', 'N/A'), style_hindi))
            elements.append(Spacer(1, 10))

            # 3. MOM
            if intel.get('mom'):
                elements.append(Paragraph("MINUTES OF MEETING", style_h2))
                for point in intel['mom']:
                    elements.append(Paragraph(f"• {point}", style_body))
                    elements.append(Spacer(1, 3))

            # 4. ACTION PLANS (Fixed Bullet Style)
            actions = intel.get('actions', [])
            if actions:
                logger.info(f"   [Actions] Found {len(actions)} action items. Adding to PDF...")
                elements.append(Spacer(1, 15))
                elements.append(Paragraph("ACTION PLANS & TASKS", style_h2))
                
                for a in actions:
                    task = a.get('task', 'No task description')
                    owner = a.get('owner', 'Unassigned')
                    deadline = a.get('deadline', 'TBD')
                    
                    # Format: • Task Name
                    #           (Owner: X | Deadline: Y)
                    text = f"• <b>{task}</b> <br/>&nbsp;&nbsp;&nbsp;<i>(Owner: {owner} | Deadline: {deadline})</i>"
                    
                    elements.append(Paragraph(text, style_action))
                    elements.append(Spacer(1, 8)) # Slightly more space between actions
            else:
                logger.info("   [Actions] No action items detected in transcript.")

            # 5. TRANSCRIPT
            elements.append(PageBreak())
            elements.append(Paragraph("FULL TRANSCRIPT", style_h2))
            
            if not segments:
                elements.append(Paragraph("<i>(No audible speech detected in recording)</i>", style_body))
            else:
                for s in segments:
                    p = f"<b>[{s['timestamp']}]</b> {s['text']}"
                    elements.append(Paragraph(p, style_body))
                    elements.append(Spacer(1, 4))

            doc.build(elements)
            logger.info(f"   [File] Saved to: {pdf_path}")
            return str(pdf_path)

        except Exception as e:
            logger.error(f"❌ PDF Generation Error: {e}")
            import traceback
            traceback.print_exc()
            return None

    def process(self, audio_file):
        # 1. Transcribe
        res = self.transcribe(audio_file)
        
        # 2. Analyze
        intel = self.analyze_transcript(res['transcript'])
        
        # 3. Generate PDF
        filename = Path(audio_file).stem + "_report"
        final_pdf = self.generate_pdf(intel, res['segments'], filename)
        
        if final_pdf:
            print(f"\n🎉 SUCCESS! Report ready: {final_pdf}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        AdaptiveMeetingNotesGenerator().process(sys.argv[1])
    else:
        print("Usage: python meeting_notes_generator.py <file.wav>")
