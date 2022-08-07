#!/usr/bin/env bash
# ########################################################################
# (C) Arthur Rabatin - All Rights Reserved. www.rabatin.com
# See LICENSE.txt for License Information
# #########################################################################


if [ -f "setup.py" ]; then
    echo "About to update requirements.txt and binary distribution"
else
    echo "Must be called from the directory where setup.py is located"
    echo "Exiting"
    exit 1
fi

source version_info.bash

set_version_info

rm -rf dist
rm -rf build
rm -f requirements.txt
rm -rf ar3_hebi.egg-info
pip freeze > requirements.txt
python3 -m pip install --upgrade build
python3 -m build

remove_version_info
