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
    page_icon="N",
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

        html, body, [class*="css"] {
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
     "stack": "Python, LangChain, FastAPI",
     "learn_label": "LangChain Official Tutorials",
     "learn_url": "https://python.langchain.com/docs/tutorials/",
     "repo_label": "Example: Build a Chatbot (GitHub)",
     "repo_url": "https://github.com/langchain-ai/langchain/tree/master/cookbook",
     "video_label": "Watch: LangChain Tutorials",
     "video_url": "https://www.youtube.com/results?search_query=langchain+tutorial+for+beginners"},
    {"name": "Nina Connect", "desc": "A member networking & mentorship platform.", "tag": "Community",
     "stack": "React, Node.js, PostgreSQL",
     "learn_label": "React Official Docs — Learn",
     "learn_url": "https://react.dev/learn",
     "repo_label": "Full-stack React+Node Example (GitHub)",
     "repo_url": "https://github.com/topics/react-node-postgresql",
     "video_label": "Watch: React + Node Full Stack",
     "video_url": "https://www.youtube.com/results?search_query=react+node+postgresql+full+stack+tutorial"},
    {"name": "GreenPulse Tracker", "desc": "Sustainability dashboard for local chapters.", "tag": "Impact",
     "stack": "Vue.js, D3.js, Firebase",
     "learn_label": "D3.js Official Gallery & Docs",
     "learn_url": "https://d3js.org/",
     "repo_label": "Vue + D3 Dashboard Examples (GitHub)",
     "repo_url": "https://github.com/topics/vue-d3",
     "video_label": "Watch: D3.js Dashboard Tutorial",
     "video_url": "https://www.youtube.com/results?search_query=d3.js+dashboard+tutorial"},
    {"name": "SkillForge Academy", "desc": "Peer-led micro-courses & certifications.", "tag": "Learning",
     "stack": "Next.js, Supabase, Stripe",
     "learn_label": "Next.js Official Learn Course",
     "learn_url": "https://nextjs.org/learn",
     "repo_label": "Next.js + Supabase Starter (GitHub)",
     "repo_url": "https://github.com/vercel/next.js/tree/canary/examples/with-supabase",
     "video_label": "Watch: Next.js + Supabase Course",
     "video_url": "https://www.youtube.com/results?search_query=next.js+supabase+full+course"},
    {"name": "EventSphere", "desc": "End-to-end event management toolkit for Nina meetups.", "tag": "Events",
     "stack": "Django, React, AWS",
     "learn_label": "Django Official Tutorial",
     "learn_url": "https://docs.djangoproject.com/en/stable/intro/tutorial01/",
     "repo_label": "Django + React Example (GitHub)",
     "repo_url": "https://github.com/topics/django-react",
     "video_label": "Watch: Django + React Tutorial",
     "video_url": "https://www.youtube.com/results?search_query=django+react+full+stack+tutorial"},
    {"name": "VoiceBridge", "desc": "Multilingual translation tool for global members.", "tag": "AI/ML",
     "stack": "Python, Whisper API, gRPC",
     "learn_label": "OpenAI Whisper Speech-to-Text Guide",
     "learn_url": "https://platform.openai.com/docs/guides/speech-to-text",
     "repo_label": "Whisper Model & Examples (GitHub)",
     "repo_url": "https://github.com/openai/whisper",
     "video_label": "Watch: OpenAI Whisper Tutorial",
     "video_url": "https://www.youtube.com/results?search_query=openai+whisper+speech+to+text+tutorial"},
    {"name": "FundRaise 360", "desc": "Transparent fundraising & donor tracking system.", "tag": "Ops",
     "stack": "Ruby on Rails, PostgreSQL, Plaid",
     "learn_label": "Ruby on Rails Official Guides",
     "learn_url": "https://guides.rubyonrails.org/",
     "repo_label": "Rails + Payments Example (GitHub)",
     "repo_url": "https://github.com/topics/rails-payments",
     "video_label": "Watch: Rails + Payments Tutorial",
     "video_url": "https://www.youtube.com/results?search_query=ruby+on+rails+payments+tutorial"},
    {"name": "PixelCraft Studio", "desc": "Creative design toolkit for branding projects.", "tag": "Design",
     "stack": "Figma API, React, Canvas.js",
     "learn_label": "Figma Developer Docs & API",
     "learn_url": "https://www.figma.com/developers/api",
     "repo_label": "Canvas.js Design Tool Examples (GitHub)",
     "repo_url": "https://github.com/topics/canvas-design-tool",
     "video_label": "Watch: Figma API Tutorial",
     "video_url": "https://www.youtube.com/results?search_query=figma+api+tutorial"},
    {"name": "CodeSprint Arena", "desc": "Competitive hackathon & coding challenge platform.", "tag": "Tech",
     "stack": "Go, Docker, Kubernetes",
     "learn_label": "Kubernetes Official Tutorials",
     "learn_url": "https://kubernetes.io/docs/tutorials/",
     "repo_label": "Go + Docker Starter Kit (GitHub)",
     "repo_url": "https://github.com/topics/go-docker-kubernetes",
     "video_label": "Watch: Kubernetes for Beginners",
     "video_url": "https://www.youtube.com/results?search_query=kubernetes+for+beginners+full+course"},
    {"name": "WellnessHub", "desc": "Mental health & wellness resource center for members.", "tag": "Community",
     "stack": "React Native, Node.js, MongoDB",
     "learn_label": "React Native Official Getting Started",
     "learn_url": "https://reactnative.dev/docs/getting-started",
     "repo_label": "React Native + Node Example (GitHub)",
     "repo_url": "https://github.com/topics/react-native-node-mongodb",
     "video_label": "Watch: React Native Full Course",
     "video_url": "https://www.youtube.com/results?search_query=react+native+full+course+for+beginners"},
]

