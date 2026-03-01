"""
Reset progress command
"""
import click
from ..core.config import PROGRESS_FILE


@click.command(context_settings={"ignore_unknown_options": True})
@click.option('--force', '-f', is_flag=True, help='Skip confirmation prompt')
@click.pass_context
def reset(ctx, force):
    """🗑️  Reset all progress and start fresh"""
    if not PROGRESS_FILE.exists():
        click.echo("📭 No progress data found. Nothing to reset.")
        return

    if not force:
        if not click.confirm("⚠️  This will delete all your progress data. Are you sure?"):
            click.echo("❌ Reset cancelled.")
            return

    try:
        PROGRESS_FILE.unlink()
        click.echo("✅ Progress reset successfully. You're starting fresh!")
    except Exception as e:
        click.echo(f"❌ Error resetting progress: {e}")
