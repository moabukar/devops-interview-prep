#!/usr/bin/env python3
"""
DevOps Interview Prep CLI - Interactive Interview Practice Tool
A CLI tool for DevOps interview preparation with scenario-based questions.
"""

import json
import click
import os
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import random as py_random

@dataclass
class Question:
    id: str
    topic: str
    difficulty: str
    question: str
    options: List[str]
    correct_answer: int
    explanation: str
    scenario: Optional[str] = None

class InterviewQuestionBank:
    def __init__(self, questions_file: str = "questions/interview_questions.json"):
        self.questions_file = Path(questions_file)
        self.questions: List[Question] = []
        self.load_questions()
    
    def load_questions(self):
        """Load interview questions from JSON file"""
        if not self.questions_file.exists():
            click.echo(f"❌ Questions file not found: {self.questions_file}")
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
                    scenario=q_data.get('scenario')
                )
                self.questions.append(question)
            
            click.echo(f"✅ Loaded {len(self.questions)} interview questions")
        except Exception as e:
            click.echo(f"❌ Error loading questions: {e}")
    
    def get_questions(self, topic: Optional[str] = None, difficulty: Optional[str] = None, count: int = 1) -> List[Question]:
        """Get filtered questions based on criteria"""
        filtered = self.questions
        
        if topic:
            filtered = [q for q in filtered if q.topic.lower() == topic.lower()]
        
        if difficulty:
            filtered = [q for q in filtered if q.difficulty.lower() == difficulty.lower()]
        
        if not filtered:
            return []
        
        return py_random.sample(filtered, min(count, len(filtered)))
    
    def get_topics(self) -> List[str]:
        """Get all available interview topics"""
        return list(set(q.topic for q in self.questions))
    
    def get_difficulties(self) -> List[str]:
        """Get all available difficulty levels"""
        return list(set(q.difficulty for q in self.questions))

class InterviewSession:
    def __init__(self):
        self.score = 0
        self.total = 0
        self.start_time = datetime.now()
        self.topic_performance = {}
    
    def ask_question(self, question: Question) -> bool:
        """Ask an interview question and return if answer was correct"""
        click.echo("\n" + "="*70)
        
        if question.scenario:
            click.echo(f"🎭 Interview Scenario:")
            click.echo(f"   {question.scenario}")
            click.echo()
        
        click.echo(f"❓ Interview Question:")
        click.echo(f"   {question.question}")
        click.echo()
        
        # Randomize answer options while tracking the correct answer
        original_correct_answer = question.correct_answer
        original_options = question.options.copy()
        
        # Create list of (option_text, is_correct) tuples
        options_with_correctness = [(option, i+1 == original_correct_answer) for i, option in enumerate(original_options)]
        
        # Shuffle the options
        py_random.shuffle(options_with_correctness)
        
        # Find new position of correct answer
        new_correct_position = None
        shuffled_options = []
        for i, (option_text, is_correct) in enumerate(options_with_correctness):
            shuffled_options.append(option_text)
            if is_correct:
                new_correct_position = i + 1
        
        # Display shuffled options
        for i, option in enumerate(shuffled_options, 1):
            click.echo(f"   {i}. {option}")
        
        click.echo()
        
        while True:
            try:
                answer = click.prompt("Your answer (1-{})".format(len(shuffled_options)), type=int)
                if 1 <= answer <= len(shuffled_options):
                    break
                else:
                    click.echo(f"Please enter a number between 1 and {len(shuffled_options)}")
            except click.Abort:
                return False
            except:
                click.echo("Please enter a valid number")
        
        self.total += 1
        correct = answer == new_correct_position
        
        # Track topic performance
        if question.topic not in self.topic_performance:
            self.topic_performance[question.topic] = {'correct': 0, 'total': 0}
        self.topic_performance[question.topic]['total'] += 1
        
        if correct:
            self.score += 1
            self.topic_performance[question.topic]['correct'] += 1
            click.echo("✅ Correct! Great job!")
        else:
            # Show the correct answer text, not position
            correct_answer_text = original_options[original_correct_answer - 1]
            click.echo(f"❌ Incorrect. The correct answer was: {correct_answer_text}")
        
        click.echo(f"💡 Explanation: {question.explanation}")
        
        return correct
    
    def show_summary(self):
        """Show interview session summary"""
        duration = datetime.now() - self.start_time
        percentage = (self.score / self.total * 100) if self.total > 0 else 0
        
        click.echo("\n" + "="*70)
        click.echo("🎯 INTERVIEW PREP SUMMARY")
        click.echo("="*70)
        click.echo(f"Overall Score: {self.score}/{self.total} ({percentage:.1f}%)")
        click.echo(f"Session Duration: {duration.seconds // 60}m {duration.seconds % 60}s")
        
        # Show topic breakdown
        if self.topic_performance:
            click.echo("\n📊 Performance by Topic:")
            for topic, perf in self.topic_performance.items():
                topic_pct = (perf['correct'] / perf['total'] * 100) if perf['total'] > 0 else 0
                click.echo(f"   • {topic.upper()}: {perf['correct']}/{perf['total']} ({topic_pct:.0f}%)")
        
        click.echo("\n🎓 Interview Readiness Assessment:")
        if percentage >= 90:
            click.echo("🌟 Excellent! You're interview-ready!")
        elif percentage >= 75:
            click.echo("👍 Great work! You're almost ready!")
        elif percentage >= 60:
            click.echo("📚 Good progress! Focus on weak areas.")
        else:
            click.echo("💪 Keep practicing! Review fundamentals.")

