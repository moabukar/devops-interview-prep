"""
Information commands (stats, topics, quick)
"""
import click
from ..core.question_bank import question_bank
from ..core.progress_tracker import progress_tracker
from ..models.session import InterviewSession
from ..utils.formatting import print_header


@click.command(context_settings={"ignore_unknown_options": True})
@click.pass_context
def stats(ctx):
    """📊 Show question bank and progress statistics"""
    log = ctx.obj['LOGGER']
    log.debug("Stats command called")
    if not question_bank.questions:
        click.echo("❌ No questions available")
        return
    
    total = len(question_bank.questions)
    topics = question_bank.get_topics()
    difficulty_dist = question_bank.get_difficulty_distribution()
    
    # Question bank stats
    print_header("QUESTION BANK STATISTICS")
    click.echo(f"📝 Total questions: {total}")
    click.echo(f"📚 Topics: {len(topics)}")
    
    # Difficulty breakdown
    click.echo(f"\n🎚️  By difficulty:")
    for difficulty in ['easy', 'medium', 'hard']:
        if difficulty in difficulty_dist:
            click.echo(f"  • {difficulty}: {difficulty_dist[difficulty]}")
    
    # Topic breakdown
    click.echo(f"\n📚 By topic:")
    for topic in sorted(topics):
        count = question_bank.get_topic_count(topic)
        click.echo(f"  • {topic}: {count}")
    
    # Progress statistics
    overall_stats = progress_tracker.get_overall_stats()
    if overall_stats['total_attempted'] > 0:
        click.echo(f"\n📈 YOUR PROGRESS:")
        click.echo(f"  • Questions attempted: {overall_stats['total_attempted']}")
        click.echo(f"  • Overall success rate: {overall_stats['success_rate']:.1%}")
        
        unique_attempted = len(set(r.question_id for r in progress_tracker.results))
        remaining = total - unique_attempted
        click.echo(f"  • Questions remaining: {remaining}")


@click.command(context_settings={"ignore_unknown_options": True})
def topics():
    """📚 List all available interview topics"""
    topics = question_bank.get_topics()
    company_types = question_bank.get_company_types()
    
    if not topics:
        click.echo("❌ No topics available")
        return
    
    print_header("Available interview topics", "📚")
    
    for topic in topics:
        count = question_bank.get_topic_count(topic)
        difficulties = set(q.difficulty for q in question_bank.questions if q.topic == topic)
        diff_str = ", ".join(sorted(difficulties))
        click.echo(f"  • {topic}: {count} questions ({diff_str})")
    
    if company_types:
        click.echo(f"\n🏢 Company types: {', '.join(company_types)}")


@click.command(context_settings={"ignore_unknown_options": True})
def quick():
    """⚡ Get a single random question for quick practice"""
    if not question_bank.questions:
        click.echo("❌ No questions available")
        return
    
    question = question_bank.get_random_question()
    if not question:
        click.echo("❌ Could not get a random question")
        return
    
    click.echo("⚡ QUICK PRACTICE")
    click.echo("="*20)
    
    session = InterviewSession()
    session.ask_question(question)
    
    # Don't show full summary for quick practice
    click.echo(f"\n⚡ Quick result: {session.score}/{session.total}")