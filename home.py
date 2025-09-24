import streamlit as st
import base64
import os
# --- NEW IMPORT ---
from rag_engine import generate_plan_with_rag

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Zypher Home",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- MOCK DATA ---
COURSE_DATA = {
    "Computer Science & Engineering": {
        3: ["Data Structures & Algorithms", "Discrete Mathematics", "Digital Logic Design", "Object Oriented Programming"],
        4: ["Database Management Systems", "Operating Systems", "Computer Networks", "Theory of Computation"],
        5: ["Artificial Intelligence", "Compiler Design", "Web Technologies", "Software Engineering"],
    },
    "Electrical Engineering": {
        3: ["Analog Circuits", "Digital Electronics", "Signals and Systems", "Electromagnetic Theory"],
        4: ["Power Systems I", "Control Systems", "Microprocessors & Microcontrollers", "Electrical Machines I"],
        5: ["Power Electronics", "Power Systems II", "Digital Signal Processing", "Communication Systems"],
    },
    "Mechanical Engineering": {
        3: ["Thermodynamics", "Fluid Mechanics", "Strength of Materials", "Theory of Machines"],
        4: ["Heat Transfer", "Manufacturing Processes", "Machine Design I", "Dynamics of Machinery"],
        5: ["Finite Element Analysis", "Mechatronics", "Machine Design II", "IC Engines"],
    },
    "Civil Engineering": {
        3: ["Surveying", "Building Materials", "Structural Analysis I", "Fluid Mechanics II"],
        4: ["Geotechnical Engineering", "Transportation Engineering", "Design of Concrete Structures I", "Hydrology"],
        5: ["Environmental Engineering", "Design of Steel Structures", "Foundation Engineering", "Water Resources Engineering"],
    },
    "Electronics & Communication Engg": {
        3: ["Electronic Devices", "Network Theory", "Digital System Design", "Signals & Systems"],
        4: ["Analog Communication", "Linear Integrated Circuits", "Microcontrollers", "Control System Engineering"],
        5: ["Digital Communication", "VLSI Design", "Microwave Engineering", "Information Theory & Coding"],
    }
}

INTERESTS_LIST = [
    "Machine Learning", "Artificial Intelligence", "Web Development", "Blockchain",
    "Cybersecurity", "Data Science", "Cloud Computing", "Robotics", "IoT",
    "Game Development", "Mobile App Development", "AR/VR"
]

# --- HELPER FUNCTION TO ENCODE IMAGE ---
def get_image_as_base64(file):
    if not os.path.exists(file):
        st.error(f"Logo file not found: {file}")
        return ""
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- STYLING ---
try:
    logo_base64 = get_image_as_base64("zypher.png")
except FileNotFoundError:
    logo_base64 = ""

page_styling = f"""
<style>
    /* --- General Page Styling --- */
    [data-testid="stAppViewContainer"] {{
        background-color: #c8e6c9;
        background-image: linear-gradient(180deg, #e0f7fa 0%, #c8e6c9 100%);
    }}

    /* --- Hide Streamlit UI --- */
    #MainMenu, footer, header {{
        visibility: hidden;
    }}
    
    /* --- NEW NAVIGATION BAR STYLING --- */
    .navbar {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 30px;
        background: rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        z-index: 1000;
        box-sizing: border-box;
    }}
    .navbar .logo-brand {{
        display: flex;
        align-items: center;
        gap: 15px;
    }}
    .navbar .logo-img {{
        width: 40px;
        height: 40px;
    }}
    .navbar .brand-name {{
        font-size: 1.5rem;
        font-weight: bold;
        color: #002e00;
        text-decoration: none;
    }}
    .navbar .nav-links a {{
        color: #004d00;
        text-decoration: none;
        margin: 0 15px;
        font-weight: 500;
        transition: color 0.3s;
    }}
    .navbar .nav-links a.active, .navbar .nav-links a:hover {{
        color: #002e00;
        font-weight: 600;
    }}
    
    /* --- Main Content Container (Adjusted for Navbar) --- */
    .main-container {{
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        padding: 80px 2rem 2rem 2rem;
        color: #002e00;
    }}

    /* --- Glass Card for the Form --- */
    .form-card {{
        background: rgba(255, 255, 255, 0.45);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
        padding: 30px;
        width: 100%;
        max-width: 700px;
        text-align: left;
    }}

    h1 {{
        font-size: 2.2rem;
        margin-bottom: 5px;
        color: #002e00 !important;
    }}

    p.subtitle {{
        font-size: 1.1rem;
        margin-bottom: 25px;
        color: #004d00;
    }}

    /* --- Styling Streamlit Widgets for HIGH CONTRAST --- */
    label[data-baseweb="form-control-label"] {{
        color: #002e00 !important;
        font-weight: 600 !important;
        text-align: left;
    }}
    div[data-baseweb="select"] > div:first-child,
    div[data-baseweb="multiselect"] > div:first-child {{
        background-color: #FFFFFF !important;
        border: 1px solid rgba(0, 0, 0, 0.2) !important;
        border-radius: 8px !important;
        color: #002e00 !important;
    }}
    div[data-baseweb="select"] input,
    div[data-baseweb="multiselect"] input {{
        color: #002e00 !important; 
    }}
    [data-testid="stRadio"] label {{
        padding: 5px 15px;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.8);
        margin: 0 5px;
        transition: background-color 0.3s;
        color: #004d00;
        border: 1px solid rgba(0, 0, 0, 0.2);
    }}
    [data-testid="stRadio"] label:has(input:checked) {{
        background-color: #4CAF50;
        color: white;
        border: 1px solid #4CAF50;
    }}
    [data-testid="stFormSubmitButton"] button {{
        width: 100%;
        padding: 15px;
        border: none;
        border-radius: 10px;
        background-color: #4CAF50;
        color: white;
        font-size: 1.2rem;
        font-weight: bold;
        cursor: pointer;
        transition: background-color 0.3s;
        margin-top: 20px;
    }}
    [data-testid="stFormSubmitButton"] button:hover {{
        background-color: #45a049;
    }}
</style>
"""
st.markdown(page_styling, unsafe_allow_html=True)


