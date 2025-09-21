import streamlit as st
import base64

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Zypher Home",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- MOCK DATA ---
# In a real app, this would come from a database.
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
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- STYLING ---
# Using the same styling as the login page for consistency
# Make sure your logo is accessible at the path "../zypher.png" if this file is in a 'pages' folder
try:
    logo_base64 = get_image_as_base64("../zypher.png")
except FileNotFoundError:
    # Fallback if the image is in the same directory (for standalone running)
    try:
        logo_base64 = get_image_as_base64("zypher.png")
    except FileNotFoundError:
        logo_base64 = "" # Set a default empty string if no logo is found


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
    
    /* --- Main Content Container --- */
    .main-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 2rem;
        color: #002e00; /* Darker base text color for better contrast */
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
        text-align: center;
    }}
    
    .logo {{
        width: 80px;
        margin-bottom: 10px;
    }}

    h1 {{
        font-size: 2.2rem;
        margin-bottom: 5px;
        color: #12420B !important; /* Dark green for main title */
    }}

    p.subtitle {{
        font-size: 1.1rem;
        margin-bottom: 25px;
        color: #004d00; /* A strong, readable green */
    }}

    /* --- Styling Streamlit Widgets for HIGH CONTRAST --- */

    /* Style for widget labels (e.g., "Select Your Course") */
    label[data-baseweb="form-control-label"] {{
        color: #002e00 !important;
        font-weight: 600 !important;
        text-align: left;
    }}
    
    /* --- Selectbox & Multiselect --- */
    div[data-baseweb="select"] > div:first-child,
    div[data-baseweb="multiselect"] > div:first-child {{
        background-color: #FFFFFF !important;
        border: 1px solid rgba(0, 0, 0, 0.2) !important;
        border-radius: 8px !important;
        color: #002e00 !important; /* Dark text for input */
    }}
    /* Ensure text typed is dark */
    div[data-baseweb="select"] input,
    div[data-baseweb="multiselect"] input {{
        color: #002e00 !important; 
    }}
    
    /* --- Radio buttons --- */
    [data-testid="stRadio"] label {{
        padding: 5px 15px;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.8);
        margin: 0 5px;
        transition: background-color 0.3s;
        color: #004d00; /* Dark green text for unselected options */
        border: 1px solid rgba(0, 0, 0, 0.2);
    }}
    /* Style for selected radio button */
    [data-testid="stRadio"] label:has(input:checked) {{
        background-color: #4CAF50; /* A standard, high-contrast green */
        color: white;
        border: 1px solid #4CAF50;
    }}

    /* --- Form Submit Button --- */
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
st.markdown(f'<div class="main-container">', unsafe_allow_html=True)
st.markdown(f'<div class="form-card">', unsafe_allow_html=True)

if logo_base64:
    st.markdown(f'<img src="data:image/png;base64,{logo_base64}" alt="Zypher Logo" class="logo">', unsafe_allow_html=True)

st.markdown('<h1>Build Your Path</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Tell us about your academic journey and passions.</p>', unsafe_allow_html=True)


# --- FORM ---
with st.form("user_details_form"):
    # --- Course and Semester Selection ---
    course = st.selectbox(
        "📚 Select Your Course",
        options=list(COURSE_DATA.keys()),
        index=None,
        placeholder="Choose your field of study"
    )

    semester = st.radio(
        "🗓️ Select Your Current Semester",
        options=[3, 4, 5], # Example semesters
        horizontal=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True) # Spacer

    # --- Dynamic Subject Selection ---
    subjects = []
    if course and semester:
        subjects = st.multiselect(
            "✍️ Select Your Subjects for this Semester",
            options=COURSE_DATA[course].get(semester, []),
            placeholder="Choose your subjects from the list"
        )
    else:
        st.info("Please select a course and semester to see your subjects.")

    # --- Interests Selection ---
    interests = st.multiselect(
        "💡 What are your interests?",
        options=INTERESTS_LIST,
        placeholder="Select skills you want to learn (e.g., AI, Web Dev)"
    )

    # --- Submit Button ---
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

st.markdown('</div>', unsafe_allow_html=True) # Close form-card
st.markdown('</div>', unsafe_allow_html=True) # Close main-container