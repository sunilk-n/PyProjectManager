"""
    Main entry point for the application to start
"""
import sys
import os as _os
import click
import logging

from pyPm import __version__
from pyPm.initialize import projectInitialize as pInit
from pyPm.install import builder as p_build
from pyPm.utilities import utils
from pyPm.utilities import moduleVersion

OUTPUT_DIR = _os.getcwd()
log = logging.getLogger(__name__)


@click.group()
@click.version_option(version=__version__, prog_name="PyProjectManager")
@click.help_option("-h", "--help", help="Displays this help options and exits")
@click.option('--verbose', is_flag=True, help='Displays all the log.')
@click.pass_context
def cli(context, verbose):
    if verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)


@cli.command()
@click.pass_context
@click.help_option("-h", "--help", help="Displays this help options and exits")
@click.option("--project", "-p", type=str, default=None, help="Project name")
@click.option("--dependency", "-d", nargs=0,
              help="Add dependency projects to the existing project with module name and version"
              )
@click.argument("dependency", nargs=-1)
@click.option("--module", '-m', help="Add new module to the project")
def init(context, project, dependency, module):
    logger = """
This utility will walk you through creating a setup.py file. It only covers the most common items, and tries to guess sensible defaults.

See `pyPm help install` for definitive documentation on these fields and exactly what they do.

Use `pyPm install -p <projectName>` afterwards to install a package and save it as a dependency in the setup.py file.

Press ^C at any time to quit.
    """
    if dependency:
        if len(dependency) > 2:
            log.error("Arguments for dependency must be either <Module> <version> or only <Module>")
            sys.exit()
        if not project:
            log.warning("Please specify the project name to add dependency by adding --project to command")
            return
        package_dict = {}
        if pInit.check_for_project(OUTPUT_DIR, pkg_file=project):
            package_dict = pInit.get_project_details(OUTPUT_DIR, pkg_file=project)
        if not package_dict:
            log.warning("Unable to find the project {0}, Please run `pyPm init --project {0}` to add dependency".format(
                    project
                )
            )
            return
        else:
            dep = False
            if utils.check_for_dependency(dependency, package_dict):
                dep = True
                if utils.check_for_dep_version(dependency, package_dict):
                    log.warning("Dependency '%s' already added to the project" % dependency[0])
                    return
                dep_version = False
            if len(dependency) == 2:
                if dep:
                    for i, module in enumerate(package_dict['dependency']):
                        if module[0] == dependency[0]:
                            package_dict['dependency'].pop(i)
                            break

                m_version = moduleVersion.get_module_version(dependency[0], module_version=dependency[1])
                if not m_version:
                    # click.echo("Unable to find the module/module version. Exiting...")
                    sys.exit()
                package_dict['dependency'].append(dependency)
            elif len(dependency) == 1:
                m_version = moduleVersion.get_module_version(dependency[0])
                package_dict['dependency'].append([dependency[0], m_version])
            pInit.create_files(OUTPUT_DIR, ".%s.json" % project, data=package_dict)
            click.echo("Dependency updated with %s module" % dependency[0])
            return

    if module:
        if not project:
            log.warning("Please specify the project name to add dependency by adding --project to command")
            return
        package_dict = {}
        if pInit.check_for_project(OUTPUT_DIR, pkg_file=project):
            package_dict = pInit.get_project_details(OUTPUT_DIR, pkg_file=project)
        if not package_dict:
            log.warning("Unable to find the project {0}, Please run `pyPm init --project {0}` to add dependency".format(
                    project
                )
            )
            return
        else:
            if utils.check_for_module(module, package_dict):
                log.warning("Module '%s' already exists in the project" % module)
                return
            package_dict['module'].append(module)
            pInit.create_files(OUTPUT_DIR, ".%s.json" % project, data=package_dict)
            click.echo("Module '%s' added to project" % module)
            return

    click.echo(message=logger)
    pInit.init_project(OUTPUT_DIR, project=project)


@cli.command()
@click.pass_context
@click.help_option("-h", "--help", help="Displays this help options and exits")
@click.option("--project", "-p", type=str, default=None, help="Project name")
# @click.option("project", type=str, help="Project name", required=True)
def install(context, project):
    click.echo(message="Starting installing from the saved data")
    package_dict = {}
    if pInit.check_for_project(OUTPUT_DIR, pkg_file=project):
        package_dict = pInit.get_project_details(OUTPUT_DIR, pkg_file=project)
    if not package_dict:
        log.warning("Unable to find the project {0}, Please run `pyPm init --project {0}` to add dependency".format(
                project
            )
        )
        return
    p_build.install(OUTPUT_DIR, package_dict)
    click.echo(message="%s project installed in %s directory" %(project, OUTPUT_DIR))


@cli.command()
@click.pass_context
@click.argument("option")
@click.help_option("-h", "--help", help="Displays this help options and exits")
def help(context, option):
    options = ['init', 'install']
    if not option in options:
        log.error("No option called '%s' in pyPm" % option)
        sys.exit()
    click.echo("Displays help for the option given %s" % option)

    helper_msg = ""
    if option == "init":
        helper_msg = """
Complete help information about init:
    * pyPm init : Starts project initialization
    * pyPm init [-p <projectName>] : Starts project initialization setting projectName as provided
    * pyPm init [-p <projectName> -d <dependancy>] : Adds 3rd party dependancy modules to the project
        Usage: pyPm init -p <projectName> -d <moduleName> [<module_version>]
            * Ex: pyPm init -p PyProjectManager -d click (or)
            * Ex: pyPm init -p PyProjectManager -d click 7.1.1
    * pyPm init [-p <projectName> -m <module>] : Adds user defined module package to the project
        Usage: pyPm init -p <projectName> -m <moduleName>
            * Ex: pyPm init -p PyProjectManager -m testModule 
        """

    elif option == "install":
        helper_msg = """
Complete help information about install:
    * pyPm install [-p <projectName>] : Starts installing project to the current directory
        Usage: pyPm install -p <projectName>
            * Ex: pyPm install -p PyProjectManager
        """

    click.echo(helper_msg)
