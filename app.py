import streamlit as st
import json
import openai
from fpdf import FPDF
import io
import tempfile
import os
import unicodedata
import base64

# Set the title of the browser tab
st.set_page_config(page_title="Clinical Documentation Assistant")

# OpenAI API Key (ensure to set this securely)
OPENAI_API_KEY = ""
openai.api_key = OPENAI_API_KEY


def add_background(image_file):
    """Adds a blurred background image to the Streamlit app."""
    bg_ext = image_file.split('.')[-1]

    with open(image_file, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()

    bg_css = f"""
    <style>
        #clinical-documentation-assistant, #enter-patient-details {{
            color: #FFFFFF;
        }}
        .stAppHeader {{
            background: transparent;
        }}
        .stApp {{
        }}
        [data-testid="stAppViewContainer"] {{
            backdrop-filter: blur(8px);
            padding: 20px;
        }}
        .stTextInput, .stButton, .stTextArea {{
            border-radius: 10px;
            color: #0d0c22;
        }}
        [data-testid=stMarkdownContainer] p {{
            color: #0d0c22;
        }}
        .stButton > button {{
            color: white !important;
            border-radius: 8px;
            padding: 10px 15px;
            font-size: 16px;
        }}
        /* Header Styling */
        .header-container {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            padding: 20px 0 20px 20px;
            text-align: left;
            font-size: 18px;
            font-weight: bold;
            color: #0d0c22;
            z-index: 1000;
        }}
        #enter-patient-details {{
            color: #0d0c22;
        }}
        /* Space below the header */
        .stApp > div:first-child {{
            padding-top: 80px;
        }}
        
        .stAppDeployButton {{
            display: none;
        }}
        
        .stMainMenu {{
            display: none;
        }}
    </style>
    """
    st.markdown(bg_css, unsafe_allow_html=True)

# Apply background image
add_background("background.jpg")

def generate_soap_note(ehr_data):
    prompt = f"""
    Generate a structured SOAP note based on the following patient data:
    {json.dumps(ehr_data, indent=2)}

    Format:
    **S:** (Subjective - patient-reported symptoms)
    **O:** (Objective - vitals, labs, exam findings)
    **A:** (Assessment - diagnosis, clinical reasoning)
    **P:** (Plan - treatment, follow-up recommendations)
    **ICD-10 Codes:** (Relevant ICD-10 codes)
    **CPT Code:** (Relevant CPT code)
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a medical documentation assistant."},
                  {"role": "user", "content": prompt}],
        max_tokens=500
    )

    return response["choices"][0]["message"]["content"].strip()

def remove_non_ascii(text):
    return ''.join([c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn'])

def replace_special_characters(text):
    replacements = {
        '\u2019': "'",  # Right single quote (’)
        '\u2013': '-',  # En-dash
        '\u2014': '-',  # Em-dash
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def sanitize_text(text):
    text = remove_non_ascii(text)
    text = replace_special_characters(text)
    return text

def convert_bold_text(text, pdf):
    parts = text.split("**")
    for i, part in enumerate(parts):
        if i % 2 == 1:
            pdf.set_font("Arial", style="B", size=12)
        else:
            pdf.set_font("Arial", style="", size=12)
        pdf.multi_cell(0, 10, part)

def export_to_pdf(ehr_data, soap_note, icd_cpt_input):
    soap_note = sanitize_text(soap_note)
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add logo
    if os.path.exists("logo.png"):
        pdf.image("header-logo.png", x=10, y=8, w=30)
    pdf.ln(40)

    pdf.multi_cell(0, 10, f"Patient ID: {ehr_data['PatientID']}")
    pdf.multi_cell(0, 10, f"Chief Complaint: {ehr_data['ChiefComplaint']}")
    pdf.multi_cell(0, 10, f"Conditions: {', '.join(ehr_data['Conditions'])}")
    pdf.multi_cell(0, 10, f"Vitals: BP {ehr_data['Vitals']['BP']}, HR {ehr_data['Vitals']['HR']}, SpO2 {ehr_data['Vitals']['SpO2']}")
    pdf.multi_cell(0, 10, f"Labs: HbA1c {ehr_data['Labs']['HbA1c']}, CBC {ehr_data['Labs']['CBC']}")
    pdf.multi_cell(0, 10, f"Medications: {', '.join(ehr_data['MedicationRequest'])}")
    pdf.ln(10)

    pdf.multi_cell(0, 10, "SOAP Note:")
    convert_bold_text(soap_note, pdf)
    pdf.ln(10)

    pdf.multi_cell(0, 10, "ICD-10/CPT Codes:")
    pdf.multi_cell(0, 10, icd_cpt_input)

    tmp_file_path = tempfile.mktemp(suffix=".pdf")
    pdf.output(tmp_file_path)

    pdf_bytes = io.BytesIO()
    with open(tmp_file_path, "rb") as f:
        pdf_bytes.write(f.read())

    pdf_bytes.seek(0)
    os.remove(tmp_file_path)
    return pdf_bytes

# UI Components
# st.image("logo.png", width=150)
# Create a fixed header with an image next to the text

# Function to encode image as Base64
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Convert the header logo to Base64
header_logo_base64 = image_to_base64("header-logo.png")

header_html = """
<div class="header-container">
    <img src="data:image/png;base64,{header_logo_base64}" alt="Logo">
    <span>Clinical Documentation Assistant</span>
</div>
"""
# Apply CSS for header styling
st.markdown(
    f"""
    <style>
        /* Fixed header styling */
        .header-container {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            padding: 15px 0 15px 10px;
            gap: 15px;
            font-size: 20px;
            font-weight: bold;
            color: #000000;
            z-index: 1000;
        }}

        /* Logo styling */
        .header-container img {{
            height: 38px;
            width: auto;
        }}

        /* Adjust padding to prevent content overlap */
        .stApp > div:first-child {{
            padding-top: 80px;
        }}
    </style>

    <div class="header-container">
        <img src="data:image/png;base64,{header_logo_base64}" alt="Logo">
        <span>Clinical Documentation Assistant</span>
    </div>
    """,
    unsafe_allow_html=True
)
# st.title("Clinical Documentation Assistant")

st.subheader("Enter Patient Details")
patient_id = st.text_input("Patient ID", "20351235")
chief_complaint = st.text_input("Chief Complaint", "Shortness of breath")
conditions = st.text_area("Conditions (comma-separated)", "Hypertension, Diabetes")
bp = st.text_input("Blood Pressure", "150/90")
hr = st.text_input("Heart Rate", "98")
spo2 = st.text_input("SpO2", "91%")
hba1c = st.text_input("HbA1c", "8.2%")
cbc = st.text_input("CBC", "Normal")
medications = st.text_area("Medications (comma-separated)", "Metformin, Lisinopril")

generate_button = st.button("Generate SOAP Note")

if generate_button:
    ehr_data = {
        "PatientID": patient_id,
        "ChiefComplaint": chief_complaint,
        "Conditions": [c.strip() for c in conditions.split(",")],
        "Vitals": {"BP": bp, "HR": hr, "SpO2": spo2},
        "Labs": {"HbA1c": hba1c, "CBC": cbc},
        "MedicationRequest": [m.strip() for m in medications.split(",")]
    }

    soap_note = generate_soap_note(ehr_data)
    formatted_soap_note = soap_note.replace("**", "")
    st.markdown(formatted_soap_note)

    icd_cpt_suggestions = "ICD-10: I50.9 (Heart failure, unspecified), E11.65 (Type 2 DM with hyperglycemia)\nCPT: 99214 (Established patient office visit, moderate complexity)"
    icd_cpt_input = st.text_area("ICD-10/CPT Codes", icd_cpt_suggestions)

    try:
        sanitized_soap = sanitize_text(soap_note)
        pdf_bytes = export_to_pdf(ehr_data, sanitized_soap, icd_cpt_input)
        st.download_button("Download PDF", pdf_bytes, file_name="SOAP_Note.pdf", mime="application/pdf")
    except Exception as e:
        st.error(f"Error generating PDF: {str(e)}")
