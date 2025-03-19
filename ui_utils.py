
import streamlit as st
from config import COLORS

def display_resume_analysis_summary(resume_data):
    """
    Display a summary of the resume analysis with improved visibility.

    Args:
        resume_data (dict): The parsed resume data dictionary
    """
    if not resume_data:
        st.warning("Resume data is not available. Please upload your resume.")
        return

    # Extract skills and experience
    skills = resume_data.get("skills", [])
    experience = resume_data.get("experience", [])

    # Define technical categories
    tech_categories = {
        "Programming": ["python", "java", "javascript", "c++", "ruby", "go"],
        "Data Science": ["ml", "ai", "machine learning", "data science", "scikit", "numpy", "pandas"],
        "Cloud & DevOps": ["aws", "azure", "gcp", "cloud", "ci/cd", "git", "docker"],
        "Databases": ["sql", "mysql", "postgresql", "mongodb", "nosql"],
        "Web & Mobile": ["react", "angular", "vue", "node", "android", "ios"],
        "Other": []
    }

    # Categorize skills
    categorized_skills = {cat: [] for cat in tech_categories}
    for skill in skills:
        skill_lower = skill.lower()
        found = False
        for category, keywords in tech_categories.items():
            if any(keyword in skill_lower for keyword in keywords):
                categorized_skills[category].append(skill)
                found = True
                break
        if not found:
            categorized_skills["Other"].append(skill)

    # Create summary
    st.subheader("Resume Analysis Summary")

    # Strengths and areas to improve
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""<h4 style="color: #1A237E; margin-bottom: 10px;">Strengths</h4>""", unsafe_allow_html=True)
        strengths = []
        # Identify strengths based on skills and experience
        if any(len(categorized_skills[cat]) > 0 for cat in ["Programming", "Data Science"]):
            strengths.append("Strong technical skills in programming and/or data science")
        if any("aws" in skill.lower() or "cloud" in skill.lower() for skill in skills):
            strengths.append("Cloud platform experience")
        if any("ml" in skill.lower() or "ai" in skill.lower() for skill in skills):
            strengths.append("Machine learning knowledge")

        # Display strengths with high-contrast styling
        if strengths:
            for strength in strengths:
                st.markdown(
                    f"""<div style="background-color: #01579B; color: white; padding: 12px; 
                    border-radius: 6px; margin-bottom: 10px; font-weight: 500;">
                    ✅ {strength}</div>""", 
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                """<div style="background-color: #546E7A; color: white; padding: 12px; 
                border-radius: 6px;">Not enough information to determine strengths</div>""", 
                unsafe_allow_html=True
            )

    with col2:
        st.markdown("""<h4 style="color: #B71C1C; margin-bottom: 10px;">Areas to Improve</h4>""", unsafe_allow_html=True)
        improvements = []
        # Identify improvement areas
        if not any("git" in skill.lower() for skill in skills):
            improvements.append("Version control experience (Git)")
        if not any(db in "".join(skills).lower() for db in ["sql", "database"]):
            improvements.append("Database knowledge")
        if not any(cloud in "".join(skills).lower() for cloud in ["aws", "azure", "gcp", "cloud"]):
            improvements.append("Cloud platform experience")

        # Display improvement areas with high-contrast styling
        if improvements:
            for improvement in improvements:
                st.markdown(
                    f"""<div style="background-color: #C62828; color: white; padding: 12px; 
                    border-radius: 6px; margin-bottom: 10px; font-weight: 500;">
                    ⚠️ {improvement}</div>""", 
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                """<div style="background-color: #2E7D32; color: white; padding: 12px; 
                border-radius: 6px;">No obvious improvement areas identified</div>""", 
                unsafe_allow_html=True
            )

def clean_and_organize_experience(experience_items):
    """Helper function to organize experience into categories."""
    categories = {
        "Programming Experience": [],
        "Machine Learning & AI": [],
        "Cloud Computing": [],
        "Data Analysis": [],
        "Companies & Roles": []
    }

    # Simple keyword-based categorization
    for item in experience_items:
        item_lower = item.lower()
        if any(kw in item_lower for kw in ["program", "develop", "code", "software"]):
            categories["Programming Experience"].append(item)
        elif any(kw in item_lower for kw in ["machine", "learning", "ai", "neural", "model"]):
            categories["Machine Learning & AI"].append(item)
        elif any(kw in item_lower for kw in ["cloud", "aws", "azure", "gcp"]):
            categories["Cloud Computing"].append(item)
        elif any(kw in item_lower for kw in ["data", "analytics", "analysis", "statistics"]):
            categories["Data Analysis"].append(item)
        else:
            categories["Companies & Roles"].append(item)

    return categories

