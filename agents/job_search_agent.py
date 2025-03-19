

# from langchain.llms import OpenAI
from langchain_groq import ChatGroq
from utils.job_scraper import JobScraper
from utils.serp_api_searcher import SerpApiSearcher
from config import GROQ_API_KEY, LLM_MODEL, JOB_PLATFORMS

class JobSearchAgent:
    """Agent for searching and matching jobs."""

    def __init__(self):
        """Initialize the job search agent."""
        self.api_key = GROQ_API_KEY
        self.model = LLM_MODEL
        self.job_scraper = JobScraper()
        self.serp_api_searcher = SerpApiSearcher()

    def search_jobs(self, resume_data, keywords, location, platforms=None, count=5):
        """
        Search for jobs based on resume and keywords.

        Args:
            resume_data (dict): The parsed resume data
            keywords (str): Search keywords or job title
            location (str): Job location
            platforms (list): List of job platforms to search
            count (int): Number of jobs per platform

        Returns:
            list: List of job dictionaries
        """
        if not platforms:
            platforms = JOB_PLATFORMS

        # Try the SerpAPI approach first (this will have real links)
        api_jobs = []

        for platform in platforms:
            # Use SerpAPI to search for real jobs
            platform_jobs = self.serp_api_searcher.search_jobs(
                keywords, 
                location, 
                platform=platform, 
                count=count
            )
            api_jobs.extend(platform_jobs)

        # If we got results from SerpAPI, use those
        if api_jobs:
            return api_jobs

        # Fallback to the scraper if SerpAPI fails
        print("SerpAPI search returned no results. Falling back to scraper.")
        all_jobs = []
        for platform in platforms:
            platform_jobs = self.job_scraper.search_jobs(
                keywords, 
                location, 
                platform=platform, 
                count=count
            )
            all_jobs.extend(platform_jobs)

        return all_jobs

    def get_job_match_analysis(self, resume_data, job_data):
        """
        Analyze how well a resume matches a job description.

        Args:
            resume_data (dict): The parsed resume data
            job_data (dict): The job listing data

        Returns:
            dict: Match analysis with score and recommendations
        """
        if not self.api_key:
            return self._generate_basic_match_analysis(resume_data, job_data)

        try:
            # Initialize OpenAI client
            client =  ChatGroq(model='gemma2-9b-it')

            # Extract relevant data
            skills = resume_data.get("skills", [])
            experience = resume_data.get("experience", [])
            job_title = job_data.get("title", "")
            job_description = job_data.get("description", "")

            # Create a prompt for matching analysis
            prompt = f"""
            Analyze how well this resume matches the job description and provide a detailed match analysis.

            === RESUME DATA ===
            Skills: {", ".join(skills)}

            Experience:
            {chr(10).join([f"- {exp}" for exp in experience])}

            === JOB DATA ===
            Title: {job_title}

            Description:
            {job_description}

            === ANALYSIS INSTRUCTIONS ===

            Provide a match analysis with the following components:

            1. MATCH SCORE: Calculate a percentage match (0-100%) based on how well the resume matches the job requirements.

            2. KEY MATCHES: List 3-5 specific skills or experiences from the resume that align well with the job requirements.

            3. GAPS: Identify 2-4 requirements in the job description that are not clearly demonstrated in the resume.

            4. RECOMMENDATIONS: Suggest 3-5 specific actions the candidate can take to better position themselves for this role.

            Format your response as a JSON with the following structure:
            {{
                "match_score": 85,
                "key_matches": ["match1", "match2", ...],
                "gaps": ["gap1", "gap2", ...],
                "recommendations": ["rec1", "rec2", ...]
            }}

            Ensure your analysis is specific, objective, and focused on the actual content in the resume and job description.
            """

            # Get analysis from OpenAI
            response = client.create(
                model=self.model,
                prompt=prompt,
                max_tokens=1000,
                temperature=0.5
            )

            # Parse the response as JSON
            try:
                import json
                analysis = json.loads(response.choices[0].message.content.strip())
                return analysis
            except json.JSONDecodeError:
                # If JSON parsing fails, return the raw text
                return {"match_analysis": response.choices[0].message.content.strip()}

        except Exception as e:
            print(f"Error in job match analysis: {e}")
            return self._generate_basic_match_analysis(resume_data, job_data)

    def _generate_basic_match_analysis(self, resume_data, job_data):
        """Generate basic job match analysis when OpenAI is not available."""
        skills = resume_data.get("skills", [])
        job_description = job_data.get("description", "").lower()

        # Count matching skills
        matching_skills = [skill for skill in skills if skill.lower() in job_description]

        # Calculate a simple match score
        match_score = min(len(matching_skills) * 10, 100) if skills else 50

        return {
            "match_score": match_score,
            "key_matches": matching_skills[:5],
            "gaps": ["Unable to analyze gaps without AI processing"],
            "recommendations": [
                "Review the job description and identify key requirements",
                "Customize your resume to highlight relevant skills and experience",
                "Add any missing skills that you possess but aren't in your resume"
            ]
        }