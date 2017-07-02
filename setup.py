try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='parsewrap',
      version='0.1',
      packages=['parsewrap'],
      entry_points = {
          'console_scripts': ['parsewrap = parsewrap.main:main']
      },
      description='Wrapper for different dependency parsers',
      url='https://github.com/vinit-ivar/parsewrap',
      author='Vinit Ravishankar',
      author_email='vinit.ravishankar@gmail.com',
      license='GPL',
      zip_safe=False)

