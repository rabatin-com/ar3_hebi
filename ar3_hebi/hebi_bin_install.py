# ########################################################################
# (C) Arthur Rabatin - All Rights Reserved. www.rabatin.com
# See LICENSE.txt.txt for License Information
# #########################################################################

import sys
import site
from pathlib import Path
import shutil
import os

INSTALL_PATH = Path('~/bin')

def run():
  install_path = INSTALL_PATH.expanduser()
  sys.stdout.write(f'Attempting to install scripts in {install_path}\n')
  sys.stdout.flush()
  if not install_path.is_dir():
    sys.stderr.write(f'Path does not exist: {install_path}. Create path before installling HEBI\n')
    return
  files = {
    'hebi.bash':None,
    'hebi_config.json':None
  }
  has_errors = False
  for x in site.getsitepackages():
    if Path(x).is_dir():
      for xx in Path(x).iterdir():
        print(xx.name)
        if str(xx.name).startswith('ar3_hebi'):
          if (xx / 'hebi.bash').is_file():
            files['hebi.bash'] = xx / 'hebi.bash'
          if (xx / 'hebi_config.json').is_file():
            files['hebi_config.json'] = xx / 'hebi_config.json'
  for k,v in files.items():
    print(k, '=>', v)
    if v is None:
      has_errors = True
      sys.stderr.write(f'Could not find value for {k}\n')
    else:
      sys.stdout.write(f'{v} => {install_path/v.name}\n')
      sys.stdout.flush()
  if has_errors:
    sys.stderr.write(f'Errors found. Nothing done\n')
    return
  else:
    for k, v in files.items():
      shutil.copy(v, install_path/v.name)
  os.symlink(src=str(Path(install_path/'hebi.bash')), dst=str(Path(install_path/'hebi')))


if __name__ == '__main__':
  run()

