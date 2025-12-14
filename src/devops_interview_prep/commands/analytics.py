"""
Analytics and weak areas commands
"""
import json
import click
from ..core.progress_tracker import progress_tracker
from ..core.question_bank import question_bank
from ..utils.formatting import (
    print_analytics_summary, 
    print_topic_stats, 
    print_difficulty_stats,
    print_weak_areas_list
)


@click.command(context_settings={"ignore_unknown_options": True})
@click.option('--topic', help='Show analytics for specific topic')
@click.option('--export', help='Export analytics to JSON file')
@click.pass_context
def analytics(ctx, topic, export):
    """📈 Show detailed performance analytics"""
    log = ctx.obj['LOGGER']
    log.debug(f"Analytics called with topic={topic}, export={export}")
    results = progress_tracker.results
    
    if not results:
        click.echo("📊 No performance data available yet.")
        click.echo("💡 Practice some questions first to see your analytics!")
        return
    
    if topic:
        results = [r for r in results if r.topic.lower() == topic.lower()]
        if not results:
            click.echo(f"❌ No data found for topic: {topic}")
            return
    
    # Get overall statistics
    overall_stats = progress_tracker.get_overall_stats()
    print_analytics_summary(overall_stats)
    
    # Topic breakdown
    topic_stats = progress_tracker.get_topic_stats()
    if topic_stats:
        print_topic_stats(topic_stats)
    
    # Difficulty breakdown
    difficulty_stats = progress_tracker.get_difficulty_stats()
    if difficulty_stats:
        print_difficulty_stats(difficulty_stats)
    
    # Export if requested
    if export:
        _export_analytics(overall_stats, topic_stats, difficulty_stats, export)


def _export_analytics(overall_stats, topic_stats, difficulty_stats, export_file):
    """Export analytics data to JSON file"""
    analytics_data = {
        'summary': overall_stats,
        'by_topic': {
            topic: {
                'success_rate': stats['correct']/stats['total'], 
                'total': stats['total']
            } 
            for topic, stats in topic_stats.items()
        },
        'by_difficulty': {
            diff: {
                'success_rate': stats['correct']/stats['total'], 
                'total': stats['total']
            } 
            for diff, stats in difficulty_stats.items()
        }
    }
    
    try:
        with open(export_file, 'w') as f:
            json.dump(analytics_data, f, indent=2)
        click.echo(f"\n📄 Analytics exported to {export_file}")
    except Exception as e:
        click.echo(f"❌ Error exporting analytics: {e}")


@click.command(context_settings={"ignore_unknown_options": True})
@click.pass_context
def weak_areas(ctx):
    """🎯 Show topics where you need more practice"""
    weak_areas = progress_tracker.get_weak_areas()
    log = ctx.obj['LOGGER']
    log.debug("Weak areas command called")
    
    if not weak_areas:
        click.echo("📊 No performance data available yet.")
        click.echo("💡 Practice some questions first to see your weak areas!")
        
        # Suggest starting with a popular topic
        if question_bank.questions:
            topics = question_bank.get_topics()
            suggested_topic = topics[0] if topics else None
            if suggested_topic and click.confirm(f"\nStart practicing {suggested_topic}?"):
                # Import here to avoid circular imports
                from .practice import practice
                ctx = click.get_current_context()
                ctx.invoke(practice, topic=suggested_topic, count=5)
        return
    
    print_weak_areas_list(weak_areas)
    
    if weak_areas:
        click.echo(f"\n💡 Recommendation: Focus on {weak_areas[0][0]}")
        if click.confirm(f"Practice {weak_areas[0][0]} questions now?"):
            # Import here to avoid circular imports
            from .practice import practice
            ctx = click.get_current_context()
            ctx.invoke(practice, topic=weak_areas[0][0], count=5)