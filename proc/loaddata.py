#!/usr/bin/python
# !coding: utf-8

import os
import sys
import json
import textwrap
import optparse
import logging.config
from datetime import datetime
from datetime import timedelta
import unicodedata
import re
import time

from pyramid.settings import aslist
from xylose.scielodocument import Article

from citedby import utils
from citedby.controller import controller, articlemeta

logger = logging.getLogger(__name__)

config = utils.Configuration.from_env()
settings = dict(config.items())

TAG_RE = re.compile(r'<[^>]+>')

IGNORE_LIST = (
    'spa_0102-311X',
    'spa_1413-8123',
    'spa_2237-9622',
    'spa_1414-3283',
    'spa_0213-9111',
    'spa_1555-7960',
    'spa_1415-790X',
    'spa_0213-9111',
    'spa_0864-3466',
    'spa_0213-9111',
    'spa_0124-0064',
    'spa_0034-8910',
    'spa_1135-5727',
    'spa_0213-9111',
    'spa_1726-4634',
    'spa_1851-8265',
    'spa_0036-3634'
)

FROM_DATE = (datetime.now()-timedelta(60)).isoformat()[:10]

def _config_logging(logging_level='INFO', logging_file=None):

    allowed_levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger.setLevel(allowed_levels.get(logging_level, 'INFO'))

    if logging_file:
        hl = logging.FileHandler(logging_file, mode='a')
    else:
        hl = logging.StreamHandler()

    hl.setFormatter(formatter)
    hl.setLevel(allowed_levels.get(logging_level, 'INFO'))

    logger.addHandler(hl)

    return logger

def remove_tags(text):
    return TAG_RE.sub('', text)

def cleanup_string(text):
    
    try:
        nfd_form = unicodedata.normalize('NFD', text.strip().lower())
    except:
        return text

    cleaned_str = u''.join(x for x in nfd_form if unicodedata.category(x)[0] == 'L' or x == ' ')

    return remove_tags(cleaned_str)


def citation_meta(document):
    """
    This function receives a article meta JSON, transform it in an citation
    dicitionary, look the response example.

    :param document: ArticleMeta Xylose Document

    This function only create keys that has content, ignore otherwise.

    :returns:
        {
          "url": "<DOAMIN>scielo.php?script=sci_arttext&pid=S0101-31222002000100038",
          "source": "Revista Brasileira de Sementes",
          "issn": "0101-3122",
          "code": "S0101-31222002000100038",
          "collection": "scl",
          "titles": ["Adequação do...", "Seconde title..."]
          "first_author": {role: "ND",
                           xref: ["A01"],
                           surname: "Moreira",
                           given_names: "Jessica Pronestino de Lima"},
          "publication_year": "2013",
          "citations":
          [{
              "source": "Anais da Academia Brasileira de Ciências",
              "first_author": "Moreira JK",
              "title": "Germination of Croton...",
              "publication_year": "2004"
           }]
        }
    """

    if document.citations:

        c_dict = {}

        c_dict['titles'] = []
        c_dict['url'] = document.html_url()
        c_dict['issn'] = document.journal.scielo_issn
        c_dict['pid'] = document.publisher_id
        c_dict['code'] = document.publisher_id
        c_dict['collection'] = document.collection_acronym
        c_dict['document_type'] = document.document_type

        if document.doi:
            c_dict['doi'] = document.doi

        if document.journal.title:
            c_dict['source'] = document.journal.title

        if document.translated_titles():
            c_dict['titles'] = [t for l, t in document.translated_titles().items() if t != None]

        if document.original_title():
            c_dict['titles'].append(cleanup_string(document.original_title()))

        if document.authors:
            c_dict['authors'] = document.authors

        if document.subject_areas:
            c_dict['subject_areas'] = document.subject_areas

        if document.first_author:
            c_dict['first_author'] = document.first_author

        if document.start_page:
            c_dict['start_page'] = document.start_page

        if document.end_page:
            c_dict['end_page'] = document.end_page

        if document.publication_date:
            c_dict['publication_year'] = document.publication_date[:4]

        for cit in document.citations:

            if cit.source:
                c_dict['reference_source'] = cit.source
                try:
                    c_dict['reference_source_cleaned'] = cleanup_string(cit.source)
                except:
                    c_dict['reference_source_cleaned'] = cit.source
            if cit.title():
                c_dict['reference_title'] = cit.title()
                c_dict['reference_title_cleaned'] = cleanup_string(cit.title())
            elif cit.chapter_title:
                c_dict['reference_title'] = cit.chapter_title
                c_dict['reference_title_cleaned'] = cleanup_string(cit.chapter_title)

            if cit.date:
                c_dict['reference_publication_year'] = cit.date[:4]

            if cit.authors:
                c_dict['reference_authors'] = cit.authors

            if cit.first_author:
                c_dict['reference_first_author'] = ' '.join([
                    cit.first_author.get('given_names', ''),
                    cit.first_author.get('surname', '')
                ])

            if cit.start_page:
                c_dict['reference_start_page'] = cit.start_page

            if cit.end_page:
                c_dict['reference_end_page'] = cit.end_page

            if cit.end_page:
                c_dict['reference_index_number'] = str(cit.index_number)

            c_dict['_id'] = '-'.join([
                document.collection_acronym,
                document.publisher_id,
                str(cit.index_number)
            ])

            yield c_dict

