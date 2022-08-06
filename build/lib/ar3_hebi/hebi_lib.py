# ########################################################################
# (C) Arthur Rabatin - All Rights Reserved. www.rabatin.com
# See LICENSE.txt.txt for License Information
# #########################################################################

import sys
from pathlib import Path
import ar3_hebi.hebi_helper

class VenvEnv:

  def __init__(self):
    self.vens = {}

  def add_from_path(self, venvpath_root: Path):
    venvpath_root = Path(venvpath_root)
    if not venvpath_root.is_dir():
      return
    loaded_paths = list(Path(venvpath_root).iterdir())
    for p in loaded_paths:
      # print(p)
      if Path(p / 'pyvenv.cfg').is_file():
        with open(Path(p / 'pyvenv.cfg'), 'r', encoding='utf8') as fp:
          cfg = fp.readlines()
        if p.name in self.vens:
          print(
            f'Ingnoring {p.name}: Error - Environment found in  {p} but already found in {self.vens[p.name]["path"]}',
            file=sys.stderr)
        else:
          self.vens[p.name] = {}
          self.vens[p.name]['path'] = p
          for line in cfg:
            self.vens[p.name][line.split('=')[0].strip()] = line.split('=')[1].strip()



def activate_on_linux(venv:VenvEnv, environment_name: str) -> None:
  if not ar3_hebi.hebi_helper.is_linux():
    raise Exception('Platform is not Linux')
  activate_path = Path(Path(venv.vens[environment_name]['path']) / 'bin' / 'activate')
  if not activate_path.is_file():
    raise Exception(f'Is not a file: {activate_path}')
  dummy_hebi = Path('~/bin/__hebi_dummy__.tmp').expanduser()
  if not dummy_hebi.is_file():
    with open(dummy_hebi, 'w', encoding='utf8') as f:
      f.write('# Dummy Contents - Ignore\n')
  brc = BashRC(Path('~/bin/__hebi__.tmp').expanduser())
  if not brc.has_hebi_info:
    brc.write_hebi_info(activate_path)
  with open(Path('~/bin/__hebi__.tmp').expanduser(), 'w', encoding='utf8') as f:
    f.write(str(activate_path))


def read_deactive_command(activate_file: Path):
  if not activate_file.is_file():
    raise Exception(f'Does not exist {activate_file}')
  with open(activate_file, 'r', encoding='utf8') as f:
    rl = f.readlines()
  start_deactivate = -1
  end_deactivate = -1
  for idx, l in enumerate(rl):
    if l.startswith('deactivate ()'):
      start_deactivate = idx
    if start_deactivate >= 0:
      if l.startswith('}'):
        end_deactivate = idx
  return rl[start_deactivate:end_deactivate + 1]


class BashRC:
  HEBI_BEGIN = '# >>> HEBI Initialization >>>'
  HEBI_END = '# <<< HEBI Initialization <<<'

  def __init__(self, file_to_source: Path):
    self.source_file = Path(file_to_source).expanduser()
    self.bashrc = Path('~/.bashrc').expanduser()
    with open(self.bashrc, 'r', encoding='utf8') as f:
      rl = f.readlines()
    self.hebi_start = -1
    self.hebi_end = -1
    for idx, line in enumerate(rl):
      if line.startswith(BashRC.HEBI_BEGIN):
        self.hebi_start = idx
      if line.startswith(BashRC.HEBI_END):
        self.hebi_end = idx
    self.has_hebi_info = ((self.hebi_end - self.hebi_start) >= 2)
    # print(self.hebi_start, self.hebi_end, self.has_hebi_info)

  def write_hebi_info(self, activate_pathfile: Path):
    if self.has_hebi_info:
      raise Exception('Already has HEBI Info')
    with open(self.bashrc, 'a', encoding='utf8') as bashrc_f:
      bashrc_f.write('\n\n')
      bashrc_f.write('# *** DO NOT MODIFY THE HEBI INFORMATION MANUALLY ***\n')
      bashrc_f.write(f'{BashRC.HEBI_BEGIN}\n')
      bashrc_f.write(f'source `cat {self.source_file}`\n')
      bashrc_f.write(f'# Below the custom adoption of the deactivate command\n')
      deactive_text = read_deactive_command(activate_pathfile)
      if deactive_text[-1:][0] != '}\n':
        raise Exception('deactive_text unexpected' + str(deactive_text))
      deactive_text = deactive_text[:-1]
      dummy = Path('~/bin/__hebi_dummy__.tmp').expanduser()
      deactive_text.append('# Customization Start\n')
      deactive_text.append(f'    echo \"{dummy}\" > {self.source_file}\n')
      deactive_text.append('# Customization End\n')
      deactive_text.append('}\n')
      for code_line in deactive_text:
        bashrc_f.write(code_line)
      bashrc_f.write(f'{BashRC.HEBI_END}\n')
      bashrc_f.write('\n\n')


