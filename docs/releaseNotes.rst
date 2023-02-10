Release Notes
=============

`Click here for Source code of PyProjectManager <https://github.com/sunilk-n/PyProjectManager>`_

You can check the version of pyProjectManager by running::

    [command prompt path]> pyPm --version
    PyProjectManager, version 1.1.0

Version History
===============

PyProjectManager Version 1.x
++++++++++++++++++++++++++++

1.1.0, release on 10-02-2023
----------------------------

.. rubric:: Changed the dependency adding to the project

* `New Features`
    * Updated the new dependency adding to the project
        `pyPm init -p projectName -d <moduleName> <moduleVersion>`
    * Updated the way to add multiple dependencies and module
        `pyPm init -p projectName -d <moduleName -d <moduleName1> -m <dirName>...`
* `Bug Fixes`
    * Fixed dependencies issue while running the command adding dependencies
    * Updated Readme with actual install commands and running pyPm cli

1.0.0, released on xx-xx-2020
-----------------------------

.. rubric:: Initial release

* Initial release for PyProjectManager
