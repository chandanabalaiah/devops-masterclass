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
     "stack": "Python, LangChain, FastAPI",
     "learn_label": "LangChain Official Tutorials",
     "learn_url": "https://python.langchain.com/docs/tutorials/",
     "repo_label": "Example: Build a Chatbot (GitHub)",
     "repo_url": "https://github.com/langchain-ai/langchain/tree/master/cookbook"},
    {"name": "Nina Connect", "desc": "A member networking & mentorship platform.", "tag": "Community",
     "stack": "React, Node.js, PostgreSQL",
     "learn_label": "React Official Docs — Learn",
     "learn_url": "https://react.dev/learn",
     "repo_label": "Full-stack React+Node Example (GitHub)",
     "repo_url": "https://github.com/topics/react-node-postgresql"},
    {"name": "GreenPulse Tracker", "desc": "Sustainability dashboard for local chapters.", "tag": "Impact",
     "stack": "Vue.js, D3.js, Firebase",
     "learn_label": "D3.js Official Gallery & Docs",
     "learn_url": "https://d3js.org/",
     "repo_label": "Vue + D3 Dashboard Examples (GitHub)",
     "repo_url": "https://github.com/topics/vue-d3"},
    {"name": "SkillForge Academy", "desc": "Peer-led micro-courses & certifications.", "tag": "Learning",
     "stack": "Next.js, Supabase, Stripe",
     "learn_label": "Next.js Official Learn Course",
     "learn_url": "https://nextjs.org/learn",
     "repo_label": "Next.js + Supabase Starter (GitHub)",
     "repo_url": "https://github.com/vercel/next.js/tree/canary/examples/with-supabase"},
    {"name": "EventSphere", "desc": "End-to-end event management toolkit for Nina meetups.", "tag": "Events",
     "stack": "Django, React, AWS",
     "learn_label": "Django Official Tutorial",
     "learn_url": "https://docs.djangoproject.com/en/stable/intro/tutorial01/",
     "repo_label": "Django + React Example (GitHub)",
     "repo_url": "https://github.com/topics/django-react"},
    {"name": "VoiceBridge", "desc": "Multilingual translation tool for global members.", "tag": "AI/ML",
     "stack": "Python, Whisper API, gRPC",
     "learn_label": "OpenAI Whisper Speech-to-Text Guide",
     "learn_url": "https://platform.openai.com/docs/guides/speech-to-text",
     "repo_label": "Whisper Model & Examples (GitHub)",
     "repo_url": "https://github.com/openai/whisper"},
    {"name": "FundRaise 360", "desc": "Transparent fundraising & donor tracking system.", "tag": "Ops",
     "stack": "Ruby on Rails, PostgreSQL, Plaid",
     "learn_label": "Ruby on Rails Official Guides",
     "learn_url": "https://guides.rubyonrails.org/",
     "repo_label": "Rails + Payments Example (GitHub)",
     "repo_url": "https://github.com/topics/rails-payments"},
    {"name": "PixelCraft Studio", "desc": "Creative design toolkit for branding projects.", "tag": "Design",
     "stack": "Figma API, React, Canvas.js",
     "learn_label": "Figma Developer Docs & API",
     "learn_url": "https://www.figma.com/developers/api",
     "repo_label": "Canvas.js Design Tool Examples (GitHub)",
     "repo_url": "https://github.com/topics/canvas-design-tool"},
    {"name": "CodeSprint Arena", "desc": "Competitive hackathon & coding challenge platform.", "tag": "Tech",
     "stack": "Go, Docker, Kubernetes",
     "learn_label": "Kubernetes Official Tutorials",
     "learn_url": "https://kubernetes.io/docs/tutorials/",
     "repo_label": "Go + Docker Starter Kit (GitHub)",
     "repo_url": "https://github.com/topics/go-docker-kubernetes"},
    {"name": "WellnessHub", "desc": "Mental health & wellness resource center for members.", "tag": "Community",
     "stack": "React Native, Node.js, MongoDB",
     "learn_label": "React Native Official Getting Started",
     "learn_url": "https://reactnative.dev/docs/getting-started",
     "repo_label": "React Native + Node Example (GitHub)",
     "repo_url": "https://github.com/topics/react-native-node-mongodb"},
]

WELCOME_MESSAGES = [
    "You're officially part of something amazing! 🎉",
    "The Nina family just got bigger — welcome
