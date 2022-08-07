#!/usr/bin/env python3
# ########################################################################
# (C) Arthur Rabatin - All Rights Reserved. www.rabatin.com
# See LICENSE.txt.txt for License Information
# #########################################################################


import argparse
import json
import platform
import shutil
import subprocess
import sys
import uuid
from pathlib import Path
import ar3_hebi.hebi_lib
import ar3_hebi.hebi_helper
from ar3_hebi.hebi_lib import activate_on_linux

VERSION = '0.1'

configfilelocations_searchlist = [Path('.'), Path('~/.venv'), Path('~/.ar3_hebi'), Path('~'),
                       Path('~/bin')]


def find_configfile(configfilename:str='hebi_config.json') -> Path:
  configfilename = Path(configfilename)
  configfile_ =None
  configfilelocations = list(map(lambda x: str(x.expanduser()), configfilelocations_searchlist))
  for loc in configfilelocations:
    if Path(loc / configfilename).is_file():
      configfile_ = Path(loc / configfilename)
      break
  if configfile_ is None:
    raise RuntimeError(f'Cannot find configfile {configfilename} in any expected path in {configfilelocations}')
  return configfile_

if ar3_hebi.hebi_helper.is_linux():
  PYTHON_EXEC = sys.executable
else:
  import warnings
  warnings.simplefilter('ignore', category=DeprecationWarning)
  from distutils import spawn
  PYTHON_EXEC = spawn.find_executable('python.exe')


if __name__ == '__main__':

  configfile = find_configfile()

  with open(configfile, 'r', encoding='utf8') as f:
    app_config = json.load(f)
  app_config['venv_path'] = str(Path(app_config['venv_path']).expanduser())

  venv = ar3_hebi.hebi_lib.VenvEnv()
  venv.add_from_path(app_config['venv_path'])

  parser = argparse.ArgumentParser(prog='PYENV Helper',
                                   usage='Print -h for help',
                                   formatter_class=argparse.RawTextHelpFormatter
                                   )

  parser.add_argument('--version', help='Displays Version Information',
                      action='store_true')

  parser.add_argument('--show_config', help='Shows Config', action='store_true')

  parser.add_argument('--list', help='Lists all environments', action='store_true')

  parser.add_argument('--long_list', help='Lists all environments', action='store_true')

  if ar3_hebi.hebi_helper.is_linux():
    parser.add_argument('--select_on_linux', help='Select from environments',
                        action='store_true')

  if ar3_hebi.hebi_helper.is_windows():
    parser.add_argument('--select', nargs=1, help='Select from environments',
                        action='store')

  parser.add_argument('--create', nargs=1,
                      help='Create an environment in the default location',
                      action='store')

  parser.add_argument('--delete', nargs=1,
                      help='Deletes environment',
                      action='store')


  parser.add_argument('--show_activate_path', nargs=1, help='Prints Activate Path',
                      action='store')

  parser.add_argument('--activate_on_linux', nargs=1, help='Activates VENV on Linux',
                      action='store')

  app_args = parser.parse_args()

  if app_args.version:
    print('HEBI VERSION', VERSION)
    print('Platform:', platform.version(), '\nPython Version:', platform.python_version())

  if app_args.show_config:
    print(f'Looking for {configfile.name} in {configfilelocations_searchlist}')
    print(f'Found {configfile.absolute()}')
    print(json.dumps(app_config, indent=2))

  if app_args.activate_on_linux:
    envname = app_args.activate_on_linux[0]
    activate_on_linux(venv, envname)

  if app_args.show_activate_path:
    envname = app_args.show_activate_path[0]
    activate_path = 'Undefined - Not Set'
    if ar3_hebi.hebi_helper.is_windows():
      activate_path = Path(Path(venv.vens[envname]['path']) / 'Scripts' / 'activate.bat')
    if ar3_hebi.hebi_helper.is_linux():
      activate_path = Path(Path(venv.vens[envname]['path']) / 'bin' / 'activate')
    print(activate_path)

  if app_args.list:
    for env in venv.vens:
      print(env)

  if app_args.long_list:
    for modulename, venv_data in venv.vens.items():
      version = venv_data.get('version')
      if not version:
        version = venv_data.get('version_info', 'Undefined')
      location = venv_data['path']
      print(modulename, ' Version:', version, ' Location:', location)

  if app_args.create:
    venv_name = app_args.create[0]
    if venv_name in venv.vens:
      print(f'Virtual Environment {venv_name} already exists', file=sys.stderr)
      exit(1)
    venv_full_path = Path(Path(app_config['venv_path']) / venv_name)
    cmd = f'{PYTHON_EXEC} -m venv {str(venv_full_path.expanduser())}'
    completed = subprocess.run(
      [PYTHON_EXEC, '-m', 'venv', str(venv_full_path.expanduser())])
    if completed.returncode != 0:
      print(f'Error in executing command {cmd}', file=sys.stderr)
      print(f'{completed.stderr}', file=sys.stderr)

  if app_args.delete:
    venv_name = app_args.delete[0]
    if venv_name not in venv.vens:
      print(f'Virtual Environment {venv_name} does not exist', file=sys.stderr)
      sys.exit(1)
    archive_path = Path(Path(app_config['venv_path']) / Path(
      'Archive') / f'{venv_name}-{uuid.uuid4()}').expanduser()
    archive_path.mkdir(parents=True, exist_ok=True)
    shutil.move(str(venv.vens[venv_name]['path']), str(archive_path))
    print(f'Removed {venv_name} into Archive')

  if ar3_hebi.hebi_helper.is_windows():
    if app_args.select:
      envlist = []
      for envname, data in venv.vens.items():
        envlist.append(envname)
      for e in envlist:
        print(f'{envlist.index(e)}: {e}')
      selection = input('Enter your selection: ')
      activate_path = Path(
        Path(venv.vens[envlist[int(selection)]]['path']) / 'Scripts' / 'activate.bat')
      created_outputfile = app_args.select[0]
      print(created_outputfile, activate_path)
      with open(created_outputfile, 'w', encoding='utf8') as f:
        f.write(str(activate_path))

  if app_args.select_on_linux:
    envlist = []
    for envname, data in venv.vens.items():
      envlist.append(envname)
    for e in envlist:
      print(f'{envlist.index(e)}: {e}')
    selection = input('Enter your selection: ')
    envname = envlist[int(selection)]
    activate_on_linux(venv, envname)
