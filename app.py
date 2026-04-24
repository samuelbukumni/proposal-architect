import streamlit as st
from fpdf import FPDF
import re
from PIL import Image
import os

# --- 1. CONFIG & UI STYLING ---
st.set_page_config(page_title="PROPOSAL ARCHITECT | GS-26", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stTextArea textarea { font-size: 14px; border-radius: 8px; border: 1px solid #d0d0d0; }
    .stButton>button { 
        width: 100%; border-radius: 8px; height: 3.5em; 
        background-color: black; color: white; font-weight: bold; 
    }
    </style>
    """, unsafe_allow_html=True)

st.title("RUN-N-RAVE ENGINE")
st.caption("2026 OFFICIAL | ARCHITECTURE BY GS-26")

# --- 2. SIDEBAR (EMPTY FIELDS FOR FRESH START) ---
with st.sidebar:
    st.header("Project Identity")
    partner = st.text_input("Brand Partner", placeholder="e.g. Saucony")
    event_name = st.text_input("Activation Title", placeholder="e.g. Urban Trail Run")
    venue = st.text_input("Venue", placeholder="e.g. RUN-N-RAVE LAB")
    date_val = st.text_input("Date", placeholder="e.g. Friday, March 27")
    st.divider()
    logo_file = st.file_uploader("Upload Brand/Event Logo", type=["png", "jpg", "jpeg"])

# --- 3. MAIN UI ---
st.subheader("Document Construction")
col1, col2 = st.columns(2)
with col1:
    overview = st.text_area("1. OVERVIEW", height=120)
    goals = st.text_area("3. STRATEGIC INTENT", height=120)
    concept = st.text_area("4. ACTIVATION CONCEPT", height=120)
    why_us = st.text_area("8. WHY RUN-N-RAVE", height=120)
with col2:
    deliverables = st.text_area("5. DELIVERABLES", height=120)
    kpis = st.text_area("6. KPIs & SUCCESS METRICS", height=120)
    investment = st.text_area("7. INVESTMENT", height=120)
    next_steps = st.text_area("9. NEXT STEPS", height=120)

# --- 4. PDF ENGINE CLASS ---
class GS26_PDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("helvetica", "B", 10)
            self.set_text_color(150, 150, 150)
            self.cell(0, 10, "Collaboration Brief & Statement of Work (SOW)", align="R", new_x="LMARGIN", new_y="NEXT")

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(180, 180, 180)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def draw_section_line(self):
        self.set_draw_color(230, 230, 230)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def write_styled_text(self, text):
        lines = text.split('\n')
        for line in lines:
            if line.strip().startswith(('-', '*', '•')):
                self.set_x(15)
            parts = re.split(r'(\*\*.*?\*\*|\*.*?\*)', line)
            for part in parts:
                if part.startswith('**') and part.endswith('**'):
                    self.set_font("helvetica", "B", 11)
                    self.write(7, part.strip('**'))
                elif part.startswith('*') and part.endswith('*'):
                    self.set_font("helvetica", "I", 11)
                    self.write(7, part.strip('*'))
                else:
                    self.set_font("helvetica", "", 11)
                    self.write(7, part)
            self.ln(7)

def clean_text(text):
    if not text: return ""
    # REPLACING SYMBOLS THAT CAUSE '?' ERRORS
    rep = {
        "’": "'", "‘": "'", "“": '"', "”": '"', "—": "-", "–": "-",
        "€": "EUR ", "$": "USD ", "•": "-" 
    }
    for s, r in rep.items(): text = text.replace(s, r)
    return text.encode('latin-1', 'replace').decode('latin-1')

def create_pdf():
    pdf = GS26_PDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    
    # PAGE 1: COVER
    pdf.add_page()
    if logo_file:
        img = Image.open(logo_file)
        img.save("temp_logo.png")
        pdf.image("temp_logo.png", x=85, y=50, w=40)
    
    pdf.set_y(120)
    pdf.set_font("helvetica", "B", 35)
    pdf.multi_cell(0, 15, f"PROPOSAL\nFOR\n{clean_text(partner).upper()}", align="C")
    
    pdf.ln(10)
    pdf.set_font("helvetica", "B", 18)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 10, f"{clean_text(event_name)}".upper(), align="C", new_x="LMARGIN", new_y="NEXT")
    
    # PAGE 2: CONTENT
    pdf.add_page()
    sections = [
        ("1. OVERVIEW", overview),
        ("2. PROJECT DETAILS", f"VENUE: {venue}\nDATE: {date_val}"),
        ("3. GOALS & STRATEGIC INTENT", goals),
        ("4. ACTIVATION CONCEPT", concept),
        ("5. DELIVERABLES", deliverables),
        ("6. KPIs & SUCCESS METRICS", kpis),
        ("7. INVESTMENT", investment),
        ("8. WHY RUN-N-RAVE", why_us),
        ("9. NEXT STEPS", next_steps)
    ]
    
    for title, content in sections:
        cleaned_content = clean_text(content).strip()
        if cleaned_content and cleaned_content != "VENUE: \nDATE: ":
            # CHECK FOR SPACE (Prevent single lines on new pages)
            if pdf.get_y() > 230: 
                pdf.add_page()
                
            pdf.set_font("helvetica", "B", 13)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
            pdf.draw_section_line()
            pdf.set_text_color(50, 50, 50)
            pdf.write_styled_text(cleaned_content)
            pdf.ln(5)

    # CONTACT BLOCK
    pdf.ln(10)
    pdf.set_font("helvetica", "B", 11)
    pdf.cell(0, 7, "Ben Olayinka", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 11)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 6, "Founder - RUN-N-RAVE", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, "ben@inlivingcolor.de", new_x="LMARGIN", new_y="NEXT")

    safe_name = "".join(x for x in partner if x.isalnum() or x in "._- ").strip().replace(' ', '_')
    filename = f"Proposal_{safe_name}.pdf"
    pdf.output(filename)
    if os.path.exists("temp_logo.png"): os.remove("temp_logo.png")
    return filename

if st.button("GENERATE OFFICIAL PDF"):
    if partner and event_name:
        file_path = create_pdf()
        with open(file_path, "rb") as f:
            st.download_button("↓ DOWNLOAD PDF", f, file_name=file_path)
    else:
        st.warning("Please enter a Brand Partner and Activation Title.")import streamlit as st
from fpdf import FPDF
import re
from PIL import Image
import os

# --- 1. CONFIG & UI STYLING ---
st.set_page_config(page_title="PROPOSAL ARCHITECT | GS-26", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stTextArea textarea { font-size: 14px; border-radius: 8px; border: 1px solid #d0d0d0; }
    .stButton>button { 
        width: 100%; border-radius: 8px; height: 3.5em; 
        background-color: black; color: white; font-weight: bold; 
    }
    .stButton>button:hover { background-color: #333333; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("RUN-N-RAVE ENGINE")
st.caption("2026 OFFICIAL | ARCHITECTURE BY GS-26")

# --- 2. SIDEBAR (IDENTITY MAPPED FROM ACTIVATION BRIEF) ---
with st.sidebar:
    st.header("Project Identity")
    partner = st.text_input("Brand Partner", value="Saucony", placeholder="e.g. Saucony") # [cite: 1]
    event_name = st.text_input("Activation Title", value="Urban Trail Run Berlin", placeholder="e.g. Half Marathon Activation") # [cite: 8]
    venue = st.text_input("Venue", value="RUN-N-RAVE LAB Community Hub", placeholder="Berlin") # [cite: 12]
    date_val = st.text_input("Date", value="Friday, March 27 - 5:30 PM", placeholder="Date & Time") # [cite: 11]
    
    st.divider()
    logo_file = st.file_uploader("Upload Brand/Event Logo", type=["png", "jpg", "jpeg"])

# --- 3. MAIN UI: Proposal Construction ---
