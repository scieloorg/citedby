# coding: utf-8

import requests
import unicodedata
import logging
import os
import re
import weakref
import threading
import string

try:
    from configparser import ConfigParser
except:
    from ConfigParser import ConfigParser

logger = logging.getLogger(__name__)

logger.addHandler(logging.NullHandler())

TAG_RE = re.compile(r'<[^>]+>')


class ThreadSafeIter(object):
    """Wraps an iterable for safe use in a threaded environment.
    """
    def __init__(self, it):
        self.it = iter(it)
        self.lock = threading.Lock()

    def __iter__(self):
        return self

    def __next__(self):
        with self.lock:
            return next(self.it)

    next = __next__


def remove_tags(text):
    return TAG_RE.sub('', text)


def cleanup_string(text):

    try:
        nfd_form = unicodedata.normalize('NFD', text.strip().lower())
    except TypeError:
        nfd_form = unicodedata.normalize('NFD', unicode(text.strip().lower()))

    cleaned_str = u''.join(x for x in nfd_form if x in string.ascii_letters or x == ' ')

    return remove_tags(cleaned_str).lower()


def dogpile_controller_key_generator(namespace, fn, *kwargs):

    fname = fn.__name__

    def generate_key(*the_args, **the_kwargs):

        tp = tuple([
            str(namespace),
            str(fname),
            str(the_args[1:]),
            tuple(the_kwargs.items())
        ])

        return str(hash(tp))

    return generate_key


def fetch_data(resource):
    """
    Fetches any resource.
    :param resource: any resource
    :returns: requests.response object
    The param resource must be a valid URL
    """
    try:
        response = requests.get(resource)
    except requests.exceptions.RequestException as e:
        logger.error('%s. Unable to connect to resource.', e)
    else:
        logger.debug('Get resource: %s', resource)
        return response


def load_from_crossref(doi):
    """
    Get the metadata from crossref
    """
    response = fetch_data('http://search.crossref.org/dois?q=%s' % doi).json()

    if len(response) == 0 or 'title' not in response[0]:
        return None

    return response[0]


def format_citation(citations):
    """
    Format the citation like:
        [{
            url: "http://www.scielo.cl/scielo.php?script=sci_arttext&pid=S0716-10182009000100012&lng=en&tlng=en",
            source: "Revista chilena de infectología",
            issn: "0716-1018",
            start_page: "105",
            end_page: "110",
            first_author: {
                surname: "ARAÚJO",
                given_names: "E. C."
            },
            code: "S0716-10182009000100012",
            title: "Fiebre tifoidea en Santiago, Chile y su control"
            authors: [
                {
                    surname: "ARAÚJO",
                    given_names: "E. C."
                }
            ],
        }]
    """
    l = []

    if not citations:
        return l

    for citation in citations['hits']['hits']:

        citation_source = citation['_source']

        l.append({
                'titles': citation_source.get('titles', ''),
                'url': citation_source.get('url', ''),
                'code': citation_source.get('code', ''),
                'source': citation_source.get('source', ''),
                'issn': citation_source.get('issn', ''),
                'authors': citation_source.get('authors', ''),
                'end_page': citation_source.get('end_page', ''),
                'start_page': citation_source.get('start_page', ''),
                'first_author': citation_source.get('first_author', '')})
    return l


class SingletonMixin(object):
    """
    Adds a singleton behaviour to an existing class.
    weakrefs are used in order to keep a low memory footprint.
    As a result, args and kwargs passed to classes initializers
    must be of weakly refereable types.
    """
    _instances = weakref.WeakValueDictionary()

    def __call__(cls, *args, **kwargs):
        key = (cls, args, tuple(kwargs.items()))

        if key in cls._instances:
            return cls._instances[key]

        new_instance = super(type(cls), cls).__new__(cls, *args, **kwargs)
        cls._instances[key] = new_instance

        return new_instance


class Configuration(SingletonMixin):
    """
    Acts as a proxy to the ConfigParser module
    """
    def __init__(self, fp, parser_dep=ConfigParser):
        self.conf = parser_dep()

        # Python 3 and 2 compatibility
        try:
            self.conf.read_file(fp)
        except:
            self.conf.readfp(fp)

    @classmethod
    def from_env(cls):
        try:
            filepath = os.environ['CITEDBY_SETTINGS_FILE']
        except KeyError:
            raise ValueError('missing env variable CITEDBY_SETTINGS_FILE')

        return cls.from_file(filepath)

    @classmethod
    def from_file(cls, filepath):
        """
        Returns an instance of Configuration

        ``filepath`` is a text string.
        """
        fp = open(filepath)
        return cls(fp)

    def __getattr__(self, attr):
        return getattr(self.conf, attr)

    def items(self):
        """Settings as key-value pair.
        """
        return [(section, dict(self.conf.items(section, raw=True))) for
                section in [section for section in self.conf.sections()]]
