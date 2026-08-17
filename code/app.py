"""
Nina Organization — Member Registration Portal
Run with: streamlit run nina_registration_app.py
"""

import streamlit as st
import time
import random
import re
from datetime import datetime

# ----------------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Nina Organization | Registration",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ----------------------------------------------------------------------------
# CUSTOM CSS — gradient background, glass cards, responsive layout
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Poppins', sans-serif;
        }

        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 45%, #f093fb 100%);
            background-attachment: fixed;
        }

        /* Hide default streamlit chrome */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 780px;
        }

        .nina-hero {
            text-align: center;
            padding: 1.5rem 1rem 0.5rem 1rem;
            color: white;
        }

        .nina-hero h1 {
            font-size: 2.6rem;
            font-weight: 800;
            margin-bottom: 0.2rem;
            text-shadow: 0 4px 20px rgba(0,0,0,0.25);
            letter-spacing: -1px;
        }

        .nina-hero p {
            font-size: 1.05rem;
            font-weight: 300;
            opacity: 0.92;
            margin-top: 0;
        }

        .glass-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 22px;
            padding: 2rem 2rem 1.2rem 2rem;
            box-shadow: 0 20px 50px rgba(31, 38, 135, 0.25);
            border: 1px solid rgba(255, 255, 255, 0.4);
            margin-top: 1.2rem;
        }

        .section-title {
            font-weight: 700;
            font-size: 1.15rem;
            color: #4c1d95;
            margin-bottom: 0.6rem;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }

        div.stButton > button {
            width: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            color: white;
            font-weight: 600;
            font-size: 1.05rem;
            padding: 0.7rem 0;
            border-radius: 14px;
            border: none;
            box-shadow: 0 8px 20px rgba(118, 75, 162, 0.4);
            transition: all 0.25s ease;
        }

        div.stButton > button:hover {
            transform: translateY(-2px) scale(1.01);
            box-shadow: 0 12px 28px rgba(118, 75, 162, 0.55);
            color: white;
        }

        .stTextInput input, .stTextInput textarea, .stSelectbox div[data-baseweb="select"] > div,
        .stDateInput input, .stTextArea textarea {
            border-radius: 12px !important;
            border: 1.5px solid #e5d9f7 !important;
        }

        .project-card {
            background: linear-gradient(135deg, #ffffff, #f6f1ff);
            border-radius: 18px;
            padding: 1.1rem 1.3rem;
            margin-bottom: 0.6rem;
            border-left: 5px solid #764ba2;
            box-shadow: 0 8px 20px rgba(118, 75, 162, 0.12);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            cursor: pointer;
        }
        .project-card:hover {
            transform: translateX(4px);
            box-shadow: 0 12px 28px rgba(118, 75, 162, 0.22);
        }
        .project-card h4 {
            margin: 0 0 0.25rem 0;
            color: #4c1d95;
        }
        .project-card p {
            margin: 0;
            color: #555;
            font-size: 0.92rem;
        }
        .badge {
            display: inline-block;
            background: #ede9fe;
            color: #5b21b6;
            font-size: 0.72rem;
            font-weight: 700;
            padding: 0.15rem 0.6rem;
            border-radius: 20px;
            margin-top: 0.4rem;
        }

        .welcome-banner {
            text-align: center;
            color: white;
            padding: 1.6rem 1rem;
            border-radius: 20px;
            background: linear-gradient(120deg, #f093fb, #764ba2);
            box-shadow: 0 15px 35px rgba(0,0,0,0.25);
            margin-bottom: 1.4rem;
        }
        .welcome-banner h2 {
            margin: 0;
            font-size: 1.8rem;
            font-weight: 800;
        }
        .welcome-banner p {
            margin-top: 0.3rem;
            font-weight: 300;
            opacity: 0.95;
        }

        .footer-note {
            text-align: center;
            color: rgba(255,255,255,0.85);
            font-size: 0.8rem;
            margin-top: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# SESSION STATE
# ----------------------------------------------------------------------------
if "registered" not in st.session_state:
    st.session_state.registered = False
if "user_data" not in st.session_state:
    st.session_state.user_data = {}
if "joined_projects" not in st.session_state:
    st.session_state.joined_projects = set()

# ----------------------------------------------------------------------------
# DATA — Project pool that gets "unlocked" after registration
# ----------------------------------------------------------------------------
PROJECT_POOL = [
    {"name": "Aurora AI Assistant", "desc": "Build a conversational assistant for internal ops.", "tag": "AI/ML",
     "team_size": "4-6 members", "duration": "8 weeks", "stack": "Python, LangChain, FastAPI", "lead": "Riya Kapoor"},
    {"name": "Nina Connect", "desc": "A member networking & mentorship platform.", "tag": "Community",
     "team_size": "3-5 members", "duration": "6 weeks", "stack": "React, Node.js, PostgreSQL", "lead": "Arjun Mehta"},
    {"name": "GreenPulse Tracker", "desc": "Sustainability dashboard for local chapters.", "tag": "Impact",
     "team_size": "3-4 members", "duration": "5 weeks", "stack": "Vue.js, D3.js, Firebase", "lead": "Simran Kaur"},
    {"name": "SkillForge Academy", "desc": "Peer-led micro-courses & certifications.", "tag": "Learning",
     "team_size": "5-7 members", "duration": "10 weeks", "stack": "Next.js, Supabase, Stripe", "lead": "Devika Rao"},
    {"name": "EventSphere", "desc": "End-to-end event management toolkit for Nina meetups.", "tag": "Events",
     "team_size": "4-5 members", "duration": "7 weeks", "stack": "Django, React, AWS", "lead": "Karan Shah"},
    {"name": "VoiceBridge", "desc": "Multilingual translation tool for global members.", "tag": "AI/ML",
     "team_size": "4-6 members", "duration": "9 weeks", "stack": "Python, Whisper API, gRPC", "lead": "Meera Iyer"},
    {"name": "FundRaise 360", "desc": "Transparent fundraising & donor tracking system.", "tag": "Ops",
     "team_size": "3-5 members", "duration": "6 weeks", "stack": "Ruby on Rails, PostgreSQL, Plaid", "lead": "Vikram Nair"},
    {"name": "PixelCraft Studio", "desc": "Creative design toolkit for branding projects.", "tag": "Design",
     "team_size": "2-4 members", "duration": "5 weeks", "stack": "Figma API, React, Canvas.js", "lead": "Ananya Desai"},
    {"name": "CodeSprint Arena", "desc": "Competitive hackathon & coding challenge platform.", "tag": "Tech",
     "team_size": "5-6 members", "duration": "8 weeks", "stack": "Go, Docker, Kubernetes", "lead": "Rohan Verma"},
    {"name": "WellnessHub", "desc": "Mental health & wellness resource center for members.", "tag": "Community",
     "team_size": "3-4 members", "duration": "6 weeks", "stack": "React Native, Node.js, MongoDB", "lead": "Priya Nambiar"},
]

WELCOME_MESSAGES = [
    "You're officially part of something amazing! 🎉",
    "The Nina family just got bigger — welcome aboard! 🚀",
    "Get ready to build, learn, and grow with us! 🌟",
    "Your journey with Nina Organization starts now! 🔥",
]

EMAIL_REGEX = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
PHONE_REGEX = r"^\+?[0-9\s\-]{7,15}$"

# ----------------------------------------------------------------------------
# HERO SECTION
# ----------------------------------------------------------------------------
st.markdown(
    """
    <div class="nina-hero">
        <h1>✨ Nina Organization</h1>
        <p>Empowering people, building futures — join our community today</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# REGISTRATION FORM  (only shown before successful registration)
# ----------------------------------------------------------------------------
if not st.session_state.registered:

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📝 Member Registration</div>', unsafe_allow_html=True)

    with st.form("registration_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name *", placeholder="Nina")
        with col2:
            last_name = st.text_input("Last Name *", placeholder="Sharma")

        email = st.text_input("Email Address *", placeholder="nina@example.com")
        phone = st.text_input("Phone Number *", placeholder="+91 98765 43210")

        col3, col4 = st.columns(2)
        with col3:
            dob = st.date_input(
                "Date of Birth",
                min_value=datetime(1950, 1, 1),
                max_value=datetime.now(),
                value=None,
            )
        with col4:
            gender = st.selectbox("Gender", ["Prefer not to say", "Female", "Male", "Non-binary", "Other"])

        department = st.selectbox(
            "Area of Interest *",
            ["Technology", "Design", "Community & Events", "Fundraising", "Learning & Development", "Operations"],
        )

        experience = st.select_slider(
            "Experience Level",
            options=["Beginner", "Intermediate", "Advanced", "Expert"],
            value="Intermediate",
        )

        bio = st.text_area("Tell us about yourself", placeholder="A few lines about you, your skills, and why you're joining Nina...", height=90)

        terms = st.checkbox("I agree to the Nina Organization's terms & code of conduct *")

        submitted = st.form_submit_button("🚀 Register & Unlock Projects")

    if submitted:
        errors = []
        if not first_name.strip() or not last_name.strip():
            errors.append("Please enter your full name.")
        if not email.strip() or not re.match(EMAIL_REGEX, email.strip()):
            errors.append("Please enter a valid email address.")
        if not phone.strip() or not re.match(PHONE_REGEX, phone.strip()):
            errors.append("Please enter a valid phone number.")
        if not terms:
            errors.append("You must agree to the terms & code of conduct.")

        if errors:
            for e in errors:
                st.error(e)
        else:
            st.session_state.user_data = {
                "first_name": first_name.strip(),
                "last_name": last_name.strip(),
                "email": email.strip(),
                "phone": phone.strip(),
                "dob": dob,
                "gender": gender,
                "department": department,
                "experience": experience,
                "bio": bio.strip(),
                "unlocked_projects": random.sample(PROJECT_POOL, k=4),
                "registered_at": datetime.now().strftime("%d %b %Y, %I:%M %p"),
            }
            st.session_state.registered = True
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# SUCCESS / WELCOME SCREEN
# ----------------------------------------------------------------------------
else:
    data = st.session_state.user_data

    st.balloons()

    with st.spinner("Unlocking your Nina member perks..."):
        time.sleep(0.6)

    st.markdown(
        f"""
        <div class="welcome-banner">
            <h2>🎉 Welcome, {data['first_name']}!</h2>
            <p>{random.choice(WELCOME_MESSAGES)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🪪 Your Registration Summary</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**Name:** {data['first_name']} {data['last_name']}")
        st.markdown(f"**Email:** {data['email']}")
        st.markdown(f"**Phone:** {data['phone']}")
    with c2:
        st.markdown(f"**Interest Area:** {data['department']}")
        st.markdown(f"**Experience:** {data['experience']}")
        st.markdown(f"**Registered On:** {data['registered_at']}")

    if data.get("bio"):
        st.markdown(f"**About:** _{data['bio']}_")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔓 Exciting News — You\'ve Unlocked 4 Projects!</div>', unsafe_allow_html=True)
    st.write("Based on your interests, here are hand-picked projects you can jump into right away:")

    for proj in data["unlocked_projects"]:
        joined = proj["name"] in st.session_state.joined_projects

        st.markdown(
            f"""
            <div class="project-card">
                <h4>🚀 {proj['name']}</h4>
                <p>{proj['desc']}</p>
                <span class="badge">{proj['tag']}</span>
                {'<span class="badge" style="background:#dcfce7;color:#166534;margin-left:6px;">✅ Joined</span>' if joined else ''}
            </div>
            """,
            unsafe_allow_html=True,
        )

        detail_col, join_col = st.columns([1, 1])

        with detail_col:
            with st.popover("🔍 View Details", use_container_width=True):
                st.markdown(f"### {proj['name']}")
                st.write(proj["desc"])
                st.markdown(f"**Project Lead:** {proj['lead']}")
                st.markdown(f"**Team Size:** {proj['team_size']}")
                st.markdown(f"**Duration:** {proj['duration']}")
                st.markdown(f"**Tech Stack:** {proj['stack']}")
                st.markdown(f"**Category:** {proj['tag']}")

        with join_col:
            if joined:
                st.button("✅ Joined", key=f"joined_{proj['name']}", disabled=True, use_container_width=True)
            else:
                if st.button("Join Project", key=f"join_{proj['name']}", use_container_width=True):
                    st.session_state.joined_projects.add(proj["name"])
                    st.toast(f"🎉 You joined {proj['name']}!", icon="🚀")
                    st.rerun()

        st.markdown("<div style='margin-bottom: 0.8rem;'></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    colA, colB = st.columns(2)
    with colA:
        if st.button("🔄 Register Another Member"):
            st.session_state.registered = False
            st.session_state.user_data = {}
            st.rerun()
    with colB:
        st.button("📤 Share My Journey (coming soon)", disabled=True)

# ----------------------------------------------------------------------------
# FOOTER
# ----------------------------------------------------------------------------
st.markdown(
    """
    <div class="footer-note">
        Made with 💜 for Nina Organization &nbsp;|&nbsp; Powered by Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)
