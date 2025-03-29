import streamlit as st
import time
import pandas as pd
import altair as alt

# Page configuration
st.set_page_config(
    page_title="Clinical Documentation Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for animations and styling
st.markdown("""
<style>
    /* Gradient header */
    .main-header {
        background: linear-gradient(90deg, #3a8dde 0%, #5e60ce 100%);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem !important;
        font-weight: 700;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Card styling */
    .stCard {
        border-radius: 12px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.1);
        padding: 1.5rem;
        margin-bottom: 1rem;
        background: white;
    }
    
    /* Section headers */
    .section-header {
        color: #3a8dde;
        font-size: 1.2rem;
        font-weight: 600;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    /* Progress indicator */
    .progress-indicator {
        display: flex;
        justify-content: space-between;
        margin-bottom: 2rem;
    }
    .progress-step {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 20%;
    }
    .step-circle {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: #e0e0e0;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 0.5rem;
        color: white;
        font-weight: bold;
    }
    .step-circle.active {
        background: linear-gradient(90deg, #3a8dde 0%, #5e60ce 100%);
        box-shadow: 0 4px 10px rgba(94, 96, 206, 0.3);
    }
    .step-line {
        height: 3px;
        background-color: #e0e0e0;
        flex-grow: 1;
        margin-top: 20px;
    }
    .step-line.active {
        background: linear-gradient(90deg, #3a8dde 0%, #5e60ce 100%);
    }
    .step-label {
        text-align: center;
        font-size: 0.8rem;
        color: #666;
    }
    .step-label.active {
        color: #3a8dde;
        font-weight: 600;
    }
    
    /* Vital signs styling */
    .vital-container {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    .vital-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        flex: 1;
        min-width: 150px;
    }
    .vital-title {
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    .vital-value {
        color: #3a8dde;
        font-size: 1.5rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("Clinical Assistant")
    
    # Simple navigation instead of option_menu
    selected = st.radio(
        "Navigation",
        ["Patient Info", "Vitals", "Assessment", "Plan", "Generate Note"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### Recent Patients")
    
    recent_patients = [
        {"id": "2035125", "name": "John Smith", "age": 45},
        {"id": "2035124", "name": "Maria Garcia", "age": 62},
        {"id": "2035123", "name": "David Chen", "age": 38}
    ]
    
    for patient in recent_patients:
        st.markdown(f"""
        <div style='padding: 0.5rem; border-radius: 8px; margin-bottom: 0.5rem; background-color: white; box-shadow: 0 2px 5px rgba(0,0,0,0.05);'>
            <div style='font-weight: 600; color: #333;'>{patient["name"]}</div>
            <div style='font-size: 0.8rem; color: #666;'>ID: {patient["id"]} | Age: {patient["age"]}</div>
        </div>
        """, unsafe_allow_html=True)

# Main content
st.markdown("<h1 class='main-header'>Clinical Documentation Assistant</h1>", unsafe_allow_html=True)

# Progress steps
current_step = {"Patient Info": 1, "Vitals": 2, "Assessment": 3, "Plan": 4, "Generate Note": 5}[selected]

st.markdown("""
<div class='progress-indicator'>
    <div class='progress-step'>
        <div class='step-circle active'>1</div>
        <div class='step-label active'>Patient Info</div>
    </div>
    <div class='step-line active'></div>
    <div class='progress-step'>
        <div class='step-circle {}''>2</div>
        <div class='step-label {}'>Vitals</div>
    </div>
    <div class='step-line {}'></div>
    <div class='progress-step'>
        <div class='step-circle {}'>3</div>
        <div class='step-label {}'>Assessment</div>
    </div>
    <div class='step-line {}'></div>
    <div class='progress-step'>
        <div class='step-circle {}'>4</div>
        <div class='step-label {}'>Plan</div>
    </div>
    <div class='step-line {}'></div>
    <div class='progress-step'>
        <div class='step-circle {}'>5</div>
        <div class='step-label {}'>Generate</div>
    </div>
</div>
""".format(
    'active' if current_step >= 2 else '', 
    'active' if current_step >= 2 else '',
    'active' if current_step >= 2 else '',
    'active' if current_step >= 3 else '',
    'active' if current_step >= 3 else '',
    'active' if current_step >= 3 else '',
    'active' if current_step >= 4 else '',
    'active' if current_step >= 4 else '',
    'active' if current_step >= 4 else '',
    'active' if current_step >= 5 else '',
    'active' if current_step >= 5 else ''
), unsafe_allow_html=True)

# Patient Info Section
if selected == "Patient Info":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.markdown("<h3 class='section-header'>Patient Demographics</h3>", unsafe_allow_html=True)
        
        patient_id = st.text_input("Patient ID", value="2035125")
        
        col_a, col_b = st.columns(2)
        with col_a:
            patient_name = st.text_input("Patient Name", value="John Smith")
            dob = st.date_input("Date of Birth", value=pd.to_datetime("1978-05-15"))
        with col_b:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            contact = st.text_input("Contact Number", value="(555) 123-4567")
        
        st.markdown("<h3 class='section-header'>Insurance Information</h3>", unsafe_allow_html=True)
        insurance = st.selectbox("Insurance Provider", ["Medicare", "Blue Cross", "Aetna", "UnitedHealthcare", "Other"])
        policy_number = st.text_input("Policy Number", value="MED12345678")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.markdown("<h3 class='section-header'>Quick Actions</h3>", unsafe_allow_html=True)
        st.button("View Patient History")
        st.button("Check Allergies")
        st.button("Medication Review")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.markdown("<h3 class='section-header'>Visit Information</h3>", unsafe_allow_html=True)
        visit_date = st.date_input("Visit Date", value=pd.to_datetime("today"))
        visit_type = st.selectbox("Visit Type", ["Follow-up", "New Patient", "Urgent Care", "Annual Physical"])
        provider = st.selectbox("Provider", ["Dr. Sarah Johnson", "Dr. Michael Chen", "Dr. Emily Rodriguez"])
        st.markdown("</div>", unsafe_allow_html=True)

# Vitals Section
elif selected == "Vitals":
    st.markdown("<div class='stCard'>", unsafe_allow_html=True)
    st.markdown("<h3 class='section-header'>Vital Signs</h3>", unsafe_allow_html=True)
    
    st.markdown("<div class='vital-container'>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("<div class='vital-card'>", unsafe_allow_html=True)
        st.markdown("<div class='vital-title'>Blood Pressure</div>", unsafe_allow_html=True)
        bp_sys = st.number_input("Systolic", value=150, min_value=60, max_value=250, step=1, label_visibility="collapsed")
        bp_dia = st.number_input("Diastolic", value=90, min_value=40, max_value=180, step=1, label_visibility="collapsed")
        st.markdown(f"<div class='vital-value'>{bp_sys}/{bp_dia}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='vital-card'>", unsafe_allow_html=True)
        st.markdown("<div class='vital-title'>Heart Rate</div>", unsafe_allow_html=True)
        hr = st.number_input("Heart Rate", value=98, min_value=30, max_value=220, step=1, label_visibility="collapsed")
        st.markdown(f"<div class='vital-value'>{hr} bpm</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='vital-card'>", unsafe_allow_html=True)
        st.markdown("<div class='vital-title'>SpO2</div>", unsafe_allow_html=True)
        spo2 = st.number_input("SpO2", value=91, min_value=70, max_value=100, step=1, label_visibility="collapsed")
        st.markdown(f"<div class='vital-value'>{spo2}%</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col4:
        st.markdown("<div class='vital-card'>", unsafe_allow_html=True)
        st.markdown("<div class='vital-title'>Temperature</div>", unsafe_allow_html=True)
        temp = st.number_input("Temperature", value=98.6, min_value=94.0, max_value=105.0, step=0.1, format="%.1f", label_visibility="collapsed")
        st.markdown(f"<div class='vital-value'>{temp}°F</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h3 class='section-header'>Additional Measurements</h3>", unsafe_allow_html=True)
        height = st.number_input("Height (cm)", value=175, min_value=50, max_value=250)
        weight = st.number_input("Weight (kg)", value=82, min_value=20, max_value=250)
        bmi = round(weight / ((height/100) ** 2), 1)
        st.info(f"BMI: {bmi} - {'Normal' if 18.5 <= bmi <= 24.9 else 'Overweight' if 25 <= bmi <= 29.9 else 'Obese' if bmi >= 30 else 'Underweight'}")
    
    with col2:
        st.markdown("<h3 class='section-header'>Lab Results</h3>", unsafe_allow_html=True)
        hba1c = st.number_input("HbA1c (%)", value=8.2, min_value=4.0, max_value=15.0, step=0.1, format="%.1f")
        glucose = st.number_input("Glucose (mg/dL)", value=145, min_value=50, max_value=500)
        
        # Simple chart for glucose trend
        glucose_data = pd.DataFrame({
            'Date': pd.date_range(end=pd.Timestamp.today(), periods=5, freq='M'),
            'Glucose': [132, 140, 138, 142, 145]
        })
        
        chart = alt.Chart(glucose_data).mark_line(point=True).encode(
            x=alt.X('Date:T', title='Date'),
            y=alt.Y('Glucose:Q', title='Glucose (mg/dL)', scale=alt.Scale(domain=[100, 160])),
            tooltip=['Date:T', 'Glucose:Q']
        ).properties(
            title='Glucose Trend',
            width=300,
            height=200
        )
        
        st.altair_chart(chart)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Assessment Section
elif selected == "Assessment":
    st.markdown("<div class='stCard'>", unsafe_allow_html=True)
    st.markdown("<h3 class='section-header'>Chief Complaint</h3>", unsafe_allow_html=True)
    chief_complaint = st.text_area("Chief Complaint", value="Shortness of breath", height=80)
    
    st.markdown("<h3 class='section-header'>History of Present Illness</h3>", unsafe_allow_html=True)
    hpi = st.text_area("History of Present Illness", value="Patient reports progressive shortness of breath over the past 3 days, worse with exertion. Denies chest pain, fever, or cough. Has history of COPD and recent medication non-compliance.", height=150)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h3 class='section-header'>Past Medical History</h3>", unsafe_allow_html=True)
        conditions = st.text_area("Conditions (comma-separated)", value="Hypertension, Diabetes, COPD", height=100)
        
        st.markdown("<h3 class='section-header'>Allergies</h3>", unsafe_allow_html=True)
        allergies = st.text_area("Allergies (comma-separated)", value="Penicillin (hives), Sulfa drugs", height=80)
    
    with col2:
        st.markdown("<h3 class='section-header'>Current Medications</h3>", unsafe_allow_html=True)
        medications = st.text_area("Medications (comma-separated)", value="Metformin, Lisinopril, Albuterol inhaler", height=100)
        
        st.markdown("<h3 class='section-header'>Social History</h3>", unsafe_allow_html=True)
        social = st.text_area("Social History", value="Former smoker (quit 5 years ago, 30 pack-year history). Occasional alcohol use. Lives alone.", height=80)
    
    st.markdown("<h3 class='section-header'>Physical Examination</h3>", unsafe_allow_html=True)
    exam = st.text_area("Physical Examination", value="General: Alert and oriented, mild respiratory distress\nLungs: Decreased breath sounds bilaterally, with expiratory wheezing\nCardiovascular: Regular rate and rhythm, no murmurs\nExtremities: Trace bilateral lower extremity edema", height=150)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Plan Section
elif selected == "Plan":
    st.markdown("<div class='stCard'>", unsafe_allow_html=True)
    st.markdown("<h3 class='section-header'>Assessment</h3>", unsafe_allow_html=True)
    
    # AI-assisted diagnosis suggestions
    st.info("AI Suggestions: Based on symptoms and history, consider COPD exacerbation, CHF, or pneumonia")
    
    diagnosis = st.text_area("Assessment/Diagnosis", value="1. COPD exacerbation - likely due to medication non-compliance\n2. Uncontrolled Type 2 Diabetes\n3. Hypertension - well controlled on current regimen", height=120)
    
    st.markdown("<h3 class='section-header'>Plan</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h4 style='color: #5e60ce; font-size: 1rem;'>Medications</h4>", unsafe_allow_html=True)
        
        meds = [
            "Continue Lisinopril 10mg daily",
            "Continue Metformin 1000mg BID",
            "Add Prednisone 40mg daily x 5 days",
            "Add Azithromycin 500mg day 1, then 250mg daily x 4 days"
        ]
        
        for med in meds:
            st.markdown(f"<div style='background: #f8f9fa; padding: 10px; border-radius: 8px; margin-bottom: 10px;'>{med}</div>", unsafe_allow_html=True)
        
        new_med = st.text_input("Add medication")
        st.button("+ Add to Plan")
    
    with col2:
        st.markdown("<h4 style='color: #5e60ce; font-size: 1rem;'>Tests & Procedures</h4>", unsafe_allow_html=True)
        
        tests = [
            "Chest X-ray",
            "Complete Blood Count",
            "Basic Metabolic Panel",
            "HbA1c"
        ]
        
        for test in tests:
            st.checkbox(test, value=True)
        
        st.text_input("Add test/procedure")
        st.button("+ Add Test")
    
    st.markdown("<h4 style='color: #5e60ce; font-size: 1rem;'>Patient Instructions</h4>", unsafe_allow_html=True)
    instructions = st.text_area("Instructions", value="1. Take all medications as prescribed\n2. Use rescue inhaler as needed for shortness of breath\n3. Follow up in 1 week\n4. Return to ED if symptoms worsen\n5. Continue to monitor blood glucose daily", height=120)
    
    st.markdown("<h4 style='color: #5e60ce; font-size: 1rem;'>Follow-up</h4>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        follow_up_time = st.selectbox("Follow-up in", ["3 days", "1 week", "2 weeks", "1 month", "3 months"])
    with col_b:
        follow_up_with = st.selectbox("Follow-up with", ["Primary Care", "Pulmonology", "Endocrinology", "Cardiology"])
    
    st.markdown("</div>", unsafe_allow_html=True)

# Generate Note Section
elif selected == "Generate Note":
    st.markdown("<div class='stCard'>", unsafe_allow_html=True)
    st.markdown("<h3 class='section-header'>Generate Clinical Note</h3>", unsafe_allow_html=True)
    
    note_type = st.selectbox("Note Type", ["SOAP Note", "Progress Note", "Discharge Summary", "Referral Letter"])
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("<div style='background: #f8f9fa; padding: 15px; border-radius: 8px; height: 400px; overflow-y: auto;'>", unsafe_allow_html=True)
        
        if st.button("Generate Note"):
            with st.spinner("Generating comprehensive clinical note..."):
                time.sleep(2)  # Simulate processing time
                
                st.markdown("""
                <h3 style='color: #3a8dde;'>SOAP Note</h3>
                
                <h4 style='color: #5e60ce;'>Subjective:</h4>
                <p>John Smith is a 45-year-old male presenting with shortness of breath for the past 3 days. The shortness of breath is worse with exertion and has been progressively worsening. Patient denies chest pain, fever, or cough. Patient reports medication non-compliance with his COPD medications over the past week due to financial constraints. He has a history of COPD, hypertension, and type 2 diabetes.</p>
                
                <h4 style='color: #5e60ce;'>Objective:</h4>
                <p><strong>Vitals:</strong> BP 150/90, HR 98, RR 22, Temp 98.6°F, SpO2 91% on room air</p>
                <p><strong>Physical Exam:</strong> General: Alert and oriented, in mild respiratory distress. Lungs: Decreased breath sounds bilaterally, with expiratory wheezing. Cardiovascular: Regular rate and rhythm, no murmurs. Extremities: Trace bilateral lower extremity edema.</p>
                <p><strong>Labs:</strong> HbA1c 8.2%, indicating poor glycemic control.</p>
                
                <h4 style='color: #5e60ce;'>Assessment:</h4>
                <p>1. COPD exacerbation - likely due to medication non-compliance</p>
                <p>2. Uncontrolled Type 2 Diabetes</p>
                <p>3. Hypertension - well controlled on current regimen</p>
                
                <h4 style='color: #5e60ce;'>Plan:</h4>
                <p><strong>Medications:</strong></p>
                <ul>
                    <li>Continue Lisinopril 10mg daily</li>
                    <li>Continue Metformin 1000mg BID</li>
                    <li>Add Prednisone 40mg daily x 5 days</li>
                    <li>Add Azithromycin 500mg day 1, then 250mg daily x 4 days</li>
                </ul>
                
                <p><strong>Tests:</strong> Chest X-ray, CBC, BMP, HbA1c</p>
                
                <p><strong>Instructions:</strong> Take all medications as prescribed. Use rescue inhaler as needed for shortness of breath. Follow up in 1 week. Return to ED if symptoms worsen. Continue to monitor blood glucose daily.</p>
                
                <p><strong>Follow-up:</strong> Follow up with Primary Care in 1 week. Consider Pulmonology referral if symptoms persist.</p>
                
                <p><strong>Provider:</strong> Dr. Sarah Johnson</p>
                """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("<h4 style='color: #5e60ce; font-size: 1rem;'>AI Assistance</h4>", unsafe_allow_html=True)
        st.markdown("""
        <div style='background: #f0f7ff; padding: 10px; border-radius: 8px; margin-bottom: 10px;'>
            <div style='font-size: 0.9rem;'>
                <strong>Suggestions:</strong><br>
                • Include medication reconciliation<br>
                • Add smoking cessation counseling<br>
                • Consider pulmonary function testing
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h4 style='color: #5e60ce; font-size: 1rem;'>Export Options</h4>", unsafe_allow_html=True)
        st.button("Export to EHR")
        st.button("Download as PDF")
        st.button("Share with Team")
        
        st.markdown("<h4 style='color: #5e60ce; font-size: 1rem;'>Templates</h4>", unsafe_allow_html=True)
        st.selectbox("Load Template", ["Default SOAP", "Detailed Assessment", "Brief Follow-up", "Specialist Referral"])
    
    st.markdown("</div>", unsafe_allow_html=True)
