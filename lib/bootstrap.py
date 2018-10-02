#!/usr/bin/python
# -*- coding: utf-8 -*-

# João Magalhães Bootstrap Scripts
# Copyright (c) 2008-2018 João Magalhães
#
# This file is part of João Magalhães Bootstrap Scripts.
#
# João Magalhães Bootstrap Scripts is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# João Magalhães Bootstrap Scripts is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# João Magalhães Bootstrap Scripts. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@gmail.com>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2018 João Magalhães"
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import os
import sys
import stat
import subprocess

import urllib #@UnusedImport

try: import urllib2
except ImportError: urllib2 = None

try: import urllib.request
except ImportError: urllib.request = None

PYTHON_3 = sys.version_info[0] >= 3
""" Global variable that defines if the current python
interpreter is at least python 3 compliant, this is used
to take some of the conversion decision for runtime """

VERBOSE = True
""" The default verbosity level to be used during the
execution of the bootstrap commands """

BASE_ADDRESS = "https://github.com/joamag/bootstrap/raw/master/%s"
""" The base address to the remote location
of the repository to retrieve the file """

BOOTSTRAP_COMMANDS = {
    "github" : (
        "git clone --recursive git@github.com:joamag/{0}.git {0} {1}",
        "cd {0} && git submodule init && git submodule update && git submodule foreach git checkout master"
    ),
    "bitbucket" : (
        "git clone --recursive git@bitbucket.org:joamag/{0}.git {0} {1}",
        "cd {0} && git submodule init && git submodule update && git submodule foreach git checkout master"
    )
}
""" The list of commands to be used for the bootstrap
operation for a repository """

UPDATE_COMMANDS = {
    "github" : (
        "cd {0} && git pull {1} && git fetch --prune && git submodule init && git submodule update && git submodule foreach git checkout master && git submodule foreach git pull",
    ),
    "bitbucket" : (
        "cd {0} && git pull {1} && git fetch --prune && git submodule init && git submodule update && git submodule foreach git checkout master && git submodule foreach git pull",
    )
}
""" The list of commands to be used for the update
operation for a repository """

FILES = {
    "nt" : (
        "lib/bootstrap.py",
        "win32/bootstrap.bat",
        "win32/update.bat"
    ),
    "unix" : (
        ("lib/bootstrap.py", stat.S_IEXEC) ,
        ("unix/bootstrap.sh", stat.S_IEXEC),
        ("unix/update.sh", stat.S_IEXEC)
    )
}
""" The map that defines the various sequences of files
to be used for retrieval under each of the os names """

REPOSITORIES = {
    "github" : (
        "aplayer",
        "binac",
        "bootstrap",
        "doers",
        "dump",
        "examples_java",
        "generator",
        "goers",
        "hello_kotlin",
        "hello_node",
        "hello_scala",
        "hello_solidity",
        "huffman",
        "invite",
        "joamag_neo",
        "mingus",
        "ptorrent",
        "scully",
        "simplefs",
        "snippets",
        "viewer",
        "weddy"
    ),
    "bitbucket" : (
    )
}
""" The map of services associated with a list of repositories
that will be used for the operation of bootstrap and update """

REPOSITORIES_MINIMAL = {
    "github" : ()
}
""" The map of services associated with a list of repositories
that will be used for the operation of bootstrap and update, these
commands will only be used in the minimal mode """

if PYTHON_3: STRINGS = (str,)
else: STRINGS = (str, unicode) #@UndefinedVariable

def urlopen(*args, **kwargs):
    if PYTHON_3: return urllib.request.urlopen(*args, **kwargs)
    else: return urllib2.urlopen(*args, **kwargs) #@UndefinedVariable

def bootstrap(minimal = False):
    # retrieves the proper repositories list according
    # to the value of the minimal flag
    repositories = minimal and REPOSITORIES_MINIMAL or REPOSITORIES

    # iterates over each of the repositories
    # and executes the commands for the bootstrap
    # operation on each of them
    for service, names in repositories.items():
        for repository in names:
            is_sequence = type(repository) in (list, tuple)
            if is_sequence: repository, extra = repository
            else: extra = ""
            exists = os.path.exists(repository)
            if not exists: _bootstrap(service, repository, extra = extra)

def _bootstrap(service, repository, extra = ""):
    # iterates over each of the bootstrap commands
    # and creates the "final" command value using
    # the repository value and then executes it
    bootstrap_commands = BOOTSTRAP_COMMANDS.get(service, ())
    for bootstrap_command in bootstrap_commands:
        command = bootstrap_command.format(repository, extra)
        execute(command)

def update(minimal = False):
    """
    "Runs" the virtual update operation under
    the current directory for all of the repositories
    registered in the current script.

    :type minimal: bool
    :param minimal: If the update operation should use
    the minimal repositories list for operation.
    """

    # retrieves the proper repositories list according
    # to the value of the minimal flag
    repositories = minimal and REPOSITORIES_MINIMAL or REPOSITORIES

    # iterates over each of the repositories
    # and executes the commands for the update
    # operation on each of them
    for service, names in repositories.items():
        for repository in names:
            is_sequence = type(repository) in (list, tuple)
            if is_sequence: repository, extra = repository
            else: extra = ""
            _update(service, repository, extra = extra)

def _update(service, repository, extra = ""):
    # iterates over each of the update commands
    # and creates the "final" command value using
    # the repository value and then executes it
    update_commands = UPDATE_COMMANDS.get(service, ())
    for update_command in update_commands:
        if not os.path.exists(repository): _bootstrap(service, repository)
        command = update_command.format(repository, extra)
        execute(command)

def execute(command, verbose = VERBOSE):
    # in case the verbose flag is set prints the command
    # string then creates a new subprocess with the shell
    if verbose: print(command)
    subprocess.call(command, shell = True)

def download():
    # retrieves the normalized version of the
    # operative system name (normalized to unix)
    # then uses it to retrieve the list of files
    os_name = os.name == "nt" and "nt" or "unix"
    files = FILES.get(os_name, [])

    # iterates over each of the files to retrieve
    # it from the remote location
    for _file in files:
        # checks the file type and in case it's a string
        # default the file structure into a tuple with the
        # file (name) and an unset (invalid) mode
        file_type = type(_file)
        if file_type in STRINGS: _file = (_file, None)

        # unpacks the file structure into the name of the file
        # and the file (execution) mode
        name, mode = _file

        # opens the remove location retrieving the data
        # and then uses it to populate the associated file
        remote = urlopen(BASE_ADDRESS % name)
        contents = remote.read()
        base = os.path.basename(name)
        file = open(base, "wb")
        try: file.write(contents)
        finally: file.close

        # in case the mode value is not set nothing more
        # to be done, must continue the loop
        if not mode: continue

        # retrieves the current state from the file and
        # uses it to retrieve its current mode and or it
        # with the requested mode value and set it
        _stat = os.stat(base)
        _mode = _stat.st_mode
        os.chmod(base, _mode | mode)

if __name__ == "__main__":
    if len(sys.argv) < 2: exit(0)
    command = sys.argv[1]
    if command == "--bootstrap": bootstrap()
    if command == "--update": update()
    if command == "--download": download()
    if command == "--update-minimal": update(minimal = True)
    if command == "--download-minimal": download(minimal = True)
else:
    __path__ = []
