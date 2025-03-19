



import re
from collections import Counter

class ResumeKeywordExtractor:
    """
    A class to extract relevant keywords from a resume for job search purposes.
    This extracts technical skills, experience-related keywords, and potential job titles.
    """

    def __init__(self):
        """Initialize the keyword extractor with common technical terms."""
        # Common technical skills to look for
        self.tech_keywords = {
            "languages": [
                "python", "java", "javascript", "typescript", "c++", "c#", "ruby", 
                "go", "rust", "swift", "kotlin", "php", "scala", "perl", "r", 
                "html", "css", "sql"
            ],
            "frameworks": [
                "react", "angular", "vue", "django", "flask", "spring", "express", 
                "rails", "laravel", "asp.net", "bootstrap", "jquery", "tensorflow",
                "pytorch", "keras", "scikit-learn", "pandas", "numpy"
            ],
            "platforms": [
                "aws", "azure", "gcp", "google cloud", "heroku", "docker", "kubernetes",
                "jenkins", "gitlab", "github", "bitbucket", "linux", "windows", "mac",
                "ios", "android"
            ],
            "concepts": [
                "api", "rest", "graphql", "microservices", "ci/cd", "agile", "scrum",
                "devops", "testing", "unit testing", "integration testing", "git",
                "version control", "database", "sql", "nosql", "machine learning",
                "deep learning", "data science", "big data", "blockchain", "cloud",
                "security", "authentication", "authorization"
            ]
        }

        # Common job titles
        self.job_titles = [
            "software engineer", "software developer", "web developer", "frontend developer",
            "backend developer", "full stack developer", "data scientist", "data analyst",
            "machine learning engineer", "devops engineer", "site reliability engineer",
            "cloud engineer", "systems administrator", "database administrator",
            "quality assurance engineer", "qa engineer", "product manager", "project manager",
            "ux designer", "ui designer", "graphic designer", "network engineer",
            "security engineer", "business analyst", "data engineer", "solutions architect",
            "technical lead", "engineering manager", "cto", "cio", "ceo"
        ]

        # Additional stopwords specific to resumes
        self.resume_stopwords = [
            "resume", "curriculum", "vitae", "cv", "objective", "summary", "experience",
            "education", "skills", "references", "projects", "achievements", "responsibilities",
            "phone", "email", "address", "linkedin", "github", "portfolio", "website",
            "a", "an", "the", "and", "but", "or", "for", "nor", "on", "at", "to", "from",
            "by", "with", "in", "out", "over", "under", "again", "further", "then",
            "once", "here", "there", "when", "where", "why", "how", "all", "any",
            "both", "each", "few", "more", "most", "other", "some", "such", "no",
            "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s",
            "t", "can", "will", "just", "don", "should", "now"
        ]

    def extract_keywords(self, resume_data, max_keywords=10):
        """
        Extract the most relevant keywords from resume data for job searching.

        Args:
            resume_data (dict): The parsed resume data containing fields like skills, experience, etc.
            max_keywords (int): The maximum number of keywords to return

        Returns:
            list: A list of keywords relevant for job searching
        """
        if not resume_data:
            return []

        # Initialize a list to store all potential keywords
        all_text = []

        # Add skills directly (these are already identified as important)
        skills = resume_data.get("skills", [])
        all_text.extend(skills)

        # Process experience to extract important terms
        experience = resume_data.get("experience", [])
        experience_text = " ".join(experience)

        # Tokenize experience text
        try:
            # Simple word extraction using regex
            experience_words = re.findall(r'\b\w+\b', experience_text.lower())
            experience_words = [word for word in experience_words if word not in self.resume_stopwords and len(word) > 2]
            all_text.extend(experience_words)
        except Exception as e:
            print(f"Error processing experience: {e}")

        # Add education keywords
        education = resume_data.get("education", [])
        education_text = " ".join(education)
        education_words = re.findall(r'\b\w+\b', education_text.lower())
        education_words = [word for word in education_words if word not in self.resume_stopwords and len(word) > 2]
        all_text.extend(education_words)

        # Check for technical keywords that appear in the resume
        technical_terms = []
        for category, terms in self.tech_keywords.items():
            for term in terms:
                # Check if term appears in the skills or experience
                if term in " ".join(all_text).lower():
                    technical_terms.append(term)

        # Add any detected technical terms
        all_text.extend(technical_terms)

        # Count the frequency of each term
        keyword_counter = Counter(all_text)

        # Get the most common keywords, prioritizing skills and technical terms
        # First add all skills
        final_keywords = []
        for skill in skills:
            if skill.lower() not in [k.lower() for k in final_keywords]:
                final_keywords.append(skill)
                if len(final_keywords) >= max_keywords:
                    return final_keywords

        # Then add technical terms not already included
        for term in technical_terms:
            if term.lower() not in [k.lower() for k in final_keywords]:
                final_keywords.append(term)
                if len(final_keywords) >= max_keywords:
                    return final_keywords

        # Then add the most common remaining terms
        for keyword, _ in keyword_counter.most_common(max_keywords * 2):  # Get more than needed to filter
            if len(final_keywords) >= max_keywords:
                break
            if keyword.lower() not in [k.lower() for k in final_keywords]:
                final_keywords.append(keyword)

        return final_keywords

    def extract_job_title(self, resume_data):
        """
        Extract the most likely job title from the resume data.

        Args:
            resume_data (dict): The parsed resume data

        Returns:
            str: The most likely job title
        """
        if not resume_data:
            return "software engineer"  # Default fallback

        # Look for title in experience
        experience = resume_data.get("experience", [])
        experience_text = " ".join(experience).lower()

        # Check if any job titles appear in the experience
        matching_titles = []
        for title in self.job_titles:
            if title in experience_text:
                matching_titles.append(title)

        if matching_titles:
            # Return the longest matching title (usually more specific)
            return max(matching_titles, key=len)

        # If no title found, infer from skills
        skills = resume_data.get("skills", [])
        skills_text = " ".join(skills).lower()

        # Check for data science/ML keywords
        data_science_terms = ["data science", "machine learning", "ai", "artificial intelligence", 
                              "deep learning", "statistics", "python", "r", "tensorflow", "pytorch"]
        if any(term in skills_text for term in data_science_terms):
            return "data scientist"

        # Check for frontend keywords
        frontend_terms = ["frontend", "front-end", "react", "angular", "vue", "javascript", 
                          "html", "css", "ui", "ux", "design"]
        if any(term in skills_text for term in frontend_terms):
            return "frontend developer"

        # Check for backend keywords
        backend_terms = ["backend", "back-end", "server", "api", "database", "sql", 
                         "nosql", "django", "flask", "node", "express", "spring"]
        if any(term in skills_text for term in backend_terms):
            return "backend developer"

        # Check for devops keywords
        devops_terms = ["devops", "aws", "azure", "gcp", "cloud", "docker", "kubernetes", 
                        "ci/cd", "jenkins", "deployment", "infrastructure"]
        if any(term in skills_text for term in devops_terms):
            return "devops engineer"

        # Default to software engineer as a safe fallback
        return "software engineer"