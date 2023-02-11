Installation Setup
==================

Install
+++++++
* Run the below command in your command prompt/ terminal to install PyProjectManager::

    > pip install pyPman

* This line will automatically install all the dependenciesof pyProjectManager

Create your first project with PyProjectManager
+++++++++++++++++++++++++++++++++++++++++++++++

PyProjectManager Initialization
-------------------------------
* Before running the project initialization, create a new folder in your local disk and go into that directory.
* Create your first python project with PyProjectManager by running::

    > pyPman init

* You can also run the initialization with project name specfied as::

    > pyPman init -p <projectName>

* This will initialize the project by prompting the basic questions like projectName, packageName, Author, ...etc.,
* After initializing the project with all the neccessary information, a .json file will be generated in the current working directory.

.. warning::
    Please don't delete the ".<projectName>.json" file. The whole initialized project will be stored in that file. Project installation is based on that file.

* To add the dependancies for the project which are 3rd party modules, PyProjectManager can do that for you. By running::

    > pyPman init -p <projectName> -d <3rdPartyModules>
    example:
    > pyPman init -p PyProjectManager -d Click
* To add multiple dependencies we can do that by using `-d` multiple times and then the <3rdPartyModules> and to use particular version of the module, you can use `==` like <3rdPartyModule>==<moduleVersion> as below::

    > pyPman init -p PyProjectManager -d Click -d traVer==1.0.0

.. note::
    The dependancy which are added to the project will check if that module already exists or not. If not exists, then this will install it for you.

.. warning::
    To add a dependancy the project must be initialized first.

PyProjectManager Installation
-----------------------------
* Once the initialization is done, we can start installing the project to your current directory.
* To install a project using PyyProjectManager::

    > pyPman install -p <projectName>
    Installing <projectName> in <current directory path>
