import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = [
            'pyramid',
            'requests',
            'elasticsearch',
            'python-memcached',
            'python-binary-memcached',
            'pyramid-debugtoolbar',
            'dogpile.cache',
            'pylibmc',
            'thriftpy',
            'thriftpywrap',
            'pyramid_debugtoolbar',
            'waitress',
            'xylose>=1.16.5',
            'articlemetaapi>=1.5.10'
           ]

test_requires = []

setup(
    name='citedby',
    version='2.13.9',
    description='API RESTFul to retrieve citations from SciELO articles to a given DOI, Article Title or SciELO ID',
    author='SciELO',
    author_email='scielo-dev@googlegroups.com',
    url='http://docs.scielo.org/projects/citedby/en/latest/',
    packages=['citedby'],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Operating System :: POSIX :: Linux",
        "Topic :: System",
        "Topic :: Utilities",
    ],
    dependency_links=[
        "git+https://github.com/scieloorg/thriftpy-wrap@0.1.1#egg=thriftpywrap"
    ],
    license='BSD 2-Clause',
    keywords='SciELO CitedBy API RESTFul',
    include_package_data=True,
    zip_safe=False,
    setup_requires=["nose>=1.0", "coverage"],
    install_requires=requires,
    tests_require=test_requires,
    test_suite="nose.collector",
    entry_points="""\
    [paste.app_factory]
    main = citedby:main
    [console_scripts]
    citedby_thriftserver = citedby.thrift.server:main
    citedby_load_citations = proc.loaddata:main
    """,
)