# Initialize question bank
question_bank = InterviewQuestionBank()

@click.group()
@click.version_option(version="1.0.0")
def cli():
    """
    🚀 DevOps Interview Prep - Master Your Next DevOps Interview
    
    Practice AWS, Kubernetes, Docker, Linux, Git, Networking, Terraform, CI/CD, 
    Security, and Monitoring with real interview questions!
    """
    pass

@cli.command()
@click.argument('topic', required=False)
@click.option('--difficulty', '-d', help='Difficulty level (easy, medium, hard)')
@click.option('--count', '-c', default=5, help='Number of questions (default: 5)')
@click.option('--interview-mode', '-i', is_flag=True, help='Full interview simulation mode')
def practice(topic, difficulty, count, interview_mode):
    """Start an interview practice session"""
    
    if not question_bank.questions:
        click.echo("❌ No interview questions available. Check your questions file.")
        return
    
    # Show available topics if none specified
    if not topic:
        topics = question_bank.get_topics()
        click.echo("📚 Available interview topics:")
        for t in sorted(topics):
            click.echo(f"  • {t}")
        
        topic = click.prompt("\nSelect a topic for practice", type=click.Choice(topics, case_sensitive=False))
    
    # Get questions
    questions = question_bank.get_questions(topic, difficulty, count)
    
    if not questions:
        click.echo(f"❌ No questions found for topic '{topic}'" + 
                  (f" with difficulty '{difficulty}'" if difficulty else ""))
        return
    
    click.echo(f"\n🎯 Starting Interview Practice: {topic.upper()}")
    if difficulty:
        click.echo(f"🔥 Difficulty Level: {difficulty.upper()}")
    click.echo(f"📊 Questions: {len(questions)}")
    
    if interview_mode:
        click.echo("🎭 Interview Simulation Mode: Answer like you're in a real interview!")
    
    session = InterviewSession()
    
    for i, question in enumerate(questions, 1):
        click.echo(f"\n📝 Question {i}/{len(questions)} | Difficulty: {question.difficulty.upper()}")
        session.ask_question(question)
        
        if interview_mode and i < len(questions):
            if not click.confirm("\nReady for the next question?", default=True):
                break
    
    session.show_summary()

@cli.command()
def topics():
    """List all available interview topics"""
    topics = question_bank.get_topics()
    
    if not topics:
        click.echo("❌ No topics available")
        return
    
    click.echo("📚 Available Interview Topics:")
    for topic in sorted(topics):
        count = len([q for q in question_bank.questions if q.topic == topic])
        difficulties = set(q.difficulty for q in question_bank.questions if q.topic == topic)
        click.echo(f"  • {topic.upper()}: {count} questions ({', '.join(sorted(difficulties))})")

