.. Cited By SciELO documentation master file, created by
   sphinx-quickstart on Fri Nov 29 14:50:18 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===================
CitedBy Restful API
===================

API to retrieve citations from SciELO articles to a given DOI, Article Title or SciELO ID.

API URL: http://citedby.scielo.org

Current API Version: 2.18.15

---------
Libraries
---------

To facilitate the use of the SciELO CitedBy API, SciELO provides an Python Library compatible with
Python 3 and 2.

Source code: https://github.com/scieloorg/citedbyapi

How to Install
--------------

pip install citedbyapi


How to Use
----------

.. code-block:: python

    In [1]: from citedby import client

    In [2]: cl = client.RestfulClient()

    In [3]: cl.citedby_pid("S0074-02761998000200011")
    Out[3]:
    {'article': {'authors': [{'given_names': 'Cristina',
        'role': 'ND',
        'surname': 'Ferro',
        'xref': ['A01']},
       {'given_names': 'Estrella',
        'role': 'ND',
        'surname': 'Cárdenas',
        'xref': ['A01']},
       {'given_names': 'Dario',
        'role': 'ND',
        'surname': 'Corredor',
        'xref': ['A02']},
       {'given_names': 'Alberto',
        'role': 'ND',
        'surname': 'Morales',
        'xref': ['A01']},
       {'given_names': 'Leonard E',
        'role': 'ND',
        'surname': 'Munstermann',
        'xref': ['A03']}],
      'code': 'S0074-02761998000200011',
      'collection': 'scl',
      'doi': '10.1590/S0074-02761998000200011',
      'end_page': '199',
      'first_author': {'given_names': 'Cristina',
       'role': 'ND',
       'surname': 'Ferro',
       'xref': ['A01']},
      'issn': '0074-0276',
      'publication_year': '1998',
      'start_page': '195',
      'titles': ['Life Cycle and Fecundity Analysis of Lutzomyia shannoni (Dyar) (Diptera: Psychodidae)'],
      'total_received': 14,
      'translated_titles': None,
      'url': 'http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0074-02761998000200011&lng=en&tlng=en'},
     'cited_by': [{'authors': [{'given_names': 'María Angélica',
         'role': 'ND',
         'surname': 'Contreras-Gutiérrez',
         'xref': ['A01']},
        {'given_names': 'Iván Darío',
         'role': 'ND',
         'surname': 'Vélez',
         'xref': ['A01']},
        {'given_names': 'Charles',
         'role': 'ND',
         'surname': 'Porter',
         'xref': ['A03']},
        {'given_names': 'Sandra Inés',
         'role': 'ND',
         'surname': 'Uribe',
         'xref': ['A02']}],
       'code': 'S0120-41572014000300017',
       'end_page': '498',
       'first_author': {'given_names': 'María Angélica',
        'role': 'ND',
        'surname': 'Contreras-Gutiérrez',
        'xref': ['A01']},
       'issn': '0120-4157',
       'source': 'Biomédica',
       'start_page': '483',
       'titles': ['An updated checklist of Phlebotomine sand flies (Diptera: Psychodidae: Phlebotominae) from the Colombian Andean coffee-growing region',
        'Lista actualizada de flebotomíneos (Diptera: Psychodidae: Phlebotominae) de la región cafetera colombiana'],
       'url': 'http://www.scielo.org.co/scielo.php?script=sci_arttext&pid=S0120-41572014000300017&lng=en&tlng=en'},
      {'authors': [{'given_names': 'Ronildo Baiatone',
         'role': 'ND',
         'surname': 'Alencar',
         'xref': ['A01']}],
       'code': 'S0044-59672007000200016',
       'end_page': '292',
       'first_author': {'given_names': 'Ronildo Baiatone',
        'role': 'ND',
        'surname': 'Alencar',
        'xref': ['A01']},
       'issn': '0044-5967',
       'source': 'Acta Amazonica',
       'start_page': '287',
       'titles': ['Emergence of phlebotomine sandflies (Diptera: Psychodidade) in non-flooded forest floor in Central Amazon, Brazil: a modified emergence trap model',
        'Emergência de flebotomíneos (Diptera: Psychodidae) em chão de floresta de terra firme na Amazônia Central do Brasil: uso de um modelo modificado de armadilha de emergência'],
       'url': 'http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0044-59672007000200016&lng=en&tlng=en'},
      {'authors': [{'given_names': 'Jesús',
         'role': 'ND',
         'surname': 'Escovar',
         'xref': ['A01']},
        {'given_names': 'Felio J',
         'role': 'ND',
         'surname': 'Bello',
         'xref': ['A01']},
        {'given_names': 'Alberto',
         'role': 'ND',
         'surname': 'Morales',
         'xref': ['A01']},
        {'given_names': 'Ligia',
         'role': 'ND',
         'surname': 'Moncada',
         'xref': ['A02']},
        {'given_names': 'Estrella',
         'role': 'ND',
         'surname': 'Cárdenas',
         'xref': ['A01']}],
       'code': 'S0074-02762004000600012',
       'end_page': '607',
       'first_author': {'given_names': 'Jesús',
        'role': 'ND',
        'surname': 'Escovar',
        'xref': ['A01']},
       'issn': '0074-0276',
       'source': 'Memórias do Instituto Oswaldo Cruz',
       'start_page': '603',
       'titles': ['Life tables and reproductive parameters of Lutzomyia spinicrassa (Diptera: Psychodidae) under laboratory conditions'],
       'url': 'http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0074-02762004000600012&lng=en&tlng=en'}]}

Loading file with citations in memory
-------------------------------------

Para processos que demandam alta velocidade de processamento, o SciELO disponibiliza
um arquivo .json com todas as citações recebidas de documentos SciELO. O formato
segue o mesmo padrão do formato entregue pela API.

Para utilizar o arquivo é necessário fazer o download do mesmo em: http://static.scielo.org/citedby/citedbyapi.json.gz

(Este arquivo será atualizado semestralmente)

O arquivo deve ser depositado em qualquer local no servidor onde a biblioteca citebyapi está instalada.

Antes de utilizar a biblioteca é necessário configurar uma variável de ambiente que indica o local onde o arquivo foi depositado.

export CITEDBYAPI_HEAP_FILE=~/Documents/citations.json

Na ausência deste arquivo, todas as requisições serão feitas diretamente para API, que possui tempo de resposta reduzido.

-------------
Developer API
-------------

.. toctree::
   :maxdepth: 1

   endpoints