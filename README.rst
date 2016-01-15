.. image:: https://travis-ci.org/sneben/motd-info.svg?branch=master
    :target: https://travis-ci.org/sneben/motd-info

.. image:: https://coveralls.io/repos/sneben/motd-info/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/sneben/motd-info?branch=master

=========
motd-info
=========

Overview
========
A script that displays several informations. It is attended to run on
every login of a user as addition to the **motd** output.

Installation
============
To build the project follow these steps:

.. code-block:: console

   $ virtualenv venv
   $ source venv/bin/activate
   $ pip install pybuilder
   $ pyb install_dependencies
   $ pyb -v

The generated install source can be found in ``target/dist/motd-info-0.1/``.
Do what ever you want with the ``setup.py``.

Configuration
=============
To define the disks, which should be displayed, create the file
``/etc/default/motd-info`` with the following **json** content:

.. code-block:: json

    {
        "users": true,
        "ram": true,
        "drives": [
            "/dev/sda1"
        ]
    }

Execute the script on every login
---------------------------------
To execute the script on every login put the following script to
``/etc/profile.d/``:

.. code-block:: bash

    #!/bin/bash

    function command_exists {
        type "$1" &> /dev/null
    }

    if [[ "$(whoami)" == "user" ]]; then
        command_exists motd-info && motd-info
    fi

Change ``user`` to your login user. The above example prevents the execution
on every e.g. ``sudo -i``.

Output
======
RAM
---
The memory usage is calculated by substracting the cached memory
from the used memory.

Example
-------
The output of the script looks like:

.. code-block:: text

    Logged in users:

    USERNAME       FROM                   LOGIN@
    user           192.168.0.1            2016-01-09 23:32:32

    Memory/Disk usage on server:

    RAM (208.3M):
    [================>................................................................] 20.89%

    /dev/sda1 (1.5G):
    [========>........................................................................] 10.50%

License
=======
Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
