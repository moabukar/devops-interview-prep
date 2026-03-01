"""
Progress tracking functionality
"""
import json
import click
from pathlib import Path
from typing import List, Tuple
from datetime import datetime

from ..models.question import QuestionResult
from .config import PROGRESS_FILE, MIN_ATTEMPTS_FOR_WEAK_AREAS, MAX_WEAK_AREAS_SHOWN


class ProgressTracker:
    """Tracks user progress and performance across sessions"""
    
    def __init__(self):
        self.results_file = PROGRESS_FILE
        self.results_file.parent.mkdir(exist_ok=True)
        self.results = self._load_results()
    
    def _load_results(self) -> List[QuestionResult]:
        """Load progress from file"""
        if not self.results_file.exists():
            return []
        
        try:
            with open(self.results_file, 'r') as f:
                data = json.load(f)
            return [
                QuestionResult(
                    question_id=r['question_id'],
                    topic=r['topic'], 
                    difficulty=r['difficulty'],
                    correct=r['correct'],
                    timestamp=datetime.fromisoformat(r['timestamp']),
                    time_taken=r.get('time_taken')
                )
                for r in data
            ]
        except Exception:
            return []
    
    def save_result(self, result: QuestionResult):
        """Save a new result"""
        self.results.append(result)
        try:
            with open(self.results_file, 'w') as f:
                json.dump([
                    {
                        'question_id': r.question_id,
                        'topic': r.topic,
                        'difficulty': r.difficulty,
                        'correct': r.correct,
                        'timestamp': r.timestamp.isoformat(),
                        'time_taken': r.time_taken
                    }
                    for r in self.results
                ], f, indent=2)
        except Exception as e:
            click.echo(f"Warning: Could not save progress: {e}")
    
    def get_weak_areas(self) -> List[Tuple[str, float]]:
        """Get topics with lowest success rates"""
        topic_stats = {}
        for result in self.results:
            if result.topic not in topic_stats:
                topic_stats[result.topic] = {'correct': 0, 'total': 0}
            topic_stats[result.topic]['total'] += 1
            if result.correct:
                topic_stats[result.topic]['correct'] += 1
        
        weak_areas = []
        for topic, stats in topic_stats.items():
            if stats['total'] >= MIN_ATTEMPTS_FOR_WEAK_AREAS:
                success_rate = stats['correct'] / stats['total']
                weak_areas.append((topic, success_rate))
        
        return sorted(weak_areas, key=lambda x: x[1])[:MAX_WEAK_AREAS_SHOWN]
    
    def get_failed_questions(self) -> List[str]:
        """Get IDs of questions that were answered incorrectly"""
        failed = []
        for result in self.results:
            if not result.correct:
                failed.append(result.question_id)
        return list(set(failed))
    
    def get_topic_stats(self) -> dict:
        """Get performance statistics by topic"""
        topic_stats = {}
        for result in self.results:
            if result.topic not in topic_stats:
                topic_stats[result.topic] = {'correct': 0, 'total': 0}
            topic_stats[result.topic]['total'] += 1
            if result.correct:
                topic_stats[result.topic]['correct'] += 1
        return topic_stats
    
    def get_difficulty_stats(self) -> dict:
        """Get performance statistics by difficulty"""
        difficulty_stats = {}
        for result in self.results:
            if result.difficulty not in difficulty_stats:
                difficulty_stats[result.difficulty] = {'correct': 0, 'total': 0}
            difficulty_stats[result.difficulty]['total'] += 1
            if result.correct:
                difficulty_stats[result.difficulty]['correct'] += 1
        return difficulty_stats
    
    def get_overall_stats(self) -> dict:
        """Get overall performance statistics"""
        if not self.results:
            return {
                'total_attempted': 0,
                'total_correct': 0,
                'success_rate': 0,
                'recent_success_rate': 0
            }
        
        total_attempted = len(self.results)
        total_correct = sum(1 for r in self.results if r.correct)
        success_rate = total_correct / total_attempted
        
        # Recent performance (last 10 questions)
        recent_results = self.results[-10:]
        recent_correct = sum(1 for r in recent_results if r.correct)
        recent_success_rate = recent_correct / len(recent_results) if recent_results else 0
        
        return {
            'total_attempted': total_attempted,
            'total_correct': total_correct,
            'success_rate': success_rate,
            'recent_success_rate': recent_success_rate
        }


# Global instance
progress_tracker = ProgressTracker()