"""
Interview session management
"""
import json
import click
import random as py_random
from datetime import datetime
from dataclasses import asdict
from typing import List

from .question import Question, QuestionResult
from ..core.progress_tracker import progress_tracker
from ..utils.formatting import format_assessment, format_duration


class InterviewSession:
    """Manages an interview session with multiple questions"""
    
    def __init__(self, track_progress: bool = True):
        self.score = 0
        self.total = 0
        self.start_time = datetime.now()
        self.topic_performance = {}
        self.track_progress = track_progress
        self.results = []
    
    def ask_question(self, question: Question) -> bool:
            """Ask an interview question and return if answer was correct"""
            click.echo("\n" + "="*70)
            
            if question.scenario:
                click.echo(f"📋 Scenario: {question.scenario}")
                click.echo()
            
            click.echo(f"❓ Question: {question.question}")
            
            question_start_time = datetime.now()
            correct = False 

            # --- BRANCH: OPEN-ENDED (ANKI STYLE) ---
            if question.is_open_ended:
                # Captures the user's attempt for visual comparison
                user_attempt = click.prompt("\nType your answer")
                
                click.echo("\n" + "-"*30)
                click.secho("📝 YOUR ANSWER:", fg='yellow', bold=True)
                click.echo(user_attempt)
                
                click.secho("\n💡 SUGGESTED ANSWER:", fg='cyan', bold=True)
                click.echo(question.correct_answer)
                click.echo("-"*30)
                
                # Self-marking based on the comparison above
                score = click.prompt(
                    "\nRate your performance (1: Fail, 2: Hard, 3: Good, 4: Easy)",
                    type=click.IntRange(1, 4),
                    default=3
                )
                correct = score >= 3

            # --- BRANCH: MULTIPLE CHOICE ---
            else:
                click.echo()
                original_correct_answer = question.correct_answer
                original_options = question.options.copy()
                
                # Shuffle and display
                options_with_correctness = [(option, i+1 == original_correct_answer) for i, option in enumerate(original_options)]
                py_random.shuffle(options_with_correctness)
                
                new_correct_position = None
                shuffled_options = []
                for i, (option_text, is_correct) in enumerate(options_with_correctness):
                    shuffled_options.append(option_text)
                    if is_correct:
                        new_correct_position = i + 1
                
                for i, option in enumerate(shuffled_options, 1):
                    click.echo(f"   {i}. {option}")
                
                click.echo()
                
                while True:
                    try:
                        answer = click.prompt(f"Your answer (1-{len(shuffled_options)})", type=int)
                        if 1 <= answer <= len(shuffled_options):
                            break
                        click.echo(f"Please enter a number between 1 and {len(shuffled_options)}")
                    except (click.Abort, ValueError):
                        return False
                
                correct = (answer == new_correct_position)
                
                if correct:
                    click.secho("✅ Correct!", fg='green')
                else:
                    correct_answer_text = original_options[original_correct_answer - 1]
                    click.secho(f"❌ Incorrect. Correct answer: {correct_answer_text}", fg='red')

            # --- SHARED LOGIC (POST-QUESTION) ---
            # This section handles analytics and persistence regardless of question type
            time_taken = (datetime.now() - question_start_time).total_seconds()
            self.total += 1
            
            if question.topic not in self.topic_performance:
                self.topic_performance[question.topic] = {'correct': 0, 'total': 0}
            
            self.topic_performance[question.topic]['total'] += 1
            if correct:
                self.score += 1
                self.topic_performance[question.topic]['correct'] += 1
                if question.is_open_ended:
                    click.secho("⭐ Recorded as a successful recall.", fg='green')

            # Show extra context if available
            if not question.is_open_ended and question.explanation:
                click.echo(f"💡 Explanation: {question.explanation}")
            
            if question.real_world_context:
                click.echo(f"🌍 Real-world context: {question.real_world_context}")
            
            # Save results to the persistent progress tracker
            if self.track_progress:
                result = QuestionResult(
                    question_id=question.id,
                    topic=question.topic,
                    difficulty=question.difficulty,
                    correct=correct,
                    timestamp=datetime.now(),
                    time_taken=time_taken
                )
                progress_tracker.save_result(result)
                self.results.append(result)
            
            return correct
        
    def show_summary(self):
        """Show interview session summary"""
        duration = datetime.now() - self.start_time
        percentage = (self.score / self.total * 100) if self.total > 0 else 0
        
        click.echo("\n" + "="*50)
        click.echo("📊 SESSION SUMMARY")
        click.echo("="*50)
        click.echo(f"Score: {self.score}/{self.total} ({percentage:.1f}%)")
        click.echo(f"Duration: {format_duration(duration.seconds)}")
        
        if self.topic_performance:
            click.echo("\n📈 Performance by Topic:")
            for topic, perf in sorted(self.topic_performance.items()):
                topic_pct = (perf['correct'] / perf['total'] * 100) if perf['total'] > 0 else 0
                click.echo(f"  {topic}: {perf['correct']}/{perf['total']} ({topic_pct:.0f}%)")
        
        click.echo(f"\n🎯 Assessment:")
        click.echo(format_assessment(percentage))
    
    def export_results(self, filename: str):
        """Export session results to JSON file"""
        if not self.results:
            click.echo("No results to export")
            return
        
        try:
            export_data = {
                'session_summary': {
                    'score': self.score,
                    'total': self.total,
                    'percentage': (self.score / self.total * 100) if self.total > 0 else 0,
                    'duration_seconds': (datetime.now() - self.start_time).total_seconds()
                },
                'results': [asdict(r) for r in self.results]
            }
            
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            click.echo(f"📄 Results exported to {filename}")
        except Exception as e:
            click.echo(f"❌ Error exporting results: {e}")