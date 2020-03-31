import sys
import os as _os
import click
import logging

from pyPm import __version__
from pyPm.initialize import projectInitialize as pInit

OUTPUT_DIR = _os.getcwd()
log = logging.getLogger(__name__)


@click.group()
@click.version_option(version=__version__, prog_name="PyProjectManager")
@click.option('--verbose', is_flag=True, help='Displays all the log.')
@click.pass_context
def cli(context, verbose):
    if verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)


@cli.command()
@click.pass_context
@click.option("--project", type=str, default=None, help="Project name")
@click.option("--dependency", type=click.Tuple([str, str]), default=[], help="Add dependency projects to the existing project")
def init(context, project, dependency):
    logger = """
This utility will walk you through creating a setup.py file. It only covers the most common items, and tries to guess sensible defaults.

See `pyPm help setup` for definitive documentation on these fields and exactly what they do.

Use `pyPm install <pkg>` afterwards to install a package and save it as a dependency in the setup.py file.

Press ^C at any time to quit.
    """
    if dependency:
        if not project:
            log.warning("Please specify the project name to add dependency by adding --project to command")
            sys.exit()
        package_dict = {}
        print project
        if pInit.check_for_project(OUTPUT_DIR, pkg_file=project):
            package_dict = pInit.get_project_details(OUTPUT_DIR, pkg_file=project)
        if not package_dict:
            log.warning("Unable to find the project {0}, Please run `pyPm init --project {0}` to add dependency".format(project))
            sys.exit()
        else:
            package_dict['dependency'].append(dependency)
            pInit.create_files(OUTPUT_DIR, ".%s.json" % project, data=package_dict)
            sys.exit()

    click.echo(message=logger)
    pInit.init_project(OUTPUT_DIR, project=project)


@cli.command()
@click.pass_context
def install(context):
    click.echo(message="Starting installing from the saved data")
