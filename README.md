# 🧠 Job Search Assistant

A powerful, AI-powered assistant designed to streamline your job hunting experience—from scraping job listings to tailoring resumes and preparing for interviews.

## 🚀 Features

* 🔍 **Job Search Automation**: Uses SERP API and scraping utilities to find job listings relevant to your profile.
* 🧾 **Resume Analysis**: Parses and analyzes your resume to match jobs and suggest improvements.
* 🗝️ **Keyword Extraction**: Automatically extracts key skills from resumes for better job targeting.
* 💬 **Interview Preparation Agent**: Helps generate potential interview questions and ideal answers based on the job profile.
* 🤖 **Modular Agents Architecture**: Cleanly separated components for job search, resume parsing, and interview prep.

---

## 🗂️ Project Structure

```
Job_Search_Assistant/
│
├── app.py                     # Main entry point for running the assistant
├── config.py                  # Configuration and API key management
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (API keys)
├── ui_utils.py                # UI-related utilities
│
├── agents/                    # Modular agents
│   ├── job_search_agent.py       # Searches and ranks jobs using SERP API
│   ├── resume_agent.py           # Handles resume parsing and keyword extraction
│   └── interview_agent.py        # Prepares interview Q&A
│
└── utils/                     # Core utility functions
    ├── job_scraper.py            # Scrapes job listings
    ├── job_storage.py            # Stores job listings persistently
    ├── resume_parser.py          # Parses resume text using libraries like PDFMiner
    ├── resume_keyword_extractor.py  # Extracts relevant keywords from resumes
    └── serp_api_searcher.py      # Searches for jobs via SERP API
```

---

## 🛠️ Installation

1. **Clone the repository**

```bash
git clone https://github.com/ankush0511/Job_Search_Assistant.git
cd Job_Search_Assistant
```

2. **Create virtual environment (optional but recommended)**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment**

Create a `.env` file in the root directory and add the following:

```env
SERP_API_KEY=your_serp_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

---

## 🧪 Usage

Run the main app:

```bash
python app.py
```

The application will begin parsing resumes, fetching job listings, and preparing interview prompts as per the agent configurations.

---

## 💡 Example Workflow

1. Parse your resume via `resume_agent`
2. Search for relevant jobs using `job_search_agent`
3. Store and review job listings
4. Use `interview_agent` to prepare customized interview questions

---

## 📦 Dependencies

* `openai`
* `requests`
* `pdfminer.six`
* `python-dotenv`
* `serpapi`
* And more in `requirements.txt`

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙋‍♂️ Author

Developed by [Ankush](https://github.com/ankush0511)

