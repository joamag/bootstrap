#!/bin/sh
# -*- coding: utf-8 -*-

# João Magalhães Bootstrap Scripts
# Copyright (c) 2008-2020 João Magalhães
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

# __author__    = João Magalhães <joamag@gmail.com>
# __version__   = 1.0.0
# __revision__  = $LastChangedRevision$
# __date__      = $LastChangedDate$
# __copyright__ = Copyright (c) 2008-2020 João Magalhães
# __license__   = Apache License, Version 2.0

# sets the temporary variables
PYTHON_PATH=python

# executes the bootstrap script after
# the download of the current version
$PYTHON_PATH bootstrap.py --download
$PYTHON_PATH bootstrap.py --bootstrap

# exits the process
exit $?
