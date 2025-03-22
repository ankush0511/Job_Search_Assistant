import spacy
import os
import tempfile
import re
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS
# from langchain.embeddings import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from config import GROQ_API_KEY
import spacy
from spacy.cli.download import download

def load_spacy_model(model_name="en_core_web_lg"):
    try:
        return spacy.load(model_name)
    except OSError:
        download(model_name)  # Download the model programmatically
        return spacy.load(model_name)

nlp = load_spacy_model()

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_lg")
except:
    os.system("python -m spacy download en_core_web_lg")
    nlp = spacy.load("en_core_web_lg")

class ResumeParser:
    """Enhanced tool for parsing resume files and extracting structured information."""

    def __init__(self):
        """Initialize the parser with GROQ_API_KEY components for RAG if API key is provided."""
        self.use_rag = False
        if GROQ_API_KEY:
            try:
                self.embeddings = OllamaEmbeddings(
    model="llama3",
)
                self.llm =  ChatGroq(model='gemma2-9b-it')
                self.use_rag = True
            except Exception as e:
                print(f"Error initializing Groq components: {e}")
                self.use_rag = False

    def save_uploaded_file(self, uploaded_file):
        """Save an uploaded file to a temporary location."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp:
            tmp.write(uploaded_file.getbuffer())
            return tmp.name

    def parse_resume(self, text):
        """
        Parse a resume text and extract structured information.

        Args:
            text (str): The raw text content of the resume

        Returns:
            dict: Structured information from the resume
        """
        if not text:
            return None

        # Extract structured information
        structured_data = self.extract_information(text)

        return structured_data

    def extract_information(self, text):
        """Extract structured information from resume text."""
        doc = nlp(text)

        # Initialize categories
        skills = []
        education = []
        experience = []
        contact_info = {"email": "", "phone": ""}

        # Extract email and phone using regex
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            contact_info["email"] = emails[0]

        phone_pattern = r'\b(?:\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b'
        phones = re.findall(phone_pattern, text)
        if phones:
            contact_info["phone"] = phones[0]

        # Extract skills using NER and keyword matching
        skill_keywords = [
            # Technical skills
            "python", "java", "javascript", "react", "angular", "vue", "node.js",
            "sql", "nosql", "mongodb", "mysql", "postgresql", "aws", "azure", "gcp",
            "docker", "kubernetes", "terraform", "ci/cd", "jenkins", "git",
            "machine learning", "deep learning", "nlp", "computer vision", "data science",
            "data analysis", "data visualization", "tableau", "power bi", "excel",
            "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy", 
            "hadoop", "spark", "airflow", "kubernetes", "docker", "rest api",

            # Cloud and DevOps
            "aws", "azure", "gcp", "google cloud", "cloud computing", "serverless",
            "lambda", "ec2", "s3", "dynamodb", "devops", "ci/cd", "jenkins", "github actions",
            "terraform", "ansible", "puppet", "chef", "kubernetes", "docker", "microservices",

            # Web Development
            "html", "css", "javascript", "typescript", "react", "angular", "vue", 
            "node.js", "express", "django", "flask", "spring", "asp.net", "php",
            "laravel", "ruby on rails", "rest api", "graphql", "responsive design",

            # Database
            "sql", "mysql", "postgresql", "mongodb", "nosql", "oracle", "database design",
            "data modeling", "etl", "data warehousing", "redis", "elasticsearch",

            # Soft skills
            "project management", "agile", "scrum", "jira", "confluence",
            "leadership", "team management", "communication", "problem-solving",
            "critical thinking", "teamwork", "time management", "stakeholder management"
        ]

        # Use RAG to extract skills more comprehensively if available
        extracted_skills = set()

        # First, extract skills by keyword matching
        for skill in skill_keywords:
            if skill.lower() in text.lower():
                extracted_skills.add(skill)

        # Use spaCy to find additional skills (entities tagged as ORG or PRODUCT often correspond to technologies)
        for ent in doc.ents:
            if ent.label_ in ("ORG", "PRODUCT"):
                # Check if it might be a skill/technology rather than just a company
                tech_indicators = ["framework", "language", "library", "tool", "platform", "software", "system", "technology"]
                context = text[max(0, ent.start_char - 50):min(len(text), ent.end_char + 50)].lower()

                if any(indicator in context for indicator in tech_indicators):
                    extracted_skills.add(ent.text)

        # Add the extracted skills to the skills list
        skills = list(extracted_skills)

        # Extract education entities
        education_keywords = ["university", "college", "institute", "school", "academy", "bachelor", 
                             "master", "phd", "degree", "diploma", "certificate", "certification"]

        education_pattern = r'(?:(?:Bachelor|Master|PhD|B\.S\.|M\.S\.|M\.B\.A\.|B\.A\.|B\.Sc\.|M\.Sc\.|B\.Tech|M\.Tech)\s+(?:of|in)\s+[A-Za-z\s]+)|(?:[A-Za-z\s]+University|College|Institute)'
        education_matches = re.findall(education_pattern, text)
        for match in education_matches:
            education.append(match.strip())

        for ent in doc.ents:
            if ent.label_ == "ORG":
                # Check if it's likely an educational institution
                if any(edu_term in ent.text.lower() for edu_term in education_keywords):
                    # Get surrounding context to capture degree information
                    context_start = max(0, ent.start_char - 100)
                    context_end = min(len(text), ent.end_char + 100)
                    context = text[context_start:context_end]

                    # Add the education entity with surrounding context if not already in the list
                    if not any(ent.text in edu for edu in education):
                        education.append(context.strip())

        # Extract experience - look for companies and job titles
        job_title_keywords = [
            "engineer", "developer", "manager", "director", "analyst", "specialist",
            "consultant", "coordinator", "administrator", "architect", "designer",
            "scientist", "head", "lead", "senior", "junior", "intern", "officer"
        ]

        # Extract work experience blocks
        experience_blocks = []
        exp_headers = ["experience", "work experience", "professional experience", "employment history"]

        # Find experience section in the resume
        text_lower = text.lower()
        for header in exp_headers:
            if header in text_lower:
                # Find the section start
                section_start = text_lower.find(header)
                if section_start != -1:
                    # Look for the next section header or end of text
                    next_section_keywords = ["education", "skills", "projects", "certifications", "references"]
                    next_section_start = float('inf')

                    for next_header in next_section_keywords:
                        pos = text_lower.find(next_header, section_start + len(header))
                        if pos != -1 and pos < next_section_start:
                            next_section_start = pos

                    if next_section_start == float('inf'):
                        next_section_start = len(text)

                    # Extract experience section
                    exp_section = text[section_start:next_section_start].strip()

                    # Split into potential job blocks (using heuristics like dates or company names)
                    date_pattern = r'\b(Jan|January|Feb|February|Mar|March|Apr|April|May|Jun|June|Jul|July|Aug|August|Sep|September|Oct|October|Nov|November|Dec|December|\d{1,2}/\d{1,2}|\d{4})[-\s]+(to|-)[-\s]+(Jan|January|Feb|February|Mar|March|Apr|April|May|Jun|June|Jul|July|Aug|August|Sep|September|Oct|October|Nov|November|Dec|December|\d{1,2}/\d{1,2}|\d{4}|Present|present|Current|current)\b'

                    date_matches = list(re.finditer(date_pattern, exp_section))
                    if date_matches:
                        for i, match in enumerate(date_matches):
                            start_pos = match.start()

                            # Find the end of this job entry (start of next one or end of section)
                            if i < len(date_matches) - 1:
                                end_pos = date_matches[i+1].start()
                            else:
                                end_pos = len(exp_section)

                            # Extract the job block
                            job_block = exp_section[start_pos:end_pos].strip()
                            experience_blocks.append(job_block)

        # If we found specific experience blocks, use them
        if experience_blocks:
            for block in experience_blocks:
                experience.append(block)
        else:
            # Fallback to entity-based experience extraction
            for ent in doc.ents:
                if ent.label_ == "ORG" and not any(edu_term in ent.text.lower() for edu_term in education_keywords):
                    # Check if it might be a company by looking for job titles nearby
                    context_start = max(0, ent.start_char - 150)
                    context_end = min(len(text), ent.end_char + 150)
                    context = text[context_start:context_end]

                    if any(title in context.lower() for title in job_title_keywords):
                        # Add the experience context if not already in the list
                        if not any(ent.text in exp for exp in experience):
                            experience.append(context.strip())

        # If using RAG, enhance the extraction with contextual understanding
        if self.use_rag:
            try:
                # Create embeddings from the resume text
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200
                )
                texts = text_splitter.split_text(text)

                # Create the vectorstore
                vectorstore = FAISS.from_texts(texts, self.embeddings)

                # Create the retrieval chain
                retriever = vectorstore.as_retriever()
                qa_chain = RetrievalQA.from_chain_type(
                    llm=self.llm,
                    chain_type="stuff",
                    retriever=retriever
                )

                # Extract skills using RAG
                rag_skills_response = qa_chain.run("What are all the technical skills, programming languages, and tools mentioned in this resume? List only the names of the skills without explanations.")
                if rag_skills_response:
                    # Process the response, assuming it's a list or comma-separated skills
                    rag_skills = [s.strip() for s in re.split(r'[,\n•-]', rag_skills_response) if s.strip()]
                    for skill in rag_skills:
                        if skill and len(skill) < 50:  # Avoid adding long text chunks as skills
                            extracted_skills.add(skill)

                # Extract education using RAG
                rag_education_response = qa_chain.run("Extract all education details including institutions, degrees, majors, and graduation dates from this resume.")
                if rag_education_response:
                    # Process the education information
                    rag_education = [e.strip() for e in rag_education_response.split('\n') if e.strip()]
                    for edu in rag_education:
                        if edu and not any(edu in existing_edu for existing_edu in education):
                            education.append(edu)

                # Extract work experience using RAG
                rag_experience_response = qa_chain.run("Extract all work experience details including company names, job titles, dates, and key responsibilities from this resume.")
                if rag_experience_response:
                    # Process the experience information
                    rag_experience = [e.strip() for e in rag_experience_response.split('\n') if e.strip()]
                    for exp in rag_experience:
                        if exp and len(exp) > 20 and not any(exp in existing_exp for existing_exp in experience):
                            experience.append(exp)

            except Exception as e:
                print(f"RAG extraction error: {e}")

        return {
            "raw_text": text,
            "skills": list(set(skills)),
            "education": list(set(education)),
            "experience": list(set(experience)),
            "contact_info": contact_info
        }