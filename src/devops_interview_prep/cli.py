#!/usr/bin/env python3
"""
DevOps Interview Prep CLI - Main entry point
"""
from .core.logger import get_logger
import click
from .core.config import APP_NAME, VERSION

# Import all commands
from .commands.practice import practice
from .commands.analytics import analytics, weak_areas
from .commands.review import review_mistakes
from .commands.interview import interview
from .commands.info import stats, topics, quick


@click.group(context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True
))
@click.version_option(version=VERSION)
@click.option("--verbose", is_flag=True, help="Enable verbose output")
@click.pass_context
def cli(ctx, verbose):
    """🚀 DevOps Interview Prep - Master Your Next DevOps Interview

    Practice AWS, Kubernetes, Docker, Linux, Git, Networking, Terraform, CI/CD,
    Security, and Monitoring with real interview questions!
    
    💡 New Features:
    • Progress tracking and weak area identification
    • Review missed questions
    • Detailed performance analytics
    • Export results for further analysis
    """
    ctx.ensure_object(dict)
    ctx.obj['VERBOSE'] = verbose

    logger = get_logger(verbose)
    ctx.obj['LOGGER'] = logger

    logger.debug("Verbose mode is enabled.")
    logger.debug("CLI initialised successfully")



# Add all commands to the CLI group
cli.add_command(practice)
cli.add_command(weak_areas)
cli.add_command(review_mistakes)
cli.add_command(analytics)
cli.add_command(interview)
cli.add_command(stats)
cli.add_command(topics)
cli.add_command(quick)


if __name__ == '__main__':
    cli()