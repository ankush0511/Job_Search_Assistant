# from langchain.llms import OpenAI
from langchain_groq import ChatGroq
from config import GROQ_API_KEY, LLM_MODEL

class ResumeAgent:
    """Agent for analyzing and improving resumes with detailed feedback."""

    def __init__(self):
        """Initialize the resume agent."""
        self.api_key = GROQ_API_KEY
        self.model = LLM_MODEL

    def analyze_resume(self, resume_data):
        """
        Analyze a resume and provide improvement suggestions.

        Args:
            resume_data (dict): The parsed resume data

        Returns:
            str: Detailed analysis and suggestions
        """
        if not self.api_key:
            return self._generate_basic_analysis(resume_data)

        try:
            # Initialize OpenAI client
            client =  ChatGroq(model='gemma2-9b-it')

            # Extract key data for analysis
            skills = resume_data.get("skills", [])
            education = resume_data.get("education", [])
            experience = resume_data.get("experience", [])

            # Create a detailed prompt
            prompt = f"""
            Analyze this resume information and provide specific, actionable suggestions 
            for improvement to make it more competitive in the job market.

            === RESUME DATA ===

            Skills: {", ".join(skills)}

            Education: 
            {chr(10).join([f"- {edu}" for edu in education])}

            Experience:
            {chr(10).join([f"- {exp}" for exp in experience])}

            === ANALYSIS INSTRUCTIONS ===

            Provide a comprehensive analysis with the following clearly labeled sections:

            1. OVERALL ASSESSMENT
            • Strengths: Identify 3-5 strong aspects of the resume
            • Weaknesses: Point out 2-4 areas that need improvement
            • Industry fit: Based on the skills and experience, suggest 2-3 suitable industry sectors or job roles

            2. CONTENT IMPROVEMENTS
            • Achievements: Suggest how to better quantify results (provide 2-3 examples of how to reword vague statements)
            • Skills presentation: Advise on better organization or presentation of technical skills
            • Missing skills: Identify any critical skills that seem to be missing based on the experience described

            3. FORMAT SUGGESTIONS
            • Structure: Suggest optimal resume sections and ordering
            • Length: Advise on appropriate length based on experience level
            • Readability: Provide tips to improve scannability

            4. ATS OPTIMIZATION
            • Keywords: Suggest 5-7 additional keywords to include for better ATS matching
            • Formatting pitfalls: Identify any elements that could harm ATS parsing
            • File format recommendations

            Be extremely specific and actionable in your suggestions. Provide concrete examples where possible.
            Focus on transformative improvements rather than minor tweaks.
            """

            # Get analysis from OpenAI
            response = client.create(
                model=self.model,
                prompt=prompt,
                max_tokens=1500,
                temperature=0.7
            )

            # Return the analysis
            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"Error in resume analysis: {e}")
            return self._generate_basic_analysis(resume_data)

    def _generate_basic_analysis(self, resume_data):
        """Generate basic resume analysis when OpenAI is not available."""
        skills = resume_data.get("skills", [])
        education = resume_data.get("education", [])
        experience = resume_data.get("experience", [])

        analysis = "OVERALL ASSESSMENT\n\n"

        # Basic strengths analysis
        strengths = []
        if len(skills) >= 5:
            strengths.append("Good range of technical skills")
        if len(experience) >= 3:
            strengths.append("Solid work experience")
        if any("machine learning" in skill.lower() or "ai" in skill.lower() for skill in skills):
            strengths.append("Valuable AI/ML skills that are in high demand")

        analysis += "Strengths:\n"
        for strength in strengths or ["Resume contains some relevant skills"]:
            analysis += f"• {strength}\n"

        # Basic weaknesses analysis
        weaknesses = []
        if len(skills) < 5:
            weaknesses.append("Limited range of technical skills listed")
        if not any("python" in skill.lower() for skill in skills):
            weaknesses.append("Python (a widely used programming language) not explicitly listed")

        analysis += "\nWeaknesses:\n"
        for weakness in weaknesses or ["Consider adding more specific technical skills"]:
            analysis += f"• {weakness}\n"

        # Content improvements
        analysis += "\nCONTENT IMPROVEMENTS\n\n"
        analysis += "• Consider quantifying your achievements with specific metrics\n"
        analysis += "• Organize skills by category (programming languages, frameworks, tools)\n"
        analysis += "• Focus on highlighting relevant skills for your target roles\n"

        # Format suggestions
        analysis += "\nFORMAT SUGGESTIONS\n\n"
        analysis += "• Use a clean, ATS-friendly format with clear section headings\n"
        analysis += "• Ensure consistent formatting (bullet points, dates, etc.)\n"
        analysis += "• Keep resume to 1-2 pages maximum\n"

        # ATS optimization
        analysis += "\nATS OPTIMIZATION\n\n"
        analysis += "• Use keywords from job descriptions in your resume\n"
        analysis += "• Save your resume as a PDF to maintain formatting\n"
        analysis += "• Avoid tables, headers/footers, and images that can confuse ATS systems\n"

        return analysis