import os
import pip
from pip.req import parse_requirements
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

install_reqs = parse_requirements('requirements.txt',
                                  session=pip.download.PipSession())

requires = [str(ir.req) for ir in install_reqs]

test_requires = requires+['mocker']

setup(name='citedby',
      version='1.0',
      description='API RESTFul to retrieve citations from SciELO articles to a given DOI, Article Title or SciELO ID',
      long_description=open(os.path.join(here, 'README.md')).read() + '\n\n' +
                       open(os.path.join(here, 'CHANGES.txt')).read(),
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
      license='BSD 2-Clause',
      url='http://docs.scielo.org/projects/citedby/en/latest/',
      keywords='SciELO CitedBy API RESTFul',
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