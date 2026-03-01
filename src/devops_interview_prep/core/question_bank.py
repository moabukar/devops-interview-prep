"""
Question bank management
"""
import json
import click
import random as py_random
from pathlib import Path
from typing import List, Optional

from ..models.question import Question
from .config import DEFAULT_QUESTIONS_FILE


class InterviewQuestionBank:
    """Manages the collection of interview questions"""
    
    def __init__(self, questions_file: str = DEFAULT_QUESTIONS_FILE):
        self.questions_file = Path(questions_file)
        self.questions: List[Question] = []
        self.load_questions()
    
    def load_questions(self):
        """Load interview questions from JSON file"""
        if not self.questions_file.exists():
            click.echo(f"❌ Error: Questions file not found: {self.questions_file}")
            return
        
        try:
            with open(self.questions_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.questions = []
            for q_data in data.get('questions', []):
                question = Question(
                    id=q_data['id'],
                    topic=q_data['topic'],
                    difficulty=q_data['difficulty'],
                    question=q_data['question'],
                    options=q_data['options'],
                    correct_answer=q_data['correct_answer'],
                    explanation=q_data['explanation'],
                    scenario=q_data.get('scenario'),
                    company_tags=q_data.get('company_tags', []),
                    real_world_context=q_data.get('real_world_context')
                )
                self.questions.append(question)
            
            click.echo(f"✅ Loaded {len(self.questions)} interview questions")
        except Exception as e:
            click.echo(f"❌ Error loading questions: {e}")
    
    def get_questions(self, topic: Optional[str] = None, difficulty: Optional[str] = None, 
                     count: int = 1, company_type: Optional[str] = None,
                     question_ids: Optional[List[str]] = None) -> List[Question]:
        """Get filtered questions based on criteria"""
        filtered = self.questions
        
        if question_ids:
            filtered = [q for q in filtered if q.id in question_ids]
        
        if topic:
            filtered = [q for q in filtered if q.topic.lower() == topic.lower()]
        
        if difficulty:
            filtered = [q for q in filtered if q.difficulty.lower() == difficulty.lower()]
        
        if company_type:
            filtered = [q for q in filtered if company_type.lower() in [tag.lower() for tag in (q.company_tags or [])]]
        
        if not filtered:
            return []
        
        # When fetching by specific IDs, return all matches (don't sample)
        if question_ids:
            return filtered
        
        return py_random.sample(filtered, min(count, len(filtered)))
    
    def get_topics(self) -> List[str]:
        """Get all available topics"""
        return sorted(list(set(q.topic for q in self.questions)))
    
    def get_company_types(self) -> List[str]:
        """Get all available company types"""
        company_types = set()
        for q in self.questions:
            if q.company_tags:
                company_types.update(q.company_tags)
        return sorted(list(company_types))
    
    def get_difficulties(self) -> List[str]:
        """Get all available difficulty levels"""
        return sorted(list(set(q.difficulty for q in self.questions)))
    
    def get_topic_count(self, topic: str) -> int:
        """Get number of questions for a specific topic"""
        return len([q for q in self.questions if q.topic == topic])
    
    def get_difficulty_distribution(self) -> dict:
        """Get distribution of questions by difficulty"""
        distribution = {}
        for q in self.questions:
            distribution[q.difficulty] = distribution.get(q.difficulty, 0) + 1
        return distribution
    
    def get_random_question(self) -> Optional[Question]:
        """Get a random question"""
        if not self.questions:
            return None
        return py_random.choice(self.questions)


# Global instance
question_bank = InterviewQuestionBank()