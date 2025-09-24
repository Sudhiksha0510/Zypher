#login.py
import streamlit as st
import streamlit.components.v1 as components
import base64

st.set_page_config(
    page_title="Zypher Login",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="collapsed"
)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}

            /* Apply gradient to the main app container */
            [data-testid="stAppViewContainer"] {
                background-color: #c8e6c9; /* Fallback for browsers without gradient */
                background-image: linear-gradient(180deg, #e0f7fa 0%, #c8e6c9 100%);
                height: 100vh; /* Ensure it takes full viewport height */
                width: 100vw; /* Ensure it takes full viewport width */
            }

            /* Remove padding and margin from specific Streamlit blocks if they're causing issues */
            [data-testid="stVerticalBlock"] {
                gap: 0; /* Adjust or remove gap between blocks */
            }
            .stApp {
                margin: 0;
                padding: 0;
            }

            /* Ensure the html and body elements also have no margin/padding and full size */
            html, body {
                margin: 0 !important;
                padding: 0 !important;
                height: 100% !important;
                width: 100% !important;
                overflow: hidden; /* Hide scrollbars if content doesn't need them */
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- ENCODE IMAGE TO BASE64 ---
# This is a robust way to ensure the image is always available in the HTML
def get_image_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# The path to your logo
logo_base64 = get_image_as_base64("zypher.png")

# --- HTML & CSS FOR THE LOGIN FORM ---
# This is the core of the custom UI. It's a single block of HTML with embedded CSS.
login_html = f"""
<!DOCTYPE html>
<html>
<head>
<title>Zypher Login</title>
<style>
    body {{
        margin: 0;
        padding: 0;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        background: linear-gradient(180deg, #e0f7fa 0%, #c8e6c9 100%);
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
    }}
    .glass-card {{
        background: rgba(255, 255, 255, 0.4);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
        padding: 40px;
        width: 100%;
        max-width: 400px;
        text-align: center;
        color: #2e7d32; /* A darker green for text */
    }}
    .logo {{
        width: 100px;
        margin-bottom: 15px;
    }}
    h1 {{
        font-size: 2.5rem;
        margin: 0;
        color: #1b5e20; /* Even darker green for the title */
    }}
    p {{
        font-size: 1.1rem;
        margin-bottom: 25px;
    }}
    .social-btn {{
        display: block;
        width: 100%;
        padding: 12px;
        margin-bottom: 10px;
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.6);
        color: #333;
        font-size: 1rem;
        text-decoration: none;
        cursor: pointer;
        transition: background-color 0.3s;
    }}
    .social-btn:hover {{
        background: rgba(255, 255, 255, 0.9);
    }}
    .divider {{
        margin: 20px 0;
        border: 0;
        border-top: 1px solid rgba(0, 0, 0, 0.1);
    }}
    input {{
        width: 100%;
        padding: 12px;
        margin-bottom: 15px;
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.6);
        box-sizing: border-box; /* Important for padding */
    }}
    .login-btn {{
        width: 100%;
        padding: 15px;
        border: none;
        border-radius: 10px;
        background-color: #81c784; /* Vibrant green from mockup */
        color: white;
        font-size: 1.2rem;
        font-weight: bold;
        cursor: pointer;
        transition: background-color 0.3s;
    }}
    .login-btn:hover {{
        background-color: #66bb6a;
    }}
    .footer-links {{
        margin-top: 20px;
        font-size: 0.9rem;
    }}
    .footer-links a {{
        color: #2e7d32;
        text-decoration: none;
    }}
    .footer-links a:hover {{
        text-decoration: underline;
    }}
</style>
</head>
<body>
    <div class="glass-card">
        <img src="data:image/jpeg;base64,{logo_base64}" alt="Zypher Logo" class="logo">
        <h1>Zypher</h1>
        <p>Your Learning Breeze</p>
        
        <a href="#" class="social-btn">Sign in with Google</a>
        <a href="#" class="social-btn">Sign in with Microsoft</a>
        
        <hr class="divider">
        
        <form action="#">
            <input type="email" placeholder="Your Email" required>
            <input type="password" placeholder="Your Secure Password" required>
            <button type="submit" class="login-btn">Log In</button>
        </form>
        
        <div class="footer-links">
            <a href="#">Forgot Password?</a> | <a href="#">Sign Up</a>
        </div>
    </div>
</body>
</html>
"""

# --- RENDER THE HTML ---
components.html(login_html, height=700, scrolling=False)