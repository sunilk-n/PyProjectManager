import sys
import os as _os
import click
import logging

from pyPm.initialize import projectInitialize as pInit

from pyPm import __version__

OUTPUT_DIR = _os.getcwd()
log = logging.getLogger(__name__)


@click.group()
@click.option('--version', is_flag=True, help="Displays project version")
@click.option('--verbose', is_flag=True, help='Displays all the log.')
@click.pass_context
def cli(context, version: bool, verbose: bool):
    if version:
        print(__version__)

    if verbose:
        # log.setLevel(level=logging.INFO)
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)


@cli.command()
@click.pass_context
def init(context):
    logger = """
This utility will walk you through creating a setup.py file. It only covers the most common items, and tries to guess sensible defaults.

See `pyPm help setup` for definitive documentation on these fields and exactly what they do.

Use `pyPm install <pkg>` afterwards to install a package and save it as a dependency in the setup.py file.

Press ^C at any time to quit.
    """
    click.echo(message=logger)
    pInit.init_project(OUTPUT_DIR)


@cli.command()
@click.pass_context
def install(context):
    click.echo(message="Starting installing from the saved data")