# ----------------------------------------------------------------------------
# INTEREST-BASED LEARNING RESOURCES — matched to the "Area of Interest" the
# member actually selected during registration
# ----------------------------------------------------------------------------
INTEREST_RESOURCES = {
    "Technology": {
        "video": "https://www.youtube.com/results?search_query=technology+career+roadmap+for+beginners",
        "doc": "https://roadmap.sh/"},
    "Software Development": {
        "video": "https://www.youtube.com/results?search_query=software+development+full+course+for+beginners",
        "doc": "https://roadmap.sh/full-stack"},
    "Data Science & Analytics": {
        "video": "https://www.youtube.com/results?search_query=data+science+full+course+for+beginners",
        "doc": "https://www.kaggle.com/learn"},
    "Artificial Intelligence & ML": {
        "video": "https://www.youtube.com/results?search_query=machine+learning+full+course+for+beginners",
        "doc": "https://www.coursera.org/specializations/machine-learning-introduction"},
    "Cybersecurity": {
        "video": "https://www.youtube.com/results?search_query=cybersecurity+full+course+for+beginners",
        "doc": "https://tryhackme.com/"},
    "Cloud & DevOps": {
        "video": "https://www.youtube.com/results?search_query=devops+full+course+for+beginners",
        "doc": "https://roadmap.sh/devops"},
    "Design": {
        "video": "https://www.youtube.com/results?search_query=graphic+design+full+course+for+beginners",
        "doc": "https://www.figma.com/resource-library/"},
    "UI/UX Design": {
        "video": "https://www.youtube.com/results?search_query=ui+ux+design+full+course+for+beginners",
        "doc": "https://www.interaction-design.org/"},
    "Graphic Design": {
        "video": "https://www.youtube.com/results?search_query=graphic+design+tutorial+for+beginners",
        "doc": "https://www.canva.com/learn/"},
    "Product Management": {
        "video": "https://www.youtube.com/results?search_query=product+management+full+course+for+beginners",
        "doc": "https://www.productplan.com/learn/"},
    "Community & Events": {
        "video": "https://www.youtube.com/results?search_query=community+management+and+event+planning+tutorial",
        "doc": "https://cmxhub.com/resources/"},
    "Marketing & Social Media": {
        "video": "https://www.youtube.com/results?search_query=digital+marketing+full+course+for+beginners",
        "doc": "https://blog.hubspot.com/marketing"},
    "Content Writing": {
        "video": "https://www.youtube.com/results?search_query=content+writing+course+for+beginners",
        "doc": "https://copyblogger.com/blog/"},
    "Fundraising": {
        "video": "https://www.youtube.com/results?search_query=nonprofit+fundraising+strategies+tutorial",
        "doc": "https://www.classy.org/blog/"},
    "Sponsorship & Partnerships": {
        "video": "https://www.youtube.com/results?search_query=sponsorship+and+partnerships+strategy+tutorial",
        "doc": "https://sponsorship.com/resources/"},
    "Learning & Development": {
        "video": "https://www.youtube.com/results?search_query=learning+and+development+tutorial+for+beginners",
        "doc": "https://www.td.org/insights"},
    "Mentorship": {
        "video": "https://www.youtube.com/results?search_query=how+to+be+a+good+mentor+tutorial",
        "doc": "https://www.mentorloop.com/blog/"},
    "Operations": {
        "video": "https://www.youtube.com/results?search_query=business+operations+management+tutorial",
        "doc": "https://asana.com/resources/operations-management"},
    "Human Resources": {
        "video": "https://www.youtube.com/results?search_query=human+resources+fundamentals+course",
        "doc": "https://www.shrm.org/topics-tools"},
    "Finance & Accounting": {
        "video": "https://www.youtube.com/results?search_query=finance+and+accounting+basics+course",
        "doc": "https://www.investopedia.com/"},
    "Legal & Compliance": {
        "video": "https://www.youtube.com/results?search_query=nonprofit+legal+compliance+basics",
        "doc": "https://www.councilofnonprofits.org/running-nonprofit"},
    "Research": {
        "video": "https://www.youtube.com/results?search_query=research+methods+tutorial+for+beginners",
        "doc": "https://www.scribbr.com/category/methodology/"},
    "Public Relations": {
        "video": "https://www.youtube.com/results?search_query=public+relations+fundamentals+course",
        "doc": "https://www.prsa.org/"},
    "Volunteering & Outreach": {
        "video": "https://www.youtube.com/results?search_query=volunteer+program+management+tutorial",
        "doc": "https://www.volunteermatch.org/nonprofits/resources"},
    "Wellness": {
        "video": "https://www.youtube.com/results?search_query=workplace+wellness+program+tutorial",
        "doc": "https://www.who.int/teams/mental-health-and-substance-use/promotion-prevention/mental-health-in-the-workplace"},
    "Other": {
        "video": "https://www.youtube.com/results?search_query=nina+organization+community+skills",
        "doc": "https://www.coursera.org/"},
}