def display_extracted_information(resume_data):
    """
    Display extracted resume information with better visibility.

    Args:
        resume_data (dict): The parsed resume data dictionary
    """
    if not resume_data:
        st.warning("Resume data is not available. Please upload your resume.")
        return

    st.subheader("Extracted Information")

    # Create columns for different information types
    info_col1, info_col2 = st.columns(2)

    with info_col1:
        # Display contact info
        st.markdown("""<h4 style="color: #333; margin-bottom: 10px;">📞 Contact Information</h4>""", unsafe_allow_html=True)
        contact_info = resume_data.get("contact_info", {})
        contact_html = """<div style="background-color: #1A237E; color: white; padding: 15px; border-radius: 8px; margin-bottom: 15px;">"""

        if contact_info and (contact_info.get("email") or contact_info.get("phone")):
            if contact_info.get("email"):
                contact_html += f"<p><strong>Email:</strong> {contact_info['email']}</p>"
            if contact_info.get("phone"):
                contact_html += f"<p><strong>Phone:</strong> {contact_info['phone']}</p>"
        else:
            contact_html += "<p>No contact information detected.</p>"

        contact_html += "</div>"
        st.markdown(contact_html, unsafe_allow_html=True)

        # Display education
        st.markdown("""<h4 style="color: #333; margin-bottom: 10px;">🎓 Education</h4>""", unsafe_allow_html=True)
        education = resume_data.get("education", [])
        education_html = """<div style="background-color: #4A148C; color: white; padding: 15px; border-radius: 8px;">"""

        if education:
            for edu in education:
                education_html += f"<p>• {edu}</p>"
        else:
            education_html += "<p>No education information detected.</p>"

        education_html += "</div>"
        st.markdown(education_html, unsafe_allow_html=True)

    with info_col2:
        # Display skills with high-contrast horizontal layout
        st.markdown("""<h4 style="color: #333; margin-bottom: 10px;">🛠️ Skills</h4>""", unsafe_allow_html=True)
        skills = resume_data.get("skills", [])

        if skills:
            # Create a flex container for horizontal layout
            skills_html = """<div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 15px;">"""

            # Add each skill with a high-contrast background
            for skill in skills:
                skills_html += f"""<div style="background-color: #0D47A1; color: white; 
                padding: 8px 12px; border-radius: 20px; font-weight: 500; margin-bottom: 8px;">
                {skill}</div>"""

            skills_html += "</div>"
            st.markdown(skills_html, unsafe_allow_html=True)
        else:
            st.markdown(
                """<div style="background-color: #546E7A; color: white; padding: 15px; 
                border-radius: 8px;">No skills detected.</div>""", 
                unsafe_allow_html=True
            )

        # Display experience using the organized categories function
        st.markdown("""<h4 style="color: #333; margin-bottom: 10px;">💼 Experience</h4>""", unsafe_allow_html=True)
        experience = resume_data.get("experience", [])

        if experience:
            # Organize the experience items
            organized_exp = clean_and_organize_experience(experience)

            # Display each category in an accordion-like structure
            for category, items in organized_exp.items():
                if items:
                    # Set category-specific colors
                    if "Programming" in category:
                        bg_color = "#01579B"  # Deep blue
                    elif "Machine Learning" in category or "AI" in category:
                        bg_color = "#4A148C"  # Deep purple
                    elif "Cloud" in category:
                        bg_color = "#004D40"  # Deep teal
                    elif "Data" in category:
                        bg_color = "#BF360C"  # Deep orange
                    elif "Companies" in category:
                        bg_color = "#B71C1C"  # Deep red
                    else:
                        bg_color = "#37474F"  # Deep blue-grey

                    # Create category header
                    st.markdown(
                        f"""<div style="background-color: {bg_color}; color: white; padding: 10px; 
                        border-radius: 8px 8px 0 0; font-weight: bold; margin-top: 10px;">
                        {category} ({len(items)})</div>""", 
                        unsafe_allow_html=True
                    )

                    # Create flex container for items
                    items_html = f"""<div style="background-color: {bg_color}; opacity: 0.9; color: white; 
                    padding: 10px; border-radius: 0 0 8px 8px; margin-bottom: 10px;">
                    <div style="display: flex; flex-wrap: wrap; gap: 6px;">"""

                    for item in items:
                        items_html += f"""<div style="background-color: rgba(255,255,255,0.2); 
                        padding: 6px 10px; border-radius: 15px; margin-bottom: 6px;">
                        {item}</div>"""

                    items_html += "</div></div>"
                    st.markdown(items_html, unsafe_allow_html=True)
        else:
            st.markdown(
                """<div style="background-color: #546E7A; color: white; padding: 15px; 
                border-radius: 8px;">No experience information detected.</div>""", 
                unsafe_allow_html=True
            )

