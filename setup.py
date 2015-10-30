import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = [
            'pyramid',
            'paster',
            'requests',
            'elasticsearch',
            'python-memcached',
            'python-binary-memcached',
            'dogpile',
            'dogpile.cache',
            'pylibmc',
            'thriftpy',
            'thriftpywrap',
            'fabric',
            'pyramid_debugtoolbar',
           ]

test_requires = requires+['nose']

setup(
    name='citedby',
    version='1.5',
    description='API RESTFul to retrieve citations from SciELO articles to a given DOI, Article Title or SciELO ID',
    long_description=open(os.path.join(here, 'README.md')).read() + '\n\n' + open(os.path.join(here, 'CHANGES.txt')).read(),
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
        "git+https://github.com/scieloorg/xylose@0.33#egg=xylose",
        "git+https://github.com/scieloorg/thriftpy-wrap@0.1.1#egg=thriftpywrap"
    ],
    author='SciELO',
    author_email='scielo-dev@googlegroups.com',
    license='BSD 2-Clause',
    url='http://docs.scielo.org/projects/citedby/en/latest/',
    keywords='SciELO CitedBy API RESTFul',
    packages=['citedby'],
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=test_requires,
    test_suite="citedby",
    entry_points="""\
    [paste.app_factory]
    main = citedby:main
    [console_scripts]
    citedby_thriftserver = citedby.thrift.server:main
    citedby_load_citations = proc.loaddata:main
    citedby_warmup = proc.warmup:main
    """,
)