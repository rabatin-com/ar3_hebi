# ########################################################################
# (C) Arthur Rabatin - All Rights Reserved. www.rabatin.com
# See LICENSE.txt.txt for License Information
# #########################################################################

"""
Helper functions which are also available in AR3 Util but we duplicate them here to reduce the
number of dependency imports we need to run this app
"""


import platform

def is_linux():
  return _is_specific_os('Linux')

def is_windows():
  return _is_specific_os('Windows')

def os_name():
  return platform.system()

def _is_specific_os(osname: str):
  if platform.system() not in ['Windows', 'Linux']:
    raise RuntimeError(f'Unexpected System found: {platform.system()}')
  return platform.system() == osname

