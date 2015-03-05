import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'waitress',
    ]

test_requires = requires+['mocker']

setup(name='citedby',
      version='1.0',
      description='Tool that retrieves documents citing a given PID, DOI or document title.',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Operating System :: POSIX :: Linux",
        "Topic :: System",
        "Topic :: Utilities",
        ],
      author='SciELO',
      author_email='scielo-dev@googlegroups.com',
      license='BSD 2 -clause',
      url='http://docs.scielo.org',
      keywords='scielo citedby',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=test_requires,
      test_suite="citedby",
      entry_points="""\
      [paste.app_factory]
      main = citedby:main
      """,
      )