def display_formatted_analysis(analysis):
    """
    Format and display the resume analysis in a structured way with improved visibility.

    Args:
        analysis (str): The resume analysis text
    """
    if not analysis:
        return

    # Extract sections using typical patterns
    sections = {
        "Overall Assessment": "",
        "Content Improvements": "",
        "Skills": "",
        "Format Suggestions": "",
        "ATS Optimization": ""
    }

    current_section = None
    lines = analysis.split('\n')

    for line in lines:
        # Check if this line is a section header
        for section in sections.keys():
            if section.lower() in line.lower() or "strength" in line.lower() or "weakness" in line.lower():
                current_section = section
                break

        # Add content to the current section
        if current_section and line:
            sections[current_section] += line + "\n"

    # Display each section in a formatted way with improved visibility
    section_colors = {
        "Overall Assessment": "#3a506b",
        "Content Improvements": "#1b3a4b",
        "Skills": "#006466",
        "Format Suggestions": "#4d194d",
        "ATS Optimization": "#54478c"
    }

    for section, content in sections.items():
        if content.strip():
            st.subheader(section)
            bg_color = section_colors.get(section, "#3a506b")
            st.markdown(
                f"""<div style='background-color: {bg_color}; color: white; 
                padding: 15px; border-radius: 8px; margin-top: 10px; 
                font-size: 16px; line-height: 1.5;'>{content}</div>""", 
                unsafe_allow_html=True
            )

def format_job_description(description):
    """
    Format the job description for better readability with high contrast.

    Args:
        description (str): Job description text

    Returns:
        str: Formatted HTML for the job description
    """
    if not description:
        return """<div style="background-color: #455A64; color: white; padding: 15px; 
                border-radius: 8px; margin-top: 15px;">No description available</div>"""

    # Clean up any problematic formatting
    description = description.replace('\n\n', '<br><br>').replace('\n', '<br>')

    # Wrap the description in a styled div with high contrast
    formatted_description = f"""
    <div style="background-color: #263238; color: white; padding: 15px; 
    border-radius: 8px; margin-top: 15px; line-height: 1.5; font-size: 16px;">
        {description}
    </div>
    """

    return formatted_description

def display_matching_skills(skills, job_description):
    """
    Display skills that match a job description with high-contrast styling.

    Args:
        skills (list): List of skills from resume
        job_description (str): Job description text
    """
    if not skills or not job_description:
        st.markdown(
            """<div style="background-color: #455A64; color: white; padding: 12px; 
            border-radius: 6px;">No matching skills could be determined.</div>""", 
            unsafe_allow_html=True
        )
        return

    job_desc = job_description.lower()

    matching_skills = []
    for skill in skills:
        if skill.lower() in job_desc:
            matching_skills.append(skill)

    if matching_skills:
        st.markdown("""<h4 style="color: #1A237E; margin-bottom: 10px;">Skills Matching Job Description</h4>""", unsafe_allow_html=True)
        skills_html = """<div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 15px;">"""

        for skill in matching_skills[:5]:  # Show top 5 matching skills
            skills_html += f"""<div style="background-color: #01579B; color: white; 
            padding: 8px 12px; border-radius: 20px; font-weight: 500; margin-bottom: 8px;">
            ✅ {skill}</div>"""

        skills_html += "</div>"
        st.markdown(skills_html, unsafe_allow_html=True)
    else:
        st.markdown(
            """<div style="background-color: #455A64; color: white; padding: 12px; 
            border-radius: 6px;">No matching skills detected in the job description.</div>""", 
            unsafe_allow_html=True
        )

    # Identify missing skills
    missing_skills = []
    common_tech_skills = [
        "python", "java", "javascript", "sql", "aws", "azure", 
        "react", "node", "docker", "kubernetes", "machine learning",
        "data science", "agile", "scrum", "git", "ci/cd"
    ]

    for tech in common_tech_skills:
        if tech in job_desc and not any(tech.lower() in s.lower() for s in skills):
            missing_skills.append(tech)

    if missing_skills:
        st.markdown("""<h4 style="color: #B71C1C; margin-bottom: 10px;">Skills to Emphasize or Develop</h4>""", unsafe_allow_html=True)
        missing_html = """<div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 15px;">"""

        for skill in missing_skills[:5]:  # Show top 5 missing skills
            missing_html += f"""<div style="background-color: #C62828; color: white; 
            padding: 8px 12px; border-radius: 20px; font-weight: 500; margin-bottom: 8px;">
            ⚠️ {skill.title()}</div>"""

        missing_html += "</div>"
        st.markdown(missing_html, unsafe_allow_html=True)

