# AR3 Hebi

------
## Python virtual environment manager helper

### Overview

Hebi is a simple Python virtual environment manager that is losely
modeled after Anaconda's <i>conda</i> tool.

It provides an easy command line to list, create, remove and activate
Pythin virtual environments using the standard python implementation.

To see the options, type "hebi --help" after installation

It is designed to be cross platform, however all utility tools are currently
designed for Linux only

### Installlation

First, pip install (can be done in a virtual or the default environment)

`pip install http://www.rabatin.net/pydist/dist/ar3_hebi-<version number>-py3-none-any.whl`

This will install all relevant files in your current python environment

Second, execute from a command line:

`python -m ar3_hebi.hebi_bin_install`

This will install the bash script hebi.bash and the config file into your ~/bin 
directory.
It will fail if ~/bin does not exist.

Once installed, it will create a symbolic link 'hebi' to 'hebi.bash' for convenience

Hebi has been designed to use the minimum number of dependencies, so a
plain python installation should be sufficient. IAW, Hebi does not pollute 
the main python environment.

### Usage (Linux)

Type `hebi --help` to see all options

### Hebi in different environments

You need to pip install for every virtual environment, however, you
do not need to re-run the hebi_bin_install module 

Best practice is to install Hebi outside a virtual environment and 
not activate new venv from an existing venv, although the system will allow it

### Usage (Windows)

To be completed








