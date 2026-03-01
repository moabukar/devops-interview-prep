"""
Configuration and constants - Smart path detection
"""
import os
from pathlib import Path

# Application info
APP_NAME = "DevOps Interview Prep"
VERSION = "1.1.0"

# Smart path detection for questions file
def _get_questions_file_path():
    """
    Smart path detection that works both locally and in Docker container
    """
    # Possible locations for the questions file
    possible_paths = [
        # Local development (from project root)
        "data/questions/interview_questions.json",
        # Docker container
        "/app/data/questions/interview_questions.json",
        # Relative from current working directory
        "./data/questions/interview_questions.json",
        # Relative from package directory
        Path(__file__).parent.parent.parent.parent / "data" / "questions" / "interview_questions.json"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return str(path)
    
    # Fallback to default relative path
    return "data/questions/interview_questions.json"

# File paths
DEFAULT_QUESTIONS_FILE = _get_questions_file_path()
PROGRESS_DIR = Path.home() / ".devops-ip"
PROGRESS_FILE = PROGRESS_DIR / "progress.json"

# Progress tracking settings
MIN_ATTEMPTS_FOR_WEAK_AREAS = 1
MAX_WEAK_AREAS_SHOWN = 5
DEFAULT_REVIEW_COUNT = 10

# Performance thresholds
EXCELLENT_THRESHOLD = 90
GOOD_THRESHOLD = 75
FAIR_THRESHOLD = 60

# UI Settings
SEPARATOR_LENGTH = 70
SUMMARY_SEPARATOR_LENGTH = 50