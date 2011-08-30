
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
except IOError:
    README = CHANGES = ''

install_requires = [
    'pyramid',
    'sphinx',
    'gumball',
    ]

test_requires = [
    'WebTest',
    #'nose',
    #'coverage',
    ]



setup(name='bottlecap',
      version='0.1',
      description=(''),
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: JavaScript",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        #"License :: ???",
        ],
      keywords='wsgi pylons pyramid transaction',
      author="",
      author_email="",
      url="",
      license="",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=install_requires+test_requires,
      test_suite="bottlecap.tests",
      entry_points="""\
        """,
      )
