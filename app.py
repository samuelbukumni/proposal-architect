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
st.subheader("Document Construction")

col1, col2 = st.columns(2)
with col1:
    overview = st.text_area("1. OVERVIEW", height=120, 
        value="This collaboration brings together the RUN-N-RAVE community to deliver a unique urban trail run experience ahead of the race weekend.") # [cite: 4]
    
    goals = st.text_area("3. STRATEGIC INTENT", height=120,
        value="• Primary: Showcase footwear versatility (Comfort, Grip, Stability)\n• Secondary: Generate authentic performance-based content.") # [cite: 14, 20]
    
    concept = st.text_area("4. ACTIVATION CONCEPT", height=120,
        value="1. Meet-Up @ LAB: Shoe fitting & test model distribution.\n2. Social Run: Transition from pavement to forest trails.\n3. Post-Run: DJ set, catering, and shoe feedback.") # [cite: 26, 38]
    
    why_us = st.text_area("8. WHY RUN-N-RAVE", height=120, 
        value="RUN-N-RAVE is a cultural leader combining music and movement, hosting 150+ runners weekly in our community space.") # [cite: 75, 76]

with col2:
    deliverables = st.text_area("5. DELIVERABLES", height=120,
        value="- Professional Event Photography\n- 2x Instagram Reels (Teaser + Recap)\n- Full on-site shoe testing integration.") # [cite: 40, 41, 48]
    
    kpis = st.text_area("6. KPIs & SUCCESS METRICS", height=120,
        value="- Participants: 50+ runners\n- Adoption: 70-80% testing footwear\n- Social: High Story & Reel interaction.") # [cite: 53, 56, 62]
    
    investment = st.text_area("7. INVESTMENT", height=120,
        value="Partner Fee: €950\nProduction Costs (Photography/Catering): €600\nTotal: €1,550") # [cite: 66, 73]
    
    next_steps = st.text_area("9. NEXT STEPS", height=120,
        value="- Budget confirmation\n- Shoe model confirmation + sizing plan\n- Content brief alignment.") # [cite: 81, 83]

# --- 4. PDF ENGINE CLASS ---
class GS26_PDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("helvetica", "B", 10)
            self.set_text_color(150, 150, 150)
            self.cell(0, 10, "Collaboration Brief & Statement of Work (SOW)", 
                      align="R", new_x="LMARGIN", new_y="NEXT")

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
            # Bullet point alignment fix
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
            self.ln(7) # Space between lines

def clean_text(text):
    if not text: return ""
    rep = {"’": "'", "‘": "'", "“": '"', "”": '"', "—": "-", "–": "-"}
    for s, r in rep.items(): text = text.replace(s, r)
    return text.encode('latin-1', 'replace').decode('latin-1')

def create_pdf():
    pdf = GS26_PDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    
    # --- PAGE 1: COVER ---
    pdf.add_page()
    if logo_file:
        img = Image.open(logo_file)
        img.save("temp_logo.png")
        pdf.image("temp_logo.png", x=85, y=50, w=40)
    
    pdf.set_y(120)
    pdf.set_font("helvetica", "B", 35)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 15, f"PROPOSAL\nFOR\n{clean_text(partner).upper()}", align="C")
    
    pdf.ln(10)
    pdf.set_font("helvetica", "B", 18)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 10, f"{clean_text(event_name)}".upper(), 
             align="C", new_x="LMARGIN", new_y="NEXT")
    
    # --- PAGE 2: SEPARATED SECTIONS ---
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
        # Only print if content exists beyond the static details
        if cleaned_content and cleaned_content != "VENUE: \nDATE: ":
            pdf.set_font("helvetica", "B", 13)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
            pdf.draw_section_line()
            pdf.set_text_color(50, 50, 50)
            pdf.write_styled_text(cleaned_content)
            pdf.ln(5)

    # --- FINAL CONTACT BLOCK (Based on Ben Olayinka's details) ---
    pdf.ln(10)
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, "Contact:", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("helvetica", "B", 11)
    pdf.cell(0, 7, "Ben Olayinka", new_x="LMARGIN", new_y="NEXT") # [cite: 86]
    
    pdf.set_font("helvetica", "", 11)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 6, "Founder - RUN-N-RAVE", new_x="LMARGIN", new_y="NEXT") # [cite: 87]
    pdf.cell(0, 6, "ben@inlivingcolor.de", new_x="LMARGIN", new_y="NEXT") # [cite: 88]

    # FILENAME & CLEANUP
    safe_name = "".join(x for x in partner if x.isalnum() or x in "._- ").strip().replace(' ', '_')
    filename = f"Proposal_{safe_name}.pdf"
    pdf.output(filename)

    if os.path.exists("temp_logo.png"):
        os.remove("temp_logo.png")
        
    return filename

# --- 5. EXECUTION BUTTON ---
if st.button("GENERATE OFFICIAL PDF"):
    if partner and event_name:
        try:
            file_path = create_pdf()
            with open(file_path, "rb") as f:
                st.download_button("↓ DOWNLOAD PDF", f, file_name=file_path)
            st.success(f"Proposal Architecture for {partner} Complete.")
        except Exception as e:
            st.error(f"Error during construction: {e}")
    else:
        st.warning("Architectural Note: Partner Name and Activation Title are required.")
