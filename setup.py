#from distutils.core import setup
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
  name = 'ionopy',         # How you named your package folder (MyLib)
  packages = ['ionopy','ionopy.process','ionopy.analysis'],   # Chose the same as "name"
  version = '0.0.9',      # Start with a small number and increase it with every change you make
  license='gpl-3.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Package for processing and analysis of GNSS data',   # Give a short description about your library
  author = 'Dinil Bose P',                   # Type in your name
  author_email = 'dinilbose@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/dinilbose/ismrpy',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/dinilbose/ionopy/archive/0.0.6.tar.gz',    # I explain this later on
  keywords = ['ionopy', 'pandas'], # Keywords that define your package best
  long_description=long_description,
  long_description_content_type="text/markdown",
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Science/Research',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',   # Again, pick a license
    'Programming Language :: Python :: 3.6',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.6',
  ], install_requires=['pandas>=0.13.1'],setup_requires=["numpy","pandas"],include_package_data=True,


)
