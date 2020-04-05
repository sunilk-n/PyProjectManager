import os

import pyPm
from pyPm.utilities import utils
from pyPm.install.utils import CommandInitializer


class CommandGenerator(CommandInitializer):
    def __init__(self, *args):
        super().__init__(*args)

    @property
    def initializer(self):
        return [
            "# This project is build with %s %sV" % (pyPm.__name__, pyPm.__version__),
            "# Please don't edit without knowing much about the working project",
            "# If you have any queries about python project builder,",
            "# Please contact below person(s)\n# %s - %s" % (
                self.package_dict['author'], self.package_dict['authorMail']
            )
        ]

    @property
    def assigner(self):
        return [
            "__version__ = '%s'" % self.package_dict['version'],
            "__name__ = '%s'" % self.package_dict['name'],
            "__author__ = ['%s']" % self.package_dict['author'],
            "__author_email__ = ['%s']" % self.package_dict['authorMail']
        ]


def command_builder(package_dict):
    cmd_gen = CommandGenerator(package_dict)
    init_file = utils.build_cmd_file(cmd_gen.initializer, class_or_def=False)
    init_file = utils.build_cmd_file(cmd_gen.assigner, script_list=init_file, class_or_def=False)
    init_file.append("")
    return "\n".join(init_file)
