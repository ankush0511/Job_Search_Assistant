
# from langchain.llms import OpenAI
from langchain_groq import ChatGroq
from config import GROQ_API_KEY, LLM_MODEL

class InterviewAgent:
    """Agent for interview preparation and question generation."""

    def __init__(self):
        """Initialize the interview agent."""
        self.api_key = GROQ_API_KEY
        self.model = LLM_MODEL

    def generate_interview_questions(self, job_data, resume_data=None, question_count=10):
        """
        Generate interview questions based on job description and resume.

        Args:
            job_data (dict): The job listing data
            resume_data (dict, optional): The parsed resume data
            question_count (int): Number of questions to generate

        Returns:
            list: List of question dictionaries with context, tips, and suggested answers
        """
        if not self.api_key:
            return self._generate_basic_questions(job_data, question_count)

        try:
            # Initialize OpenAI client
            client =  ChatGroq(model='gemma2-9b-it')

            # Extract job details
            job_title = job_data.get('title', 'Unknown Position')
            job_company = job_data.get('company', 'Unknown Company')
            job_description = job_data.get('description', '')

            # Extract customization options if provided
            interview_customization = job_data.get('interview_customization', '')

            # Extract skills from resume if available
            skills = []
            if resume_data and "skills" in resume_data:
                skills = resume_data.get("skills", [])

            # Create a detailed prompt
            prompt = f"""
            Generate {question_count} interview questions for the following job:

            Job Title: {job_title}
            Company: {job_company}

            Job Description:
            {job_description}

            {interview_customization}

            Candidate Skills: {', '.join(skills) if skills else 'Not provided'}

            Include a mix of:
            1. Technical questions specific to the role
            2. Behavioral questions relevant to this position
            3. Problem-solving questions
            4. Job-specific knowledge questions

            For each question, please provide:
            1. The question itself
            2. Context for why this question matters
            3. Tips for answering effectively
            4. A suggested answer structure or example

            Format each question as a JSON object:

            {{
                "question": "The actual interview question",
                "context": "Why this question is asked and what it's testing",
                "tips": "How to approach answering this question",
                "suggested_answer": "An example or structure for an effective answer"
            }}

            Return the questions as a JSON array of these objects.
            """

            # Get questions from OpenAI
            response = client.create(
                model=self.model,
                prompt=prompt,
                max_tokens=2500,
                temperature=0.7
            )

            # Parse the response as JSON
            try:
                import json
                import re

                content = response.choices[0].message.content.strip()

                # First try to parse as direct JSON
                try:
                    questions = json.loads(content)
                    return questions
                except json.JSONDecodeError:
                    # If that fails, try to extract JSON array pattern
                    json_pattern = r'\[\s*\{.*\}\s*\]'
                    json_match = re.search(json_pattern, content, re.DOTALL)

                    if json_match:
                        questions = json.loads(json_match.group(0))
                        return questions
                    else:
                        # If still can't parse, create structured questions from the text
                        # Split by numbered patterns like "1.", "2.", etc.
                        question_blocks = re.split(r'\n\s*\d+\.', content)

                        # Remove the intro text if present
                        if not re.match(r'\s*\{', question_blocks[0]):
                            question_blocks = question_blocks[1:]

                        questions = []
                        for block in question_blocks:
                            if not block.strip():
                                continue

                            # Try to extract parts from the block
                            question_match = re.search(r'["\']?question["\']?\s*:\s*["\'](.+?)["\']', block, re.IGNORECASE | re.DOTALL)
                            context_match = re.search(r'["\']?context["\']?\s*:\s*["\'](.+?)["\']', block, re.IGNORECASE | re.DOTALL)
                            tips_match = re.search(r'["\']?tips["\']?\s*:\s*["\'](.+?)["\']', block, re.IGNORECASE | re.DOTALL)
                            answer_match = re.search(r'["\']?suggested_answer["\']?\s*:\s*["\'](.+?)["\']', block, re.IGNORECASE | re.DOTALL)

                            question_obj = {}
                            if question_match:
                                question_obj["question"] = question_match.group(1).strip()
                            else:
                                # If we can't find a clear pattern, use the whole block as the question
                                question_obj["question"] = block.strip()

                            if context_match:
                                question_obj["context"] = context_match.group(1).strip()
                            if tips_match:
                                question_obj["tips"] = tips_match.group(1).strip()
                            if answer_match:
                                question_obj["suggested_answer"] = answer_match.group(1).strip()

                            questions.append(question_obj)

                        return questions
            except Exception as parse_error:
                print(f"Error parsing questions: {parse_error}")
                # Return the raw text as a fallback
                return [{"question": response.choices[0].message.content.strip()}]

        except Exception as e:
            print(f"Error generating interview questions: {e}")
            return self._generate_basic_questions(job_data, question_count)

    def _generate_basic_questions(self, job_data, question_count=10):
        """Generate basic interview questions when OpenAI is not available."""
        job_title = job_data.get('title', 'this position').lower()

        # Prepare some general questions based on job title
        general_questions = [
            {"question": "Tell me about yourself and your experience.", 
             "tips": "Keep it professional and relevant to the role."},

            {"question": "Why are you interested in this position?", 
             "tips": "Research the company and connect the role to your career goals."},

            {"question": "What are your strengths and weaknesses?", 
             "tips": "Be honest about weaknesses but focus on how you're addressing them."},

            {"question": f"Describe a challenging situation you faced in your previous role and how you handled it.",
             "tips": "Use the STAR method: Situation, Task, Action, Result."},

            {"question": "Where do you see yourself in 5 years?", 
             "tips": "Show ambition while being realistic about career progression."}
        ]

        # Add some role-specific questions
        if "developer" in job_title or "engineer" in job_title:
            technical_questions = [
                {"question": "Can you describe your experience with modern development tools and practices?",
                 "tips": "Mention version control, CI/CD, code review, and testing practices."},

                {"question": "How do you keep your technical skills current?",
                 "tips": "Discuss learning resources, side projects, or communities you're part of."},

                {"question": "Describe a complex technical problem you solved recently.",
                 "tips": "Explain your thought process and the steps you took to solve it."},

                {"question": "How do you approach debugging a complex issue?",
                 "tips": "Describe your systematic approach to problem solving."},

                {"question": "How do you ensure code quality in your projects?",
                 "tips": "Mention testing, code reviews, and adherence to standards."}
            ]
            questions = general_questions + technical_questions

        elif "data" in job_title or "analyst" in job_title:
            data_questions = [
                {"question": "Describe a complex data analysis you performed and the insights you derived.",
                 "tips": "Focus on the business impact of your analysis."},

                {"question": "Which data visualization tools are you comfortable using?",
                 "tips": "Mention specific tools and how you've used them effectively."},

                {"question": "How do you ensure the accuracy of your data analysis?",
                 "tips": "Discuss data validation techniques and quality checks."},

                {"question": "How do you explain complex data insights to non-technical stakeholders?",
                 "tips": "Emphasize your communication skills and ability to translate technical concepts."},

                {"question": "Describe your experience with SQL and database querying.",
                 "tips": "Provide specific examples of complex queries you've written."}
            ]
            questions = general_questions + data_questions

        elif "manager" in job_title or "lead" in job_title:
            leadership_questions = [
                {"question": "How do you motivate team members?",
                 "tips": "Discuss your leadership style and specific motivation strategies."},

                {"question": "Describe how you handle conflicts within your team.",
                 "tips": "Provide a specific example using the STAR method."},

                {"question": "How do you prioritize tasks when managing multiple projects?",
                 "tips": "Explain your project management approach and prioritization criteria."},

                {"question": "Tell me about a time when you had to make a difficult decision as a leader.",
                 "tips": "Focus on your decision-making process and the outcome."},

                {"question": "How do you provide feedback to team members?",
                 "tips": "Discuss both positive feedback and constructive criticism approaches."}
            ]
            questions = general_questions + leadership_questions

        else:
            # Default to general professional questions
            professional_questions = [
                {"question": "How do you prioritize your work when dealing with multiple deadlines?",
                 "tips": "Explain your time management strategies and how you handle pressure."},

                {"question": "Describe a situation where you had to adapt to a significant change at work.",
                 "tips": "Show your flexibility and resilience when facing change."},

                {"question": "How do you approach working in a team versus working independently?",
                 "tips": "Demonstrate your ability to collaborate and work autonomously as needed."},

                {"question": "Tell me about a time when you went above and beyond in your role.",
                 "tips": "Highlight your work ethic and commitment to excellence."},

                {"question": "How do you handle feedback or criticism?",
                 "tips": "Show that you're open to growth and can turn feedback into improvement."}
            ]
            questions = general_questions + professional_questions

        # Return only the requested number of questions
        return questions[:question_count]