class PCitation(object):
    """
    Process citation getting articles from Article Meta
    """

    usage = """\
    %prog -f (full) index all citations OR -d (distinct) only difference
    between endpoints.

    This process collects all articles in the Article meta
    http://articlemeta.scielo.org and index in ES (elasticsearch).

    With this process it is possible to process all the citations or only difference
    between elasticsearch and Article Meta, use pcitations -h to verify the options list.

    Edit logging.ini to change logging definitions.
    """

    parser = optparse.OptionParser(
        textwrap.dedent(usage), version="prog 0.9 - beta")

    parser.add_option('-f', '--full', action='store_true',
                      help='update all documents and insert the difference')

    parser.add_option('-r', '--rebuild_index', action='store_true',
                      help='this will remove all data in ES and\
                             index all documents')

    parser.add_option(
        '--from_date',
        '-b',
        default=FROM_DATE,
        help='From processing date (YYYY-MM-DD). Default (%s)' % FROM_DATE
    )

    parser.add_option(
        '--logging_file',
        '-o',
        help='Full path to the log file'
    )

    parser.add_option(
        '--logging_level',
        '-l',
        default='DEBUG',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Logggin level'
    )

    def __init__(self, argv):
        self.started = None
        self.finished = None
        self.options, self.args = self.parser.parse_args(argv)
        _config_logging(self.options.logging_level, self.options.logging_file)

        hosts = aslist(settings['app:main'].get('elasticsearch_host', '127.0.0.1:9200'))
        index = settings['app:main'].get('elasticsearch_index', 'citations')

        self.controller = controller(
            hosts=hosts,
            timeout=60,
            sniff_on_start=True,
            sniff_on_connection_fail=True
        )

        self.articlemeta = articlemeta()

    def _duration(self):
        """
        Return datetime process duration
        """
        return self.finished - self.started

    def _string_json(self, data):
        """
        Method convert string to json handler some errors.

        :param data: string

        :returns: json
        """

        try:
            jdata = json.loads(data)
        except ValueError as e:
            logger.error(e)
        else:
            return jdata

    def _bulk(self):

        for document in self.articlemeta.documents():
            logger.debug('bulking document %s, %s' % (document.publisher_id, document.collection_acronym))

            if '_'.join([document.collection_acronym, document.scielo_issn]) in IGNORE_LIST:
                logger.debug('In ignore list, skippind document %s, %s' % (document.publisher_id, document.collection_acronym))
                continue

            attempts = 0
            for reference in citation_meta(document):
                logger.debug('bulking reference %s' % (reference['_id']))
                while True:
                    try:
                        self.controller.index_citation(reference, reference['_id'])
                        logger.debug('Reference loaded %s' % reference['_id'])
                        break
                    except:
                        attempts += 1
                        logger.warning('fail to bult: %s retry (%d/10) in 2 seconds' % (reference['_id'], attempts))
                        time.sleep(2)

                    if attempts == 10:
                        logger.error('fail to bult: %s' % reference['_id'])
                        break

    def _bulk_incremental(self, from_date=FROM_DATE):

        for event, document in self.articlemeta.documents_history(from_date=from_date):
            if event.event == 'delete':
                logger.debug('%s (%s) document %s, %s' % (event.event, event.date, event.code, event.collection))

                self.controller.del_citation(
                    event.collection,
                    event.code
                )
                logger.debug('document deleted %s, %s' % (event.code, event.collection))
                continue

            if event.event in ['update', 'add']:
                logger.debug('%s (%s) document %s, %s' % (event.event, event.date, document.publisher_id, document.collection_acronym))

                if '_'.join([document.collection_acronym, document.scielo_issn]) in IGNORE_LIST:
                    logger.debug('In ignore list, skippind document %s, %s' % (document.publisher_id, document.collection_acronym))
                    continue

                attempts = 0
                for reference in citation_meta(document):
                    logger.debug('bulking reference %s' % (reference['_id']))
                    while True:
                        try:
                            self.controller.index_citation(reference, reference['_id'])
                            logger.debug('Reference loaded %s' % reference['_id'])
                            break
                        except:
                            attempts += 1
                            logger.warning('fail to bult: %s retry (%d/10) in 2 seconds' % (reference['_id'], attempts))
                            time.sleep(2)

                        if attempts == 10:
                            logger.error('fail to bult: %s' % reference['_id'])
                            break

    def run(self):
        """
        Run the Loaddata switching between full and incremental indexation
        """

        self.started = datetime.now()

        logger.info('Load Data Script (index citation)')

        self.controller.load_mapping()

        logger.info('Get all ids from articlemeta')

        if self.options.full:
            logger.info('You have selected full processing... this will take a while')

            if self.options.rebuild_index:
                logger.info('This will remove EVERYTHING from your search index')
                self.controller.index_reset()

            self._bulk()

        else:
            logger.info('You have selected incremental processing... It will include, update and remove records according to ArticleMeta history change API.')

            self._bulk_incremental()

        self.finished = datetime.now()

        logger.info("Total processing time: %s sec." % self._duration())


def main(argv=sys.argv[1:]):

    command = PCitation(argv)

    return command.run()