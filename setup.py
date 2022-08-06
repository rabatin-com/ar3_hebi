from setuptools import setup, find_packages

import os

ar3_version = os.getenv('__AR3_HEBI__BUILD_VERSION__')
ar3_author = os.getenv('__AR3_HEBI__BUILD_AUTHOR__')


setup(
  name='ar3_hebi',
  version=ar3_version,
  packages=['ar3_hebi'],
  package_data={'':['hebi.bash', 'hebi_config.json']},
  url='www.rabatin.com',
  license='MIT',
  author=ar3_author,
  author_email='webmaster@rabatin.net',
  description='Python Environment Helper'
)
