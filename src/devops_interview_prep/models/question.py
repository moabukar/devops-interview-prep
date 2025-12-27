"""
Question and QuestionResult models
"""
from dataclasses import dataclass
from typing import List, Optional, Union
from datetime import datetime


@dataclass
class Question:
    """Interview question model"""
    id: str
    topic: str
    difficulty: str
    question: str
    options: Optional[List[str]] 
    correct_answer: Union[int, str] 
    explanation: str
    scenario: Optional[str] = None
    company_tags: Optional[List[str]] = None
    real_world_context: Optional[str] = None

    @property
    def is_open_ended(self) -> bool:
        """Helper to check the question type"""
        return self.options is None


@dataclass
class QuestionResult:
    """Result of answering a question"""
    question_id: str
    topic: str
    difficulty: str
    correct: bool
    timestamp: datetime
    time_taken: Optional[float] = None


