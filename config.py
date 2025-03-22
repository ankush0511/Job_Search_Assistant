import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# API keys


SERPAPI_API_KEY = st.secrets["SERPAPI_API_KEY"]
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
# SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Model settings
LLM_MODEL = ChatGroq(model='gemma2-9b-it')

# Job search settings
DEFAULT_JOB_COUNT = 5
JOB_PLATFORMS = ["LinkedIn", "Indeed", "Glassdoor", "ZipRecruiter", "Monster"]

COLORS = {
    # Primary palette
    "primary": "#1C4E80",  # Dark blue for main elements and headers
    "secondary": "#0091D5",  # Medium blue for secondary elements
    "tertiary": "#6BB4C0",  # Teal blue for tertiary elements

    # Accent colors
    "accent": "#F17300",  # Orange for highlighting
    "accent1": "#3E7CB1",  # Steel blue for subtler accents
    "accent2": "#44BBA4",  # Seafoam for highlighting information
    "accent3": "#F17300",  # Orange for call-to-action buttons

    # Functional colors
    "success": "#26A69A",  # Teal green for success messages
    "warning": "#F9A825",  # Golden yellow for warnings
    "error": "#E53935",  # Bright red for errors
    "info": "#0277BD",  # Information blue

    # Background and text - BASIC PROFESSIONAL STYLE
    "background": "#F5F7FA",  # Light blue-gray for backgrounds
    "card_bg": "#FFFFFF",  # White for card backgrounds
    "text": "#FFFFFF",  # White for text on dark backgrounds
    "text_dark": "#000000",  # Black for text on light backgrounds
    "text_light": "#333333",  # Dark gray for secondary text
    "text_red": "#FF5252",  # Red color for high-contrast text
    "panel_bg": "#F0F5FF"  # Light blue background for panels
}