@cli.command()
@click.argument('topic')
def focus(topic):
    """Get detailed information about a specific topic"""
    questions = [q for q in question_bank.questions if q.topic.lower() == topic.lower()]
    
    if not questions:
        click.echo(f"❌ Topic '{topic}' not found")
        return
    
    difficulties = {}
    for q in questions:
        if q.difficulty not in difficulties:
            difficulties[q.difficulty] = 0
        difficulties[q.difficulty] += 1
    
    click.echo(f"📊 Interview Topic: {topic.upper()}")
    click.echo(f"Total Questions: {len(questions)}")
    click.echo("Difficulty Breakdown:")
    for diff, count in sorted(difficulties.items()):
        click.echo(f"  • {diff.capitalize()}: {count} questions")
    
    # Show sample question IDs
    sample_ids = [q.id for q in questions[:5]]
    if sample_ids:
        click.echo(f"Sample Questions: {', '.join(sample_ids)}")

@cli.command()
@click.argument('topic')
@click.argument('difficulty')
def quick(topic, difficulty):
    """Get a single random interview question for quick practice"""
    questions = question_bank.get_questions(topic, difficulty, 1)
    
    if not questions:
        click.echo(f"❌ No questions found for {topic} / {difficulty}")
        return
    
    click.echo("🚀 Quick Interview Practice")
    session = InterviewSession()
    session.ask_question(questions[0])

@cli.command()
def stats():
    """Show interview question bank statistics"""
    if not question_bank.questions:
        click.echo("❌ No questions available")
        return
    
    total = len(question_bank.questions)
    topics = question_bank.get_topics()
    difficulties = question_bank.get_difficulties()
    
    click.echo("📊 DEVOPS INTERVIEW PREP STATISTICS")
    click.echo("="*50)
    click.echo(f"Total Interview Questions: {total}")
    click.echo(f"Available Topics: {len(topics)}")
    click.echo(f"Difficulty Levels: {len(difficulties)}")
    
    click.echo("\n📚 Questions by Topic:")
    for topic in sorted(topics):
        count = len([q for q in question_bank.questions if q.topic == topic])
        click.echo(f"  • {topic.upper()}: {count}")
    
    click.echo("\n🔥 Questions by Difficulty:")
    for diff in sorted(difficulties):
        count = len([q for q in question_bank.questions if q.difficulty == diff])
        click.echo(f"  • {diff.capitalize()}: {count}")

@cli.command()
@click.option('--count', '-c', default=10, help='Number of questions (default: 10)')
@click.option('--time-limit', '-t', help='Time limit in minutes (optional)')
def interview(count, time_limit):
    """Full interview simulation with mixed topics and difficulties"""
    if not question_bank.questions:
        click.echo("❌ No interview questions available.")
        return
    
    # Get a mix of questions from different topics and difficulties
    all_questions = question_bank.questions
    if len(all_questions) < count:
        count = len(all_questions)
    
    selected_questions = py_random.sample(all_questions, count)
    
    click.echo("🎭 FULL INTERVIEW SIMULATION")
    click.echo("="*50)
    click.echo(f"Questions: {count}")
    if time_limit:
        click.echo(f"Time Limit: {time_limit} minutes")
    click.echo("Mix of topics and difficulty levels")
    click.echo("\nTreat this like a real DevOps interview!")
    
    if not click.confirm("\nAre you ready to begin?"):
        click.echo("Come back when you're ready! 💪")
        return
    
    session = InterviewSession()
    
    for i, question in enumerate(selected_questions, 1):
        click.echo(f"\n📝 Interview Question {i}/{count}")
        click.echo(f"Topic: {question.topic.upper()} | Difficulty: {question.difficulty.upper()}")
        session.ask_question(question)
    
    session.show_summary()
    
    # Additional interview feedback
    percentage = (session.score / session.total * 100) if session.total > 0 else 0
    click.echo(f"\n🎯 Interview Simulation Complete!")
    if percentage >= 80:
        click.echo("🌟 Outstanding performance! You're ready for senior roles!")
    elif percentage >= 70:
        click.echo("🚀 Great job! You're well-prepared for most DevOps positions!")
    elif percentage >= 60:
        click.echo("📈 Good foundation! Focus on your weaker areas before interviewing.")
    else:
        click.echo("📚 More preparation needed. Keep practicing and review fundamentals!")

if __name__ == '__main__':
    cli()