# --- PAGE LAYOUT ---

# --- NEW NAVIGATION BAR ---
logo_html = f'<img src="data:image/png;base64,{logo_base64}" class="logo-img">' if logo_base64 else ''
st.markdown(f"""
    <div class="navbar">
        <div class="logo-brand">
            {logo_html}
            <a href="#" class="brand-name">Zypher</a>
        </div>
        <div class="nav-links">
            <a href="#" class="active">Home</a>
            <a href="#">My Plan</a>
            <a href="#">Profile</a>
        </div>
    </div>
""", unsafe_allow_html=True)


# --- MAIN CONTENT ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<div class="form-card">', unsafe_allow_html=True)

st.markdown('<h1>Build Your Path</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Tell us about your academic journey and passions.</p>', unsafe_allow_html=True)


# --- FORM ---
with st.form("user_details_form"):
    course = st.selectbox(
        "📚 Select Your Course",
        options=list(COURSE_DATA.keys()),
        index=None,
        placeholder="Choose your field of study"
    )
    semester = st.radio(
        "🗓️ Select Your Current Semester",
        options=[3, 4, 5],
        horizontal=True
    )
    st.markdown("<br>", unsafe_allow_html=True)
    subjects = []
    if course and semester:
        subjects = st.multiselect(
            "✍️ Select Your Subjects for this Semester",
            options=COURSE_DATA[course].get(semester, []),
            placeholder="Choose your subjects from the list"
        )
    else:
        st.info("Please select a course and semester to see your subjects.")
    interests = st.multiselect(
        "💡 What are your interests?",
        options=INTERESTS_LIST,
        placeholder="Select skills you want to learn (e.g., AI, Web Dev)"
    )
    submitted = st.form_submit_button("Generate My Plan")


# --- POST-SUBMISSION LOGIC ---
if submitted:
    if not course or not semester or not subjects or not interests:
        st.warning("Please fill out all the fields to generate your plan!")
    else:
        st.success("Great! Here's the information we've gathered:")
        st.balloons()
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Your Academics")
            st.write(f"**Course:** {course}")
            st.write(f"**Semester:** {semester}")
            st.write("**Subjects:**")
            for subject in subjects:
                st.write(f"- {subject}")
        with col2:
            st.subheader("Your Interests")
            st.write("**Skills to Develop:**")
            for interest in interests:
                st.write(f"- {interest}")
        
        st.info("Next, we'll use this to create your personalized learning roadmap!")
        
        # --- RAG + AGENTIC AI LOGIC ---
        with st.spinner("Talking to the AI..."):
            try:
                # Call your new function to generate the plan
                learning_plan = generate_plan_with_rag(course, semester, subjects, interests)
                
                # Store the generated plan in session state
                st.session_state.plan = learning_plan
                
                st.balloons()
                st.success("Plan generated successfully!")
                st.switch_page("pages/plan.py") # <-- THIS IS THE CORRECTED LINE
            except Exception as e:
                st.error(f"An error occurred: {e}. Please try again.")

st.markdown('</div>', unsafe_allow_html=True) # Close form-card
st.markdown('</div>', unsafe_allow_html=True) # Close main-container
