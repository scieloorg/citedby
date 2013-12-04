from xylose.scielodocument import Article
import utils
import unicodedata
import string

def remove_accents(data):
    return ''.join(x for x in unicodedata.normalize('NFKD', data) if unicodedata.category(x)[0] == 'L').lower()

def load_article_title_keys(article):
    titles = []

    if article.original_title():
        titles.append(remove_accents(article.original_title()))

    if article.translated_titles():
        for title in article.translated_titles().values():
            titles.append(remove_accents(title))

    return titles

def load_article(coll, pid):
    query = coll.find_one({'code': pid}, {'article': 1, 'title': 1})

    if not query:
        return None

    return Article(query)


def query_by_pid(coll, pid):
    article = load_article(coll, pid)

    if not article:
        return None

    title_keys = load_article_title_keys(article)

    query = coll.find({'citations_title_no_accents': {'$in': title_keys}}, {'article': 1, 'title': 1})

    citations = None
    if query:
        citations = []
        for doc in query:
            citation = Article(doc)
            meta = {
                'code': citation.publisher_id,
                'title': citation.original_title(),
                'issn': citation.any_issn(),
                'journal': citation.journal_title,
                'article_url': citation.html_url
            }
            citations.append(meta)

    article_meta = {
        'code': article.publisher_id,
        'title': article.original_title(),
        'issn': article.any_issn(),
        'journal': article.journal_title,
        'article_url': article.html_url,
    }
    
    return {'article': article_meta, 'cited_by': citations}

