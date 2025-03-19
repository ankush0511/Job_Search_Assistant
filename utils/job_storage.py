# 


import os
import json
from datetime import datetime

# Create directory for saved jobs
os.makedirs("saved_jobs", exist_ok=True)

class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder for datetime objects."""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        return super().default(obj)

def save_job_to_local(job_data):
    """Save job data to a local JSON file with proper datetime handling.

    Args:
        job_data (dict): The job data to save

    Returns:
        str: Path to the saved file
    """
    # Generate a unique filename based on job title, company, and timestamp
    job_id = f"{job_data['title'].replace(' ', '_')}_{job_data['company'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    file_path = os.path.join("saved_jobs", f"{job_id}.json")

    # Add timestamp
    job_data["date_saved"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create a copy of job_data to avoid modifying the original
    job_data_copy = job_data.copy()

    # Process the dictionary to convert datetime objects to strings
    for key, value in job_data_copy.items():
        if isinstance(value, datetime):
            job_data_copy[key] = value.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(value, dict):
            # Handle nested dictionaries
            process_dict_datetime(value)

    # Save the job data to a JSON file with custom encoder for any missed datetime objects
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(job_data_copy, f, indent=4, cls=DateTimeEncoder)

    return file_path

def process_dict_datetime(d):
    """Process a dictionary to convert all datetime objects to strings."""
    for key, value in list(d.items()):  # Use list to avoid dictionary size change during iteration
        if isinstance(value, datetime):
            d[key] = value.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(value, dict):
            process_dict_datetime(value)
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, datetime):
                    value[i] = item.strftime("%Y-%m-%d %H:%M:%S")
                elif isinstance(item, dict):
                    process_dict_datetime(item)

def load_saved_jobs():
    """Load all saved jobs from local storage with error handling.

    Returns:
        list: List of job dictionaries
    """
    saved_jobs = []

    if not os.path.exists("saved_jobs"):
        return saved_jobs

    for file_name in os.listdir("saved_jobs"):
        if file_name.endswith(".json"):
            file_path = os.path.join("saved_jobs", file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    job_data = json.load(f)
                    saved_jobs.append(job_data)
            except Exception as e:
                print(f"Error loading job file {file_name}: {e}")

    return saved_jobs

def remove_saved_job(job_title, job_company):
    """Remove a saved job from local storage.

    Args:
        job_title (str): Title of the job to remove
        job_company (str): Company of the job to remove

    Returns:
        bool: True if the job was successfully removed, False otherwise
    """
    for file_name in os.listdir("saved_jobs"):
        if file_name.endswith(".json"):
            file_path = os.path.join("saved_jobs", file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    job_data = json.load(f)

                if job_data.get("title") == job_title and job_data.get("company") == job_company:
                    os.remove(file_path)
                    return True
            except Exception as e:
                print(f"Error processing job file {file_name}: {e}")

    return False