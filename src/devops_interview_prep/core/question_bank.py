"""
Question bank management
"""
import json
import click
import requests
import re
import uuid
import random as py_random
from pathlib import Path
from typing import List, Optional
from ..models.question import Question
from .config import DEFAULT_QUESTIONS_FILE

class InterviewQuestionBank:
    """Manages the collection of interview questions"""

    def __init__(self, questions_file: str = DEFAULT_QUESTIONS_FILE):
        self.questions_file = Path(questions_file)
        self.external_file = self.questions_file.parent / "open_ended.json"
        self.questions: List[Question] = []
        self.load_questions()
    
    def _load_from_path(self, file_path: Path):
        """Internal helper to load questions from a specific JSON file"""
        if not file_path.exists():
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for q_data in data.get('questions', []):
                question = Question(
                    id=q_data['id'],
                    topic=q_data['topic'],
                    difficulty=q_data['difficulty'],
                    question=q_data['question'],
                    options=q_data.get('options'),
                    correct_answer=q_data['correct_answer'],
                    explanation=q_data.get('explanation', ''),
                    scenario=q_data.get('scenario'),
                    company_tags=q_data.get('company_tags', []),
                    real_world_context=q_data.get('real_world_context')
                )
                self.questions.append(question)
        except Exception as e:
            click.echo(f"❌ Error loading from {file_path.name}: {e}")

    def load_questions(self):
        """Load interview questions from all sources"""
        self.questions = [] # Clear existing list
        
        # 1. Load main questions from interview_questions.json
        if not self.questions_file.exists():
            click.echo(f"❌ Error: Primary questions file not found.")
        else:
            self._load_from_path(self.questions_file)
    
        # 2. Load tech-vault questions
        if self.external_file.exists():
            local_count = len(self.questions)
            self._load_from_path(self.external_file)
            external_count = len(self.questions) - local_count
            click.echo(f"✅ Loaded {external_count} external questions from tech-vault")

    def sync_tech_vault(self):
        """Fetches questions and saves them to the external JSON file"""
        url = "https://raw.githubusercontent.com/moabukar/tech-vault/main/README.md"
        
        # normalization map to convert tech vault topics into topics in the cli tool
        normalization_map = {
                "docker & k8s": "docker & kubernetes",                
                "aws": "aws",
                "ansible": "ansible",
                "linux": "linux",
                "networking": "networking",
                "terraform": "terraform",
                "git": "git",
                "ci/cd": "cicd",
                "azure": "azure",
                "cyber scurity & info security": "security",
                "monitoring": "monitoring",
                "data architect": "data architect",
                "data engineering": "data engineering",
                "data modelling and schemas": "data modelling and schemas",
                "sql": "sql"
            }
        
        try:
            click.echo("🌐 Syncing with Tech Vault...")
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Split content into topic blocks
            topic_blocks = re.split(r'<summary><h3 [^>]*>(.*?)</h3></summary>', response.text)
            new_questions_data = []
            
            for i in range(1, len(topic_blocks), 2):
                raw_topic = topic_blocks[i].strip()
                block_content = topic_blocks[i+1]

                # NORMALISE TOPIC NAME
                # Matches "kubernetes" -> "Docker & K8s", etc.
                standard_topic = normalization_map.get(raw_topic.lower(), raw_topic)

                qa_pairs = re.findall(r'<details>\s*<summary>(.*?)</summary>(.*?)</details>', block_content, re.DOTALL)

                for q_text, a_text in qa_pairs:
                    clean_answer = re.sub(r'<[^>]+>', '', a_text).strip()
                    # Store the dictionary format for the JSON file

                    # Ignore questions with no answers
                    if clean_answer and clean_answer != "*Answer coming soon!":
                        new_questions_data.append({
                            "id": f"tv-{str(uuid.uuid4())[:8]}",
                            "topic": standard_topic,
                            "difficulty": "medium",
                            "question": q_text.strip(),
                            "options": None,
                            "correct_answer": clean_answer,
                            "explanation": f"Source: Tech Vault ({raw_topic})"
                        })

            # Save to the external file
            with open(self.external_file, 'w', encoding='utf-8') as f:
                json.dump({"questions": new_questions_data}, f, indent=4)
            
            click.echo(f"✨ Successfully synced {len(new_questions_data)} tech-vault questions to {self.external_file.name}")
            
            # Reload the bank to include the new questions
            self.load_questions()

        except Exception as e:
            click.echo(f"❌ Failed to sync: {e}")


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
        
        return py_random.sample(filtered, min(count, len(filtered)))
    
    def get_topics(self) -> List[str]:
        # Use a set to get unique values, then sort them alphabetically
        topic_set = set(q.topic for q in self.questions)
        return sorted(list(topic_set))

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
        search_topic = topic.lower()
        return len([q for q in self.questions if q.topic.lower() == search_topic])
    
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


