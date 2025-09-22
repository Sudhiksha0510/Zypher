import streamlit as st
import base64

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="My Plan",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- HELPER FUNCTION TO ENCODE IMAGE ---
def get_image_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- STYLING (Copied from home.py for consistency) ---
try:
    logo_base64 = get_image_as_base64("../zypher.png")
except FileNotFoundError:
    logo_base64 = ""

# Note: This is the same styling block as home.py
page_styling = f"""
<style>
    /* General Page Styling & Navbar */
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
    .dropdown-content .user-info {{ padding: 15px; border-bottom: 1px solid rgba(0, 0, 0, 0.1); }}
    .dropdown-content a.signout-link {{ color: #004d00; padding: 12px 15px; text-decoration: none; display: block; }}
    
    /* Main Content Container */
    .main-container {{ padding: 80px 2rem 2rem 2rem; color: #002e00; }}
    
    /* Plan Display Styling */
    .plan-container {{
        background: rgba(255, 255, 255, 0.45);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 30px;
        width: 100%;
        max-width: 900px;
        margin: auto;
    }}
    .plan-title {{
        font-size: 2.2rem;
        font-weight: bold;
        color: #002e00;
        text-align: center;
        margin-bottom: 25px;
    }}
    div[data-testid="stExpander"] > div:first-child {{
        background-color: rgba(255, 255, 255, 0.6);
        border-radius: 10px;
        border: 1px solid rgba(0,0,0,0.1);
    }}
     div[data-testid="stExpander"] p {{
        font-size: 1.1rem !important;
        color: #004d00 !important;
     }}
     div[data-testid="stExpander"] h3 {{
        font-size: 1.25rem !important;
        color: #002e00 !important;
        margin-top: 15px;
        margin-bottom: 5px;
     }}
</style>
"""
st.markdown(page_styling, unsafe_allow_html=True)

# --- NAVIGATION BAR ---
logo_html = f'<img src="data:image/png;base64,{logo_base64}" class="logo-img">' if logo_base64 else ''
st.markdown(f"""
    <div class="navbar">
        <div class="logo-brand">{logo_html}<a href="#" class="brand-name">Zypher</a></div>
        <div class="nav-links">
            <a href="home">Home</a>
            <a href="#" class="active">My Plan</a> 
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

# --- MAIN CONTENT ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Check if the plan exists in the session state
if 'plan' in st.session_state and st.session_state.plan:
    plan = st.session_state.plan
    
    st.markdown('<div class="plan-container">', unsafe_allow_html=True)
    st.markdown(f'<h2 class="plan-title">{plan["title"]}</h2>', unsafe_allow_html=True)
    
    for week in plan["weeks"]:
        with st.expander(f"🗓️ Week {week['week']}: {week['title']}", expanded=week['week']==1):
            st.markdown(f"### 🎓 Academic Focus: {week['academic_focus']['title']}")
            st.markdown(f"<p>{week['academic_focus']['content']}</p>", unsafe_allow_html=True)
            st.markdown(f"**Resource:** [{week['academic_focus']['resource']['name']}]({week['academic_focus']['resource']['url']})")
            st.markdown("---")
            st.markdown(f"### 💡 Interest-Based Skill: {week['skill_focus']['title']}")
            st.markdown(f"<p>{week['skill_focus']['content']}</p>", unsafe_allow_html=True)
            st.markdown(f"**Resource:** [{week['skill_focus']['resource']['name']}]({week['skill_focus']['resource']['url']})")
            st.markdown("---")
            st.markdown(f"### 🎯 Actionable Task: {week['actionable_task']['title']}")
            st.markdown(f"<p>{week['actionable_task']['content']}</p>", unsafe_allow_html=True)
            st.markdown(f"**Resource:** [{week['actionable_task']['resource']['name']}]({week['actionable_task']['resource']['url']})")

    st.markdown('</div>', unsafe_allow_html=True) # Close plan-container

else:
    # If no plan is found, guide the user back to the home page
    st.info("Your personalized plan will appear here once you've generated it.")
    if st.button("⬅️ Go back to build your path"):
        st.switch_page("pages/home.py")

st.markdown('</div>', unsafe_allow_html=True) # Close main-container