def apply_styling():
    """Apply custom CSS styling to the Streamlit app."""
    st.markdown(f"""
    <style>
        /* Global font styling */
        * {{
            font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
        }}

        /* Main header styling */
        h1, h2, .main-header {{
            color: white !important;
            background-color: {COLORS['primary']} !important;
            padding: 20px !important;
            border-radius: 8px !important;
            margin-bottom: 20px !important;
            font-weight: bold !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
        }}

        /* Blue header panels styling */
        div[style*="background-color: {COLORS['primary']}"],
        div[style*="background-color: rgb(28, 78, 128)"],
        [data-testid="stForm"] h3,
        .blue-header {{
            color: white !important;
            font-size: 1.2rem !important;
            font-weight: bold !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
            padding: 15px !important;
            border-radius: 6px !important;
            margin-bottom: 15px !important;
            background-color: {COLORS['primary']} !important;
        }}

        /* Fix for text in blue panels */
        div[style*="background-color: {COLORS['primary']}"] p,
        div[style*="background-color: {COLORS['primary']}"] span,
        div[style*="background-color: {COLORS['primary']}"] h3,
        div[style*="background-color: {COLORS['primary']}"] h4,
        div[style*="background-color: {COLORS['primary']}"] div {{
            color: white !important;
            font-weight: bold !important;
        }}

        /* All form inputs styling */
        input, select, textarea, 
        [data-baseweb="input"], 
        [data-baseweb="select"], 
        [data-baseweb="textarea"] {{
            color: black !important;
            background-color: white !important;
            border: 1px solid #cccccc !important;
            border-radius: 4px !important;
            padding: 8px !important;
        }}

        /* Buttons styled */
        .stButton>button,
        button[kind="primary"] {{
            background-color: {COLORS["accent3"]} !important;
            color: white !important;
            font-weight: bold !important;
            border-radius: 4px !important;
            padding: 0.5rem 1rem !important;
            border: none !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
            transition: all 0.3s ease !important;
            width: 100% !important;
            font-size: 16px !important;
            height: auto !important;
            min-height: 45px !important;
        }}

        .stButton>button:hover,
        button[kind="primary"]:hover {{
            background-color: #E67E22 !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
            transform: translateY(-1px) !important;
        }}

        /* Table styling */
        table, .dataframe, [data-testid="stTable"] {{
            width: 100% !important;
            border-collapse: collapse !important;
            margin-bottom: 20px !important;
            border-radius: 4px !important;
            overflow: hidden !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
        }}

        /* Table headers */
        th, thead tr th {{
            background-color: #222222 !important;
            color: white !important;
            font-weight: bold !important;
            padding: 12px 8px !important;
            text-align: left !important;
            border: none !important;
        }}

        /* Table cells */
        td, tbody tr td {{
            padding: 12px 8px !important;
            border-bottom: 1px solid #EEEEEE !important;
            background-color: white !important;
            color: black !important;
        }}

        /* Alternate row styling */
        tbody tr:nth-child(even) td {{
            background-color: #f9f9f9 !important;
        }}

        /* Tab navigation */
        div[data-baseweb="tab-list"] {{
            gap: 0 !important;
            background-color: {COLORS["background"]} !important;
            padding: 10px !important;
            border-radius: 12px !important;
            display: flex !important;
            justify-content: space-between !important;
            width: 100% !important;
            margin-bottom: 20px !important;
            box-shadow: 0 2px 12px rgba(0,0,0,0.1) !important;
        }}

        div[data-baseweb="tab-list"] button {{
            flex: 1 !important;
            text-align: center !important;
            margin: 0 5px !important;
            height: 60px !important;
            font-size: 16px !important;
            background-color: rgba(255, 255, 255, 0.7) !important;
            color: {COLORS["primary"]} !important;
            border-radius: 8px !important;
            border: 1px solid rgba(0,0,0,0.05) !important;
            transition: all 0.3s ease !important;
        }}

        div[data-baseweb="tab-list"] button[aria-selected="true"] {{
            background-color: {COLORS["primary"]} !important;
            color: white !important;
            border-bottom: 3px solid {COLORS["accent3"]} !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
            transform: translateY(-2px) !important;
        }}

        /* Background colors */
        body {{
            background-color: #FFFFFF !important;
        }}

        .stApp {{
            background-color: #FFFFFF !important;
        }}

        /* Headers inside panels */
        .stExpander h3, .stForm h3 {{
            color: {COLORS["primary"]} !important;
            font-weight: bold !important;
        }}

        /* Expandable sections */
        .stExpander {{
            border: 1px solid #eee !important;
            border-radius: 8px !important;
            overflow: hidden !important;
        }}

        .stExpander details {{
            padding: 0 !important;
        }}

        .stExpander summary {{
            padding: 15px !important;
            background-color: #f5f7fa !important;
            font-weight: bold !important;
            color: {COLORS["primary"]} !important;
        }}
    </style>
    """, unsafe_allow_html=True)