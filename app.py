import streamlit as st
import time
import base64
from PIL import Image
import io
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Clinical Documentation Assistant",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for animations and styling
st.markdown("""
<style>
    /* Gradient background and overall styling */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4edf5 100%);
    }
    
    /* Card styling */
    div.stButton > button {
        background: linear-gradient(90deg, #3a7bd5, #00d2ff);
        color: white;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        border: none;
        box-shadow: 0 4px 6px rgba(50, 50, 93, 0.11), 0 1px 3px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 7px 14px rgba(50, 50, 93, 0.1), 0 3px 6px rgba(0, 0, 0, 0.08);
    }
    
    /* Input field styling */
    div.stTextInput > div > div > input {
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        padding: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    div.stTextInput > div > div > input:focus {
        border-color: #3a7bd5;
        box-shadow: 0 0 0 2px rgba(58, 123, 213, 0.2);
    }
    
    /* Text area styling */
    div.stTextArea > div > div > textarea {
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        padding: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    /* Animation classes */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translate3d(0, 20px, 0);
        }
        to {
            opacity: 1;
            transform: translate3d(0, 0, 0);
        }
    }
    
    .animate-fadeInUp {
        animation: fadeInUp 0.5s ease forwards;
    }
    
    /* Delay classes for staggered animations */
    .delay-1 { animation-delay: 0.1s; opacity: 0; }
    .delay-2 { animation-delay: 0.2s; opacity: 0; }
    .delay-3 { animation-delay: 0.3s; opacity: 0; }
    .delay-4 { animation-delay: 0.4s; opacity: 0; }
    .delay-5 { animation-delay: 0.5s; opacity: 0; }
    .delay-6 { animation-delay: 0.6s; opacity: 0; }
    .delay-7 { animation-delay: 0.7s; opacity: 0; }
    .delay-8 { animation-delay: 0.8s; opacity: 0; }
    .delay-9 { animation-delay: 0.9s; opacity: 0; }
    .delay-10 { animation-delay: 1.0s; opacity: 0; }
    
    /* Section styling */
    .section-container {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    /* Header styling */
    .header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Success animation */
    @keyframes successPulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .success-animation {
        animation: successPulse 0.5s ease-in-out;
    }
    
    /* Custom label styling */
    .custom-label {
        font-weight: 600;
        color: #555;
        margin-bottom: 5px;
        font-size: 0.9rem;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div {
        background-color: #3a7bd5;
    }
    
    /* Icon container */
    .icon-container {
        display: flex;
        justify-content: center;
        margin-bottom: 1rem;
    }
    
    /* Pulse animation for the icon */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
</style>
""", unsafe_allow_html=True)

# Function to create animated containers with delay
def animated_container(content, delay_class):
    return st.markdown(f"""
    <div class="animate-fadeInUp {delay_class}">
        {content}
    </div>
    """, unsafe_allow_html=True)

# Function to encode image to base64
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Helper function to simulate loading
def simulate_processing():
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress_bar.progress(i + 1)
    st.success("✅ Processing complete!")
    time.sleep(1)
    progress_bar.empty()

# Medical bot SVG icon (embedded directly)
medical_bot_svg = """
<svg width="120" height="120" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="60" cy="40" r="25" fill="#3a7bd5" />
    <rect x="35" y="65" width="50" height="30" rx="5" fill="#3a7bd5" />
    <circle cx="45" cy="40" r="5" fill="white" />
    <circle cx="75" cy="40" r="5" fill="white" />
    <path d="M50 50 Q60 60 70 50" stroke="white" stroke-width="3" />
    <rect x="50" y="20" width="20" height="5" rx="2.5" fill="#ff5757" />
    <rect x="57.5" y="12.5" width="5" height="20" rx="2.5" fill="#ff5757" />
    <rect x="25" y="95" width="10" height="20" rx="5" fill="#3a7bd5" />
    <rect x="85" y="95" width="10" height="20" rx="5" fill="#3a7bd5" />
</svg>
"""

# Display header with animated icon
st.markdown(f"""
<div class="header animate-fadeInUp">
    <div class="icon-container pulse">
        {medical_bot_svg}
    </div>
    <h1>Clinical Documentation Assistant</h1>
    <p style="color: #666; font-size: 1.1rem;">Streamline your medical documentation workflow</p>
</div>
""", unsafe_allow_html=True)

# Create tabs for a multi-step process
tabs = st.tabs(["Patient Info", "Vitals & Labs", "Generate Note"])

# Tab 1: Patient Information
with tabs[0]:
    st.markdown('<div class="section-container animate-fadeInUp delay-1">', unsafe_allow_html=True)
    st.subheader("Patient Details")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="custom-label">Patient ID</div>', unsafe_allow_html=True)
        patient_id = st.text_input("", value="2031125", key="patient_id", label_visibility="collapsed")
    
    with col2:
        st.markdown('<div class="custom-label">Visit Date</div>', unsafe_allow_html=True)
        visit_date = st.date_input("", label_visibility="collapsed")
    
    st.markdown('<div class="custom-label animate-fadeInUp delay-2">Chief Complaint</div>', unsafe_allow_html=True)
    chief_complaint = st.text_input("", value="Shortness of breath", key="chief_complaint", label_visibility="collapsed")
    
    st.markdown('<div class="custom-label animate-fadeInUp delay-3">Conditions (comma-separated)</div>', unsafe_allow_html=True)
    conditions = st.text_area("", value="Hypertension, Diabetes", height=100, key="conditions", label_visibility="collapsed")
    
    st.markdown('<div class="custom-label animate-fadeInUp delay-4">Medications (comma-separated)</div>', unsafe_allow_html=True)
    medications = st.text_area("", value="Metformin, Lisinopril", height=100, key="medications", label_visibility="collapsed")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Next button with animation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Next: Vitals & Labs", key="next_to_vitals"):
            tabs[1].selectbox = True

