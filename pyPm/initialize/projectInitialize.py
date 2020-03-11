import sys
import os as _os
import logging
import pprint
import json

from traVer import Version
from pyPm import __version__

log = logging.getLogger(__name__)

PACKAGE_NAME = None
PACKAGE_VERSION = "1.0.0"
DESCRIPTION = None
ENTRY_POINT = "__main__.py"
TEST_COMMAND = None
GIT_REPO = None
KEYWORDS = None
AUTHOR = None
AUTHOR_EMAIL = None
LICENSE = "GNU V3"


def create_files(output, file_name, data=None):
    if not _os.path.exists(output):
        log.error("Please make sure that the output directory exists")
        return False
    file_path = _os.path.join(output, file_name)
    with open(file_path, 'w') as newFile:
        if data and isinstance(data, dict):
            json.dump(data, newFile, indent=2)
        elif data:
            newFile.write(data)
    log.info("%s file created in %s" % (file_name, output))
    return True


def get_project_details(install_path):
    package_file = ".%s.json" % PACKAGE_NAME
    pkg_file_path = _os.path.join(install_path, package_file)
    if check_for_project(install_path, pkg_file=package_file):
        with open(pkg_file_path) as fd:
            data = json.load(fd)
        return data


def check_for_project(install_path, pkg_file=None):
    package_file = pkg_file or ".%s.json" % PACKAGE_NAME
    pkg_file_path = _os.path.join(install_path, package_file)
    if _os.path.exists(pkg_file_path):
        return True
    return False

def create_directory(output, dir_name):
    if _os.path.exists(output):
        log.warning("Directory name already exists.")
        return

    dir_path = _os.path.join(output, dir_name)
    _os.makedirs(dir_path)
    log.info("%s directory created in %s" % (dir_name, output))


def init_project(install_path):
    global PACKAGE_NAME, PACKAGE_VERSION, DESCRIPTION, ENTRY_POINT, TEST_COMMAND, GIT_REPO
    global KEYWORDS, AUTHOR, AUTHOR_EMAIL, LICENSE
    pkg_name = _os.path.basename(install_path)
    package_dict = {}
    PACKAGE_NAME = query_detail("Project Name", default=pkg_name)
    if check_for_project(install_path):
        package_dict = get_project_details(install_path)
        log.warning("%s already been setup in the directory" % PACKAGE_NAME)
    PACKAGE_VERSION = query_detail("Project Version", default=package_dict.get('version', None) or PACKAGE_VERSION)
    DESCRIPTION = query_detail("Description", default=package_dict.get('description', None))
    ENTRY_POINT = query_detail("Entry Point", default=package_dict.get('main', None) or ENTRY_POINT)
    TEST_COMMAND = query_detail("Test Command", default=package_dict['scripts'].get('version', None) if package_dict.get('scripts', False) else None)
    GIT_REPO = query_detail("Git Repository", default=package_dict.get('url', None))
    KEYWORDS = query_detail("Keywords", default=package_dict.get('keywords', None))
    AUTHOR = query_detail("Author", default=package_dict.get('author', None))
    AUTHOR_EMAIL = query_detail("Author Email", default=package_dict.get('authorMail', None))
    LICENSE = query_detail("License", default=package_dict.get('license', None) or LICENSE)

    package_dict = {
        "name": PACKAGE_NAME,
        "version": PACKAGE_VERSION,
        "description": DESCRIPTION,
        "main": ENTRY_POINT,
        "scripts": {
            "test": "No test specified",
        },
        "author": AUTHOR,
        "authorMail": AUTHOR_EMAIL,
        "license": LICENSE,
        "url": GIT_REPO,
    }

    log.warning("About to write the following dictionary to <package>.json\n")
    pprint.pprint(package_dict)

    accept = query_detail("Is this Okay?", default="yes")
    if not accept == "yes":
        log.warning("Project creation exited by user.")
        sys.exit()

    create_files(install_path, ".%s.json" % PACKAGE_NAME, data=package_dict)


def query_detail(query, default=None):
    query = query.strip() + ": "
    if default:
        query = query + "(%s) " % default
    result = input(query)

    if result:
        return result
    else:
        return default
