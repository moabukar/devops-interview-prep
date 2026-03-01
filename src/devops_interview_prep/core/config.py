"""
Configuration and constants - Smart path detection
"""
import os
from pathlib import Path

# Application info
APP_NAME = "MockOps"
VERSION = "1.2.0"

# Smart path detection for questions file
def _get_questions_file_path():
    """
    Smart path detection that works locally, in Docker, and via pip/brew install
    """
    _pkg_dir = Path(__file__).parent.parent  # devops_interview_prep/
    possible_paths = [
        # Bundled with package (pip install -e . or pip install .)
        _pkg_dir / "data" / "questions" / "interview_questions.json",
        # Relative from package source root (dev checkout)
        _pkg_dir.parent.parent / "data" / "questions" / "interview_questions.json",
        # Docker container
        Path("/app/data/questions/interview_questions.json"),
        # Homebrew share directory
        Path("/usr/local/share/mockops/data/questions/interview_questions.json"),
        Path("/opt/homebrew/share/mockops/data/questions/interview_questions.json"),
        # Relative from current working directory
        Path("data/questions/interview_questions.json"),
    ]
    
    for path in possible_paths:
        if path.exists():
            return str(path)
    
    # Fallback to relative path
    return "data/questions/interview_questions.json"

# File paths
DEFAULT_QUESTIONS_FILE = _get_questions_file_path()
PROGRESS_DIR = Path.home() / ".mockops"
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