# Tab 2: Vitals and Labs
with tabs[1]:
    st.markdown('<div class="section-container animate-fadeInUp delay-1">', unsafe_allow_html=True)
    st.subheader("Vitals & Laboratory Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="custom-label">Blood Pressure (mmHg)</div>', unsafe_allow_html=True)
        bp = st.text_input("", value="150/90", key="bp", label_visibility="collapsed")
        
        st.markdown('<div class="custom-label">Heart Rate (bpm)</div>', unsafe_allow_html=True)
        hr = st.text_input("", value="98", key="hr", label_visibility="collapsed")
        
        st.markdown('<div class="custom-label">Temperature (°F)</div>', unsafe_allow_html=True)
        temp = st.text_input("", value="98.6", key="temp", label_visibility="collapsed")
    
    with col2:
        st.markdown('<div class="custom-label">SpO2 (%)</div>', unsafe_allow_html=True)
        spo2 = st.text_input("", value="91%", key="spo2", label_visibility="collapsed")
        
        st.markdown('<div class="custom-label">HbA1c (%)</div>', unsafe_allow_html=True)
        hba1c = st.text_input("", value="8.2%", key="hba1c", label_visibility="collapsed")
        
        st.markdown('<div class="custom-label">CBC</div>', unsafe_allow_html=True)
        cbc = st.text_input("", value="Normal", key="cbc", label_visibility="collapsed")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Lab results visualization (simple example)
    st.markdown('<div class="section-container animate-fadeInUp delay-3">', unsafe_allow_html=True)
    st.subheader("Lab Trends")
    
    # Sample data for demonstration
    chart_data = pd.DataFrame({
        'Date': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
        'HbA1c': [8.5, 8.4, 8.3, 8.2, 8.2],
        'Glucose': [180, 175, 165, 160, 155]
    })
    
    st.line_chart(chart_data.set_index('Date'))
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Back to Patient Info", key="back_to_patient"):
            tabs[0].selectbox = True
    with col3:
        if st.button("Next: Generate Note", key="next_to_generate"):
            tabs[2].selectbox = True

# Tab 3: Generate SOAP Note
with tabs[2]:
    st.markdown('<div class="section-container animate-fadeInUp delay-1">', unsafe_allow_html=True)
    st.subheader("Generate SOAP Note")
    
    note_type = st.selectbox("Note Type", ["SOAP Note", "Progress Note", "Discharge Summary", "Consultation"])
    
    # Additional context options
    st.markdown('<div class="custom-label animate-fadeInUp delay-2">Additional Context (optional)</div>', unsafe_allow_html=True)
    additional_context = st.text_area("", height=100, label_visibility="collapsed")
    
    # Generate button with animation
    if st.button("Generate Note", key="generate_note"):
        with st.spinner("Generating comprehensive medical note..."):
            simulate_processing()
        
        # Display generated note with animation
        st.markdown('<div class="section-container animate-fadeInUp success-animation">', unsafe_allow_html=True)
        st.subheader("Generated SOAP Note")
        
        soap_note = f"""
        # SOAP Note
        **Date:** {time.strftime("%Y-%m-%d")}
        **Patient ID:** {patient_id}
        
        ## Subjective
        Patient presents with chief complaint of shortness of breath. Patient has a history of hypertension and diabetes. Currently on Metformin and Lisinopril.
        
        ## Objective
        **Vitals:**
        - BP: {bp}
        - HR: {hr} bpm
        - SpO2: {spo2}
        - Temperature: 98.6°F
        
        **Labs:**
        - HbA1c: {hba1c}
        - CBC: {cbc}
        
        ## Assessment
        1. Shortness of breath - likely due to poor glycemic control and possible early CHF
        2. Hypertension - poorly controlled
        3. Diabetes Type 2 - suboptimal control
        
        ## Plan
        1. Increase Lisinopril to 20mg daily
        2. Add Furosemide 20mg daily
        3. Adjust Metformin dosage
        4. Schedule follow-up in 2 weeks
        5. Order echocardiogram
        """
        
        st.markdown(soap_note)
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="Download Note",
                data=soap_note,
                file_name="soap_note.md",
                mime="text/markdown"
            )
        with col2:
            if st.button("Copy to Clipboard", key="copy_note"):
                st.success("Note copied to clipboard!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Back button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Back to Vitals & Labs", key="back_to_vitals"):
            tabs[1].selectbox = True

# Footer with animation
st.markdown("""
<div class="animate-fadeInUp delay-10" style="text-align: center; margin-top: 2rem; padding: 1rem; color: #666;">
    <p>© 2023 Clinical Documentation Assistant | Powered by AI</p>
</div>
""", unsafe_allow_html=True)
