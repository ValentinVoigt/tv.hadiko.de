import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

requires = [
    'pyramid',
    'pyramid_mako',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'python-dateutil',
    'awesome-slugify',
    'pytz'
    ]

setup(name='tv.hadiko.de',
      version='0.0',
      description='tv.hadiko.de',
      long_description=README,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='tvhadikode',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = tvhadikode:main
      [console_scripts]
      tv_create_tables = tvhadikode.scripts.create_tables:main
      tv_import_services = tvhadikode.scripts.import_services:main
      tv_import_epg = tvhadikode.scripts.import_epg:main
      """,
      )