WELCOME_MESSAGES = [
    "You're officially part of something amazing! ",
    "The Nina family just got bigger — welcome aboard! ",
    "Get ready to build, learn, and grow with us! ",
    "Your journey with Nina Organization starts now! ",
]

EMAIL_REGEX = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
PHONE_REGEX = r"^\+?[0-9\s\-]{7,15}$"

# ----------------------------------------------------------------------------
# HERO SECTION
# ----------------------------------------------------------------------------
st.markdown(
    """
    <div class="nina-hero">
        <h1> Nina Organization</h1>
        <p>Empowering people, building futures — join our community today</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# REGISTRATION FORM (only shown before successful registration)
# ----------------------------------------------------------------------------
if not st.session_state.registered:

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Member Registration</div>', unsafe_allow_html=True)

    with st.form("registration_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name *", placeholder="Nina")
        with col2:
            last_name = st.text_input("Last Name *", placeholder="Sharma")

        email = st.text_input("Email Address *", placeholder="nina@example.com")
        phone = st.text_input("Phone Number *", placeholder="+91 98765 43210")

        department = st.selectbox(
            "Area of Interest *",
            [
                "Technology",
                "Software Development",
                "Data Science & Analytics",
                "Artificial Intelligence & ML",
                "Cybersecurity",
                "Cloud & DevOps",
                "Design",
                "UI/UX Design",
                "Graphic Design",
                "Product Management",
                "Community & Events",
                "Marketing & Social Media",
                "Content Writing",
                "Fundraising",
                "Sponsorship & Partnerships",
                "Learning & Development",
                "Mentorship",
                "Operations",
                "Human Resources",
                "Finance & Accounting",
                "Legal & Compliance",
                "Research",
                "Public Relations",
                "Volunteering & Outreach",
                "Wellness",
                "Other",
            ],
        )

        experience = st.select_slider(
            "Experience Level",
            options=["Beginner", "Novice", "Intermediate", "Advanced", "Expert", "Specialist"],
            value="Intermediate",
        )

        availability = st.selectbox(
            "Weekly Availability",
            [
                "Less than 2 hours",
                "2-5 hours",
                "5-10 hours",
                "10-15 hours",
                "15-20 hours",
                "20+ hours",
                "Flexible / Varies",
            ],
        )

        preferred_mode = st.selectbox(
            "Preferred Mode of Involvement",
            [
                "Remote only",
                "In-person only",
                "Hybrid (Remote + In-person)",
                "No preference",
            ],
        )

        referral = st.selectbox(
            "How did you hear about Nina Organization?",
            [
                "Social Media",
                "Friend or Colleague Referral",
                "College/University Event",
                "Online Search",
                "Community Meetup",
                "Newsletter",
                "Other",
            ],
        )

        bio = st.text_area("Tell us about yourself", placeholder="A few lines about you, your skills, and why you're joining Nina...", height=90)

        terms = st.checkbox("I agree to the Nina Organization's terms & code of conduct")

        submitted = st.form_submit_button("Register & Unlock Projects")

    if submitted:
        errors = []
        if not first_name.strip() or not last_name.strip():
            errors.append("Please enter your full name.")
        if not email.strip() or not re.match(EMAIL_REGEX, email.strip()):
            errors.append("Please enter a valid email address.")
        if not phone.strip() or not re.match(PHONE_REGEX, phone.strip()):
            errors.append("Please enter a valid phone number.")

        if errors:
            for e in errors:
                st.error(e)
        else:
            st.session_state.user_data = {
                "first_name": first_name.strip(),
                "last_name": last_name.strip(),
                "email": email.strip(),
                "phone": phone.strip(),
                "department": department,
                "experience": experience,
                "availability": availability,
                "preferred_mode": preferred_mode,
                "referral": referral,
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

    st.markdown(
        """
        <style>
            .success-check-wrap {
                position: relative;
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 1.5rem 0 0.5rem 0;
                height: 120px;
            }
            .success-check {
                position: relative;
                z-index: 2;
                width: 84px;
                height: 84px;
                border-radius: 50%;
                background: linear-gradient(135deg, #22c55e, #16a34a);
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 10px 30px rgba(34, 197, 94, 0.45);
                animation: pop-in 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
            }
            .success-check svg {
                width: 44px;
                height: 44px;
            }
            .success-check svg path {
                stroke: white;
                stroke-width: 4;
                fill: none;
                stroke-linecap: round;
                stroke-linejoin: round;
                stroke-dasharray: 48;
                stroke-dashoffset: 48;
                animation: draw-check 0.5s ease forwards 0.35s;
            }
            .blast-dot {
                position: absolute;
                top: 50%;
                left: 50%;
                width: 8px;
                height: 8px;
                border-radius: 50%;
                opacity: 0;
                animation: blast-out 0.7s ease-out forwards 0.15s;
            }
            @keyframes pop-in {
                0% { transform: scale(0); opacity: 0; }
                60% { transform: scale(1.15); opacity: 1; }
                100% { transform: scale(1); }
            }
            @keyframes draw-check {
                to { stroke-dashoffset: 0; }
            }
            @keyframes blast-out {
                0% { transform: translate(-50%, -50%) rotate(var(--ang)) translateX(0) scale(1); opacity: 1; }
                100% { transform: translate(-50%, -50%) rotate(var(--ang)) translateX(70px) scale(0); opacity: 0; }
            }
        </style>
        <div class="success-check-wrap">
            <div class="blast-dot" style="--ang:0deg; background:#22c55e;"></div>
            <div class="blast-dot" style="--ang:30deg; background:#764ba2;"></div>
            <div class="blast-dot" style="--ang:60deg; background:#f093fb;"></div>
            <div class="blast-dot" style="--ang:90deg; background:#22c55e;"></div>
            <div class="blast-dot" style="--ang:120deg; background:#764ba2;"></div>
            <div class="blast-dot" style="--ang:150deg; background:#f093fb;"></div>
            <div class="blast-dot" style="--ang:180deg; background:#22c55e;"></div>
            <div class="blast-dot" style="--ang:210deg; background:#764ba2;"></div>
            <div class="blast-dot" style="--ang:240deg; background:#f093fb;"></div>
            <div class="blast-dot" style="--ang:270deg; background:#22c55e;"></div>
            <div class="blast-dot" style="--ang:300deg; background:#764ba2;"></div>
            <div class="blast-dot" style="--ang:330deg; background:#f093fb;"></div>
            <div class="success-check">
                <svg viewBox="0 0 24 24">
                    <path d="M4 12.5 L9.5 18 L20 6" />
                </svg>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.spinner("Unlocking your Nina member perks..."):
        time.sleep(0.6)

    st.markdown(
        f"""
        <div class="welcome-banner">
            <h2>Welcome, {data['first_name']}!</h2>
            <p>{random.choice(WELCOME_MESSAGES)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Your Registration Summary</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**Name:** {data['first_name']} {data['last_name']}")
        st.markdown(f"**Email:** {data['email']}")
        st.markdown(f"**Phone:** {data['phone']}")
        st.markdown(f"**Availability:** {data['availability']}")
    with c2:
        st.markdown(f"**Interest Area:** {data['department']}")
        st.markdown(f"**Experience:** {data['experience']}")
        st.markdown(f"**Preferred Mode:** {data['preferred_mode']}")
        st.markdown(f"**Registered On:** {data['registered_at']}")

    if data.get("bio"):
        st.markdown(f"**About:** _{data['bio']}_")

    st.markdown("</div>", unsafe_allow_html=True)

    interest_res = INTEREST_RESOURCES.get(data["department"], INTEREST_RESOURCES["Other"])
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">Resources for {data["department"]}</div>', unsafe_allow_html=True)
    st.write(f"Since you're interested in **{data['department']}**, here's where to start learning:")

    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.link_button(f"Watch: {data['department']} Videos", interest_res["video"], use_container_width=True)
    with res_col2:
        st.link_button(f"Explore: {data['department']} Resources", interest_res["doc"], use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Exciting News — You\'ve Unlocked 4 Projects!</div>', unsafe_allow_html=True)
    st.write("Based on your interests, here are hand-picked projects you can jump into right away:")

    for proj in data["unlocked_projects"]:
        joined = proj["name"] in st.session_state.joined_projects

        st.markdown(
            f"""
            <div class="project-card">
                <h4>{proj['name']}</h4>
                <p>{proj['desc']}</p>
                <p style="margin-top:0.4rem; font-size:0.82rem; color:#764ba2;"><b>Tech Stack:</b> {proj['stack']}</p>
                <span class="badge">{proj['tag']}</span>
                {'<span class="badge" style="background:#dcfce7;color:#166534;margin-left:6px;">Joined</span>' if joined else ''}
            </div>
            """,
            unsafe_allow_html=True,
        )

        link_col1, link_col2, link_col3, join_col = st.columns([1.15, 1.15, 1.15, 0.9])

        with link_col1:
            st.link_button(f"{proj['learn_label']}", proj["learn_url"], use_container_width=True)

        with link_col2:
            st.link_button(f"{proj['repo_label']}", proj["repo_url"], use_container_width=True)

        with link_col3:
            st.link_button(f"{proj['video_label']}", proj["video_url"], use_container_width=True)

        with join_col:
            if joined:
                st.button("Joined", key=f"joined_{proj['name']}", disabled=True, use_container_width=True)
            else:
                if st.button("Join Project", key=f"join_{proj['name']}", use_container_width=True):
                    st.session_state.joined_projects.add(proj["name"])
                    st.toast(f"You joined {proj['name']}!", icon="")
                    st.rerun()

        st.markdown("<div style='margin-bottom: 0.8rem;'></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    colA, colB = st.columns(2)
    with colA:
        if st.button("Register Another Member"):
            st.session_state.registered = False
            st.session_state.user_data = {}
            st.rerun()
    with colB:
        st.button("Share My Journey (coming soon)", disabled=True)

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