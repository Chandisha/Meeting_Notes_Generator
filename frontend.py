import streamlit as st
import subprocess
import os
import time
import sys
from pathlib import Path

# --- 1. PAGE CONFIGURATION & STYLING ---
st.set_page_config(
    page_title="RENA | AI Meeting Agent",
    layout="wide",
    page_icon="🤖",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS (FORCED LIGHT BLUE THEME) ---
st.markdown("""
<style>
    /* 1. FORCE Global Light Blue Background */
    [data-testid="stAppViewContainer"] {
        background-color: #f0f4f8 !important; /* Cool Light Blue base */
        background-image: linear-gradient(180deg, #f0f4f8 0%, #d9e2ec 100%) !important;
        background-attachment: fixed !important;
    }
    
    /* Make the top header transparent so it blends in */
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
    }

    /* 2. Typography */
    h1, h2, h3 {
        color: #1e293b !important; /* Dark Slate Blue Text */
        font-family: 'Inter', sans-serif;
        font-weight: 800;
    }
    p, div, label, span {
        color: #475569 !important; /* Slate Grey Text */
    }

    /* 3. The "Hero" Input Box - White on Blue */
    .stTextInput > div > div > input {
        background-color: #ffffff !important;
        color: #1e293b !important;
        border: 2px solid #cbd5e1;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6 !important; /* Blue Focus */
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
    }

    /* 4. Buttons */
    div.stButton > button {
        border-radius: 10px;
        font-weight: 700;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.1s ease;
    }
    div.stButton > button:active {
        transform: scale(0.97);
    }

    /* 5. Report Cards (White Paper on Blue Background) */
    .report-card-container {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 15px;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .report-card-container:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border-color: #3b82f6;
    }

    /* 6. Custom Badges */
    .badge {
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        display: inline-block; /* Ensure badges behave like blocks */
    }
    .badge-daily { background: #dbeafe !important; color: #1e40af !important; border: 1px solid #bfdbfe; }
    .badge-client { background: #fef3c7 !important; color: #92400e !important; border: 1px solid #fde68a; }
    .badge-general { background: #f1f5f9 !important; color: #475569 !important; border: 1px solid #e2e8f0; }

    /* 7. Success Toast */
    .stToast {
        background-color: #ffffff !important;
        border-left: 6px solid #10b981;
        color: #0f172a !important;
        box-shadow: 0 10px 15px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- 2. HEADER SECTION WITH BOT IDENTITY ---
col_bot, col_title = st.columns([0.8, 5])

with col_bot:
    # 3D Bot Avatar Image
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=95) 

with col_title:
    st.markdown("""
        <div style="padding-top: 10px;">
            <h1 style="margin-bottom: 0px; font-size: 3rem; color: #1e293b;">RENA</h1>
            <p style="font-size: 1.2rem; font-weight: 500; color: #64748b; margin-top: -5px;">
                Your AI Meeting Assistant & Note Taker
            </p>
        </div>
    """, unsafe_allow_html=True)

st.write("") # Spacer

# --- 3. MISSION CONTROL (HERO SECTION) ---
with st.container():
    # White Card Container for Controls
    st.markdown('<div style="background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05); border: 1px solid #fff;">', unsafe_allow_html=True)
    
    c1, c2 = st.columns([3.5, 1])
    with c1:
        st.subheader("🚀 Operations Center")
        meet_link = st.text_input("Meeting Coordinates", placeholder="Paste Google Meet Link (e.g., meet.google.com/abc-xyz-123)", label_visibility="collapsed")
    
    with c2:
        st.write("") 
        st.write("") 
        # Primary Action Button
        join_btn = st.button("🔴 START BOT", type="primary", use_container_width=True)

    # --- DEPLOYMENT ANIMATION ---
    if join_btn and meet_link:
        st.write("")
        progress_text = "Waking up RENA..."
        my_bar = st.progress(0, text=progress_text)
        
        deployment_steps = [
            (20, "🔄 Resolving Link...", "Connecting to Meeting Host..."),
            (50, "🧠 Loading Brain...", "Initializing Qwen-2.5 Model..."),
            (80, "🎧 Ears Open...", "Calibrating Audio Inputs..."),
            (100, "✅ ONLINE", "RENA IS LISTENING.")
        ]
        
        for percent, log, label in deployment_steps:
            time.sleep(0.5) 
            my_bar.progress(percent, text=label)
            
        # Backend Trigger
        subprocess.Popen([sys.executable, "rena_bot_pilot.py", meet_link])
        st.toast(f"✅ RENA has joined: {meet_link}", icon="🤖")

    st.markdown('</div>', unsafe_allow_html=True) # End White Card

# --- 4. SECONDARY TOOLS ---
st.write("")
with st.expander("🛠️ Manual Tools & Uploads"):
    ac1, ac2, ac3 = st.columns(3)
    with ac1:
        if st.button("⚡ Join via Clipboard", use_container_width=True):
             st.toast("Reading Clipboard...", icon="📋")
             subprocess.Popen([sys.executable, "rena_bot_pilot.py", "--auto"])
    
    with ac2:
         uploaded_file = st.file_uploader("📂 Upload Recording", type=["wav", "mp3"], label_visibility="collapsed")
    
    with ac3:
         if uploaded_file and st.button("Analyze File", use_container_width=True):
            save_path = Path("temp_audio.wav")
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.info("🧠 RENA is processing the file...")
            subprocess.Popen([sys.executable, "meeting_notes_generator.py", str(save_path)])

# --- 5. INTELLIGENCE FEED ---
st.markdown("---")
st.subheader("📑 RENA's Notebook")

# Feed Controls
fc1, fc2 = st.columns([4, 1])
with fc1:
    st.caption("All your meeting intelligence, neatly organized.")
with fc2:
    auto_refresh = st.toggle("🔴 Live Sync", value=False)
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()

# --- 6. REPORT CARD RENDERING ---
output_dir = Path("meeting_outputs")
output_dir.mkdir(exist_ok=True)
files = sorted(list(output_dir.glob("*.pdf")), key=os.path.getmtime, reverse=True)

if not files:
    st.info("👋 Hi there! I haven't attended any meetings yet. Send me to one above!")
else:
    for pdf_file in files:
        mod_time = os.path.getmtime(pdf_file)
        time_str = time.strftime('%d %b %Y • %I:%M %p', time.localtime(mod_time))
        clean_name = pdf_file.stem.replace("_", " ").replace("report", "").upper()
        
        # Determine Tag Style
        if "DAILY" in clean_name:
            tag_html = "<span class='badge badge-daily'>Daily Standup</span>"
        elif "CLIENT" in clean_name:
            tag_html = "<span class='badge badge-client'>Client Call</span>"
        else:
            tag_html = "<span class='badge badge-general'>General</span>"

        # --- RENDER CARD ---
        with st.container():
            st.markdown(f"""
            <div class="report-card-container">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div style="display: flex; align-items: center; gap: 20px;">
                        <div style="background: #eff6ff; padding: 10px; border-radius: 10px;">
                            <img src="https://cdn-icons-png.flaticon.com/512/337/337946.png" width="35" style="display:block;">
                        </div>
                        <div>
                            <h4 style="margin: 0; color: #1e293b; font-size: 1.1rem;">{clean_name}</h4>
                            <div style="margin-top: 8px; display: flex; align-items: center; gap: 10px;">
                                {tag_html} 
                                <span style="font-size: 0.8em; color: #64748b;">📅 {time_str}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Download Button aligned with card
            col_spacer, col_dl = st.columns([4, 1])
            with col_dl:
                 with open(pdf_file, "rb") as f:
                    st.download_button(
                        label="⬇️ Download PDF",
                        data=f,
                        file_name=pdf_file.name,
                        mime="application/pdf",
                        key=str(pdf_file),
                        use_container_width=True
                    )

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=60)
    st.title("Settings")
    
    st.markdown("### 🤖 Bot Identity")
    st.info("Name: **RENA**\n\nRole: **Enterprise Secretary**")
    
    if st.button("Reconnect Google Account"):
        subprocess.Popen([sys.executable, "rena_bot_pilot.py", "--setup"])
    
    st.markdown("---")
    st.markdown("### 📊 Status")
    st.markdown("✅ **Brain:** Online")
    st.markdown("✅ **Ears:** Connected")
    st.markdown("✅ **Storage:** Local")

# --- AUTO REFRESH ---
if auto_refresh:
    time.sleep(5)
    st.rerun()
