#coding: utf-8
import os
import logging

import thriftpy
from thriftpy.rpc import make_client

logger = logging.getLogger(__name__)

logger.addHandler(logging.NullHandler())


articlemeta_thrift = thriftpy.load(os.path.join(os.path.dirname(
                               os.path.abspath(__file__)), 'thrift/articlemeta.thrift'))

client = make_client(articlemeta_thrift.ArticleMeta, 'articlemeta.scielo.org', 11720)


def get_all_identifiers(collection=None, limit=1000, offset_range=1000):
    """
    Get all identifiers by Article Meta Thrift

    :param offset_range: paging through RCP result, default:1000.

    :returns: return a generator with a tuple ``(collection, PID)``,
    ex.: (mex, S0036-36342014000100009)
    """

    offset = 0

    logger.debug('Get all identifiers from Article Meta, please wait... this while take while!')

    while True:
        idents = client.get_article_identifiers(collection=collection, limit=limit, offset=offset)

        if not idents:
            raise StopIteration

        for ident in idents:
            logger.debug('Get article with code: %s from: %s' %
                (ident.code, ident.collection))

            yield (ident.collection, ident.code)

        offset += offset_range


def get_article(code, collection):
    """
    Get article meta data by code

    :param code: SciELO PID(Publisher Identifier)
    :param collection: collection acronym

    Endpoint: ``/api/v1/pid/?q=S0101-31222002000100038``

    :returns: Article JSON
    """
    logger.debug('Get article with code: %s by collection %s' % (code, collection))

    return client.get_article(collection, code, True)
