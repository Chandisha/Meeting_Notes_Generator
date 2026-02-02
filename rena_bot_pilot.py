import os
import sys
import time
import subprocess
import threading
import signal
import re
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
import pyperclip

# --- HELPER FUNCTIONS ---

def is_meet_url(text: str) -> bool:
    return isinstance(text, str) and text.startswith("https://meet.google.com/")

def wait_for_meet_link_from_clipboard():
    print("👀 Auto Mode ON: Copy Google Meet link (Ctrl+C) to start bot...")
    last = ""
    while True:
        current = pyperclip.paste().strip()
        if current != last and is_meet_url(current):
            print(f"✅ Meet URL detected from clipboard: {current}")
            return current
        last = current
        time.sleep(1)

# --- IMPORT AI GENERATOR ---
try:
    from meeting_notes_generator import AdaptiveMeetingNotesGenerator
except ImportError:
    print("❌ Error: Could not find meeting_notes_generator.py in the same directory.")
    sys.exit(1)

# --- MAIN BOT CLASS ---

class RenaMeetingBot:
    """
    Rena AI Meeting Bot v1.4 (Robust Audio Setup)
    """
    
    def __init__(self, bot_name="Rena AI (Note Taker)"):
        self.bot_name = bot_name
        self.output_dir = Path("meeting_outputs") / "recordings"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.is_recording = False
        self.audio_process = None
        self.recording_path = None

    def get_audio_device_name(self, ffmpeg_exe):
        """Finds the actual name of the VB-CABLE device on this system."""
        try:
            cmd = [ffmpeg_exe, "-list_devices", "true", "-f", "dshow", "-i", "dummy"]
            res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
            output = res.stderr
            matches = re.findall(r'"(CABLE Output [^"]+)"', output)
            if matches:
                return f"audio={matches[0]}"
            return "audio=CABLE Output (VB-Audio Virtual Cable)"
        except:
            return "audio=CABLE Output (VB-Audio Virtual Cable)"

    def start_audio_recording(self, filename):
        """Starts FFmpeg with auto-device detection and signal boost."""
        self.recording_path = self.output_dir / f"{filename}.wav"
        
        # Discover FFmpeg
        ffmpeg_exe = "ffmpeg"
        common_paths = [
            r"C:\Users\user\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin\ffmpeg.exe",
            r'C:\ffmpeg\bin\ffmpeg.exe',
            r"C:\Program Files\ffmpeg\bin\ffmpeg.exe"
        ]
        for p in common_paths:
            if os.path.exists(p):
                ffmpeg_exe = p
                break
        
        device_name = self.get_audio_device_name(ffmpeg_exe)
        print(f"🎬 Using FFmpeg at: {ffmpeg_exe}")
        print(f"🎙️ Target Device: {device_name}")
        print(f"🎙️ Starting recording: {self.recording_path}")

        # Command with low-latency and slight volume boost (2x)
        command = [
            ffmpeg_exe, '-y',
            '-f', 'dshow',
            '-i', device_name,
            '-af', 'volume=2.0',
            str(self.recording_path)
        ]
        
        try:
            self.audio_process = subprocess.Popen(
                command, 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
            self.is_recording = True
        except Exception as e:
            print(f"❌ FAILED TO START RECORDING: {e}")
            self.is_recording = False

    def stop_audio_recording(self):
        """Gracefully stops the FFmpeg process."""
        if self.audio_process:
            print("🛑 Stopping recording...")
            self.audio_process.send_signal(signal.CTRL_BREAK_EVENT)
            self.audio_process.wait()
            self.is_recording = False
            print(f"✅ Recording saved to: {self.recording_path}")

    def setup_mode(self):
        """Opens browser strictly for the user to log in manually."""
        print("🔑 SETUP MODE: Please log in to your Google Account.")
        print("⚠️  Use this window to sign in. Close it when you are done.")
        
        with sync_playwright() as p:
            user_data_dir = os.path.join(os.getcwd(), "bot_session")
            
            context = p.chromium.launch_persistent_context(
                user_data_dir,
                headless=False,
                viewport={'width': 1280, 'height': 720},
                channel="chrome", 
                args=["--disable-blink-features=AutomationControlled"]
            )
            page = context.new_page()
            
            print("🚀 Opening Google Sign-in Page...")
            try:
                page.goto("https://accounts.google.com/signin")
                while context.pages:
                    time.sleep(1)
            except Exception:
                print("✅ Browser closed. Login session saved!")

    def join_google_meet(self, meet_url):
        """Launches browser and handles the joining flow."""
        with sync_playwright() as p:
            user_data_dir = os.path.join(os.getcwd(), "bot_session")
            
            context = p.chromium.launch_persistent_context(
                user_data_dir,
                headless=False,
                viewport={'width': 1280, 'height': 720},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                args=[
                    "--use-fake-ui-for-media-stream",
                    "--use-fake-device-for-media-stream",
                    "--disable-blink-features=AutomationControlled"
                ]
            )
            
            page = context.pages[0] if context.pages else context.new_page()
            stealth = Stealth()
            stealth.apply_stealth_sync(page)
            
            print(f"🚀 Navigating to: {meet_url}")
            page.goto(meet_url)
            
            try:
                print("⏳ Waiting for page to load (10s)...")
                time.sleep(10) 
                
                # Check for blocking or dialogs
                try: page.click("text=Dismiss", timeout=3000)
                except: pass

                # Input Name
                try:
                    name_input = page.wait_for_selector('input[aria-label="Your name"], input[type="text"]', timeout=5000)
                    if name_input:
                        name_input.click()
                        name_input.fill(self.bot_name)
                        page.keyboard.press("Enter")
                except: pass
                
                # Turn off Cam/Mic
                time.sleep(2)
                page.keyboard.press("Control+e")
                page.keyboard.press("Control+d")
                print("🔇 Camera and Mic toggled off.")

                # Click Join
                join_selectors = [
                    'span:has-text("Ask to join")', 'span:has-text("Join now")',
                    'button:has-text("Ask to join")', 'button:has-text("Join now")'
                ]
                for selector in join_selectors:
                    if page.is_visible(selector):
                        page.locator(selector).first.click()
                        print("📩 Join request sent.")
                        break

                print("⏳ Waiting for admission...")
                page.wait_for_selector('button[aria-label="Leave call"]', timeout=300000) 
                print("🎉 Bot is in the meeting.")

                # --- AUTO-CONFIGURE SPEAKER (ROBUST VERSION) ---
                try:
                    print("⚙️ Auto-configuring audio output to VB-CABLE...")
                    # 1. Open Options Menu
                    page.wait_for_selector('button[aria-label="More options"]', timeout=5000).click()
                    
                    # 2. Click Settings
                    page.wait_for_selector('li[role="menuitem"]:has-text("Settings")', timeout=5000).click()
                    time.sleep(2) # Allow modal to animate
                    
                    # 3. Ensure we are on the Audio Tab
                    try: page.click('li[role="tab"]:has-text("Audio")', timeout=2000)
                    except: pass 

                    # 4. Click Speakers Dropdown
                    page.click('[aria-label="Speakers"]', timeout=5000)
                    time.sleep(1)
                    
                    # 5. Smart Search for Cable
                    # We try to scroll down just in case it's hidden
                    page.keyboard.press("ArrowDown")
                    page.keyboard.press("ArrowDown")
                    
                    # Look for ANY text containing "CABLE" (Partial match is safer)
                    cable_option = page.locator('li[role="option"]').filter(has_text="CABLE").first
                    
                    if cable_option.is_visible():
                        cable_option.click()
                        print("✅ Speaker successfully set to Virtual Cable.")
                    else:
                        print("⚠️ Could not find 'CABLE' in the list automatically.")
                        raise Exception("Cable option not visible")
                    
                    # Close Settings
                    page.keyboard.press("Escape")
                    
                except Exception as e:
                    print("\n" + "!"*50)
                    print(f"⚠️  AUTO SETUP FAILED: {e}")
                    print("👉 ACTION REQUIRED: Please Manually set Speaker to 'VB-Cable' NOW.")
                    print("👉 Do NOT close this window. Just change the setting.")
                    print("!"*50 + "\n")
                    # Try to close menu if stuck open
                    try: page.keyboard.press("Escape")
                    except: pass

                # Start Recording
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                self.start_audio_recording(f"meeting_{timestamp}")

                # Monitor Loop
                while True:
                    if not page.is_visible('button[aria-label="Leave call"]'):
                        print("📴 Meeting ended.")
                        break
                    time.sleep(5)

            except Exception as e:
                print(f"⚠️ Session interrupted: {e}")
            finally:
                self.stop_audio_recording()
                try: context.close()
                except: pass
                
                if self.recording_path and os.path.exists(self.recording_path):
                    self.run_ai_pipeline()

    def run_ai_pipeline(self):
        """Triggers the analysis pipeline."""
        print("\n" + "="*60)
        print("🤖 STARTING AI ANALYSIS")
        print("="*60)
        generator = AdaptiveMeetingNotesGenerator()
        generator.process(str(self.recording_path))
        print("🎉 COMPLETE!")


# --- ENTRY POINT ---

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "--setup":
            RenaMeetingBot().setup_mode()
            sys.exit(0)

        if len(sys.argv) > 1 and sys.argv[1] == "--auto":
            meet_url = wait_for_meet_link_from_clipboard()
            RenaMeetingBot().join_google_meet(meet_url)

        else:
            url = sys.argv[1] if len(sys.argv) > 1 else ""
            if not url:
                print("Usage: python rena_bot_pilot.py <MEET_URL>")
                sys.exit(1)

            RenaMeetingBot().join_google_meet(url)

    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
