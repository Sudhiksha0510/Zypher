import streamlit as st
import base64
from datetime import date, timedelta

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="My Progress",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- MOCK QUIZ DATA ---
# In a real app, this would come from a database
MOCK_QUIZ_DATA = {
    "Data Structures & Algorithms": 85,
    "Database Management Systems": 92,
    "Operating Systems": 78,
    "Web Technologies": 88,
}

# --- INITIALIZE SESSION STATE ---
if 'streak' not in st.session_state:
    st.session_state.streak = 0
if 'last_completed_date' not in st.session_state:
    st.session_state.last_completed_date = None

# --- HELPER FUNCTION TO ENCODE IMAGE ---
def get_image_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- STYLING ---
try:
    logo_base64 = get_image_as_base64("../zypher.png")
except FileNotFoundError:
    logo_base_64 = ""

page_styling = f"""
<style>
    /* General Page Styling & Navbar (same as other pages) */
    [data-testid="stAppViewContainer"] {{ background-image: linear-gradient(180deg, #e0f7fa 0%, #c8e6c9 100%); }}
    #MainMenu, footer, header {{ visibility: hidden; }}
    .navbar {{ position: fixed; top: 0; left: 0; width: 100%; display: flex; justify-content: space-between; align-items: center; padding: 10px 30px; background: rgba(255, 255, 255, 0.3); backdrop-filter: blur(10px); border-bottom: 1px solid rgba(255, 255, 255, 0.2); z-index: 1000; box-sizing: border-box; }}
    .navbar .logo-brand {{ display: flex; align-items: center; gap: 15px; }}
    .navbar .logo-img {{ width: 40px; height: 40px; }}
    .navbar .brand-name {{ font-size: 1.5rem; font-weight: bold; color: #002e00; text-decoration: none; }}
    .navbar .nav-links a {{ color: #004d00; text-decoration: none; margin: 0 15px; font-weight: 500; }}
    .navbar .nav-links a.active, .navbar .nav-links a:hover {{ color: #002e00; font-weight: 600; }}
    .profile-dropdown {{ position: relative; display: inline-block; }}
    .profile-dropdown:hover .dropdown-content {{ display: block; }}
    .dropdown-content {{ display: none; position: absolute; right: 0; background-color: rgba(255, 255, 255, 0.9); min-width: 200px; box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2); z-index: 1; border-radius: 10px; overflow: hidden; }}
    .main-container {{ padding: 80px 2rem 2rem 2rem; color: #002e00; }}

    /* --- STYLING FOR PROGRESS PAGE --- */
    .progress-grid {{
        display: grid;
        grid-template-columns: 1fr 1.5fr;
        gap: 30px;
        max-width: 1100px;
        margin: auto;
    }}
    .metric-card {{
        background: rgba(255, 255, 255, 0.45);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 25px;
        text-align: center;
    }}
    .metric-card h2 {{
        font-size: 1.5rem;
        color: #002e00;
        margin-bottom: 20px;
    }}
    .streak-number {{
        font-size: 5rem;
        font-weight: bold;
        color: #ff7043; /* Fire color for streak */
        line-height: 1;
    }}
    .streak-text {{
        font-size: 1.5rem;
        color: #004d00;
    }}

    /* --- UPDATED: Week View Styling --- */
    .week-view {{
        display: grid;
        grid-template-columns: repeat(7, 1fr); /* Creates 7 equal columns */
        gap: 8px;
        margin-top: 20px;
        text-align: center;
    }}
    .day-label {{
        padding: 8px 5px;
        border-radius: 8px;
        font-size: 0.9rem;
        font-weight: 500;
        color: #004d00;
        background-color: rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(0, 0, 0, 0.1);
    }}
    .day-label.completed {{
        background-color: #81c784; /* Green for completed */
        color: white;
        border: 1px solid #4caf50;
    }}
    
    /* Progress Bar Styling */
    [data-testid="stProgressBar"] > div > div {{
        background-image: linear-gradient(90deg, #66bb6a, #43a047);
    }}
    .subject-progress {{
        margin-bottom: 15px;
        text-align: left;
    }}
    .subject-progress label {{
        font-weight: 500;
        color: #004d00;
    }}
</style>
"""
st.markdown(page_styling, unsafe_allow_html=True)

# --- NAVIGATION BAR ---
logo_html = f'<img src="data:image/png;base64,{logo_base_64}" class="logo-img">' if logo_base_64 else ''
st.markdown(f"""
    <div class="navbar">
        <div class="logo-brand">{logo_html}<a href="#" class="brand-name">Zypher</a></div>
        <div class="nav-links">
            <a href="home">Home</a>
            <a href="plan">My Plan</a> 
            <a href="#" class="active">Progress</a> 
            <div class="profile-dropdown">
                <a href="#">Profile</a>
                <div class="dropdown-content">
                    <div class="user-info"><p>Sahasra</p></div>
                    <a href="#" class="signout-link">Sign Out</a>
                </div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- STREAK LOGIC ---
today = date.today()
yesterday = today - timedelta(days=1)
last_completed = st.session_state.last_completed_date

if last_completed != today:
    if last_completed != yesterday:
        st.session_state.streak = 0 # Reset streak if a day was missed

def mark_day_complete():
    today = date.today()
    if st.session_state.last_completed_date != today:
        if st.session_state.last_completed_date == today - timedelta(days=1):
            st.session_state.streak += 1
        else:
            st.session_state.streak = 1
        st.session_state.last_completed_date = today

# --- MAIN CONTENT ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<div class="progress-grid">', unsafe_allow_html=True)

# --- Left Column: Streak Tracker ---
with st.container():
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<h2>Daily Study Streak</h2>', unsafe_allow_html=True)
    st.markdown(f'<div class="streak-number">🔥{st.session_state.streak}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="streak-text">{"Day" if st.session_state.streak == 1 else "Days"}</div>', unsafe_allow_html=True)

    # --- UPDATED: Week visualization ---
    st.markdown('<div class="week-view">', unsafe_allow_html=True)
    start_of_week = today - timedelta(days=today.weekday()) # today.weekday() is 0 for Monday
    for i in range(7):
        day = start_of_week + timedelta(days=i)
        day_name = day.strftime("%A") # Get full day name e.g., "Monday"
        
        # Check if this day has been completed
        completed_class = "completed" if (st.session_state.last_completed_date and day <= st.session_state.last_completed_date and day <= today) else ""
        
        st.markdown(f'<div class="day-label {completed_class}">{day_name}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("I Studied Today!", use_container_width=True, on_click=mark_day_complete, disabled=(st.session_state.last_completed_date == today)):
        st.rerun() # Rerun to update the UI immediately
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- Right Column: Quiz Progress ---
with st.container():
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<h2>Quiz Performance</h2>', unsafe_allow_html=True)
    
    for subject, score in MOCK_QUIZ_DATA.items():
        st.markdown(f'<div class="subject-progress">', unsafe_allow_html=True)
        st.markdown(f"<label>{subject}: {score}%</label>", unsafe_allow_html=True)
        st.progress(score)
        st.markdown(f'</div>', unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)


st.markdown('</div>', unsafe_allow_html=True) # Close progress-grid
st.markdown('</div>', unsafe_allow_html=True) # Close main-container