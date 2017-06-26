.. Cited By SciELO documentation master file, created by
   sphinx-quickstart on Fri Nov 29 14:50:18 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

API Endpoints
=============

The API endpoints are available at: http://citedby.scielo.org

/pid/
-----

Retrieve “cited by” documents of a given PID (SciELO ID)

Parameters:

+------------+-----------------------------------------------------+-------------+
| Paremeter  | Description                                         | Mandatory   |
+============+=====================================================+=============+
| **q**      | PID (SciELO) or any article unique code, required   | yes         |
+------------+-----------------------------------------------------+-------------+
| metaonly   | get only the article meta data without the citaitons| No          |
+------------+-----------------------------------------------------+-------------+
| callback   | JSONP callback method                               | No          |
+------------+-----------------------------------------------------+-------------+

Mandatory Parameters: *q* PID (SciELO) or any article unique code


``GET /api/v1/pid/?q=S0100-84551997000100001``


Response::


    {
        "article": {
            "total_received": 1,
            "code": "S0100-84551997000100001",
            "titles": [
                "Chromosome polymorphism in Ctenomys minutus (Rodentia-Octodontidae)"
            ],
            "first_author": {
                "surname": "Freitas"
            },
            "issn": "0100-8455",
            "collection": "scl",
            "total_granted": 26,
            "source": "Brazilian Journal of Genetics",
            "publication_year": "1997",
            "authors": [
                {
                    "surname": "Freitas",
                    "given_names": "Thales Renato O. de"
                }
            ],
            "url": "http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0100-84551997000100001&lng=en&tlng=en",
            "translated_titles": {
                "en": "Chromosome polymorphism in Ctenomys minutus (Rodentia-Octodontidae)"
            },
            "doi": "10.1590/S0100-84551997000100001"
        },
        "cited_by": [
            {
                "start_page": "2684",
                "title": "Activation of rabbit muscle phosphofructokinase by F-actin and reconstituted thin filaments",
                "first_author": {
                    "surname": "Liou",
                    "given_names": "R-S"
                },
                "publication_year": "1980",
                "source": "Biochemistry",
                "authors": [
                    {
                        "surname": "Liou",
                        "given_names": "R-S"
                    },
                    {
                        "surname": "Anderson",
                        "given_names": "S"
                    }
                ],
                "end_page": "2688"
            }
        ]
    }


``GET /api/v1/pid/?q=S0074-02761936000400003&metaonly=true``

Response::


    {
        "article": {
            "total_received": 1,
            "code": "S0100-84551997000100001",
            "titles": [
                "Chromosome polymorphism in Ctenomys minutus (Rodentia-Octodontidae)"
            ],
            "first_author": {
                "surname": "Freitas"
            },
            "issn": "0100-8455",
            "collection": "scl",
            "total_granted": 26,
            "source": "Brazilian Journal of Genetics",
            "publication_year": "1997",
            "authors": [
                {
                    "surname": "Freitas",
                    "given_names": "Thales Renato O. de"
                }
            ],
            "url": "http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0100-84551997000100001&lng=en&tlng=en",
            "translated_titles": {
                "en": "Chromosome polymorphism in Ctenomys minutus (Rodentia-Octodontidae)"
            },
            "doi": "10.1590/S0100-84551997000100001"
        }
    }


/doi/
-----

Retrieve “cited by” documents of a given DOI (Document Objects Identifier)

Parameters:

+------------+-----------------------------------------------------+-------------+
| Paremeter  | Description                                         | Mandatory   |
+============+=====================================================+=============+
| **q**      | DOI(Document Objects Identifier), required          |yes          |
+------------+-----------------------------------------------------+-------------+
| metaonly   | get only the article meta data without the citaitons| No          |
+------------+-----------------------------------------------------+-------------+
| callback   | JSONP callback method                               | No          |
+------------+-----------------------------------------------------+-------------+


``GET /api/v1/doi/?q=10.1590/S1679-39512007000300011``


Response::


    {
        "article": {
            "total_cited_by": 2,
            "author": "",
            "year": "2007",
            "title": [
                "Tecnologia Social de Mobilização para Arranjos Produtivos Locais: uma proposta de aplicabilidade"
            ]
        },
        "cited_by": [
            {
                "url": "http://www.scielo.br/scielo.php?script=sci_arttext&pid=S1679-39512009000400001&lng=en&tlng=en",
                "source": "Cadernos EBAPE.BR",
                "issn": "1679-3951",
                "titles": [
                    "Environment, people and work, clusters beyond economic development in the opal mining in Pedro II, Piauí",
                    "Ambiente, pessoas e labor: APLs além do desenvolvimento econômico na mineração de opalas em Pedro II, no Piauí"
                ],
                "code": "S1679-39512009000400001"
            },
            {
                "url": "http://www.scielo.br/scielo.php?script=sci_arttext&pid=S1984-92302011000200004&lng=en&tlng=en",
                "source": "Organização & Sociedade",
                "issn": "1984-9230",
                "titles": [
                    "Identification of the challenges to the local productive arrangement of information technology in Fortaleza-CE",
                    "Identificação dos desafios do arranjo produtivo local de tecnologia da informação de Fortaleza-CE"
                ],
                "code": "S1984-92302011000200004"
            }
        ]
    }


``GET /api/v1/doi/?q=10.1590/S1679-39512007000300011&metaonly=true``


Response::


    {
        "article": {
            "total_cited_by": 2,
            "author": "",
            "year": "2007",
            "title": [
                "Tecnologia Social de Mobilização para Arranjos Produtivos Locais: uma proposta de aplicabilidade"
            ]
        }
    }

/meta/
------

Retrieve “cited by” documents of a given parameter

Parameters:

+------------+-----------------------------------------------------+-------------+
| Paremeter  | Description                                         | Mandatory   |
+============+=====================================================+=============+
| **title**  | Title of the article required                       | Yes         |
+------------+-----------------------------------------------------+-------------+
| author     | Name of the first author                            | No          |
+------------+-----------------------------------------------------+-------------+
| year       | Year of the article publication                     | No          |
+------------+-----------------------------------------------------+-------------+
| callback   | JSONP callback method                               | No          |
+------------+-----------------------------------------------------+-------------+

``GET /api/v1/meta/?title=The psychiatric comorbidity of epilepsy``

.. attention::
    research in this endpoint is more accurate when used with all parameters


Response::


    {
        "article": {
            "title": "The psychiatric comorbidity of epilepsy",
            "total_cited_by": 31,
            "year": "",
            "author": ""
        },
        "cited_by": [
            {
                "url": "http://www.scielo.br/scielo.php?script=sci_arttext&pid=S1676-26492011000200006&lng=en&tlng=en",
                "source": "Journal of Epilepsy and Clinical Neurophysiology",
                "issn": "1676-2649",
                "titles": [
                    "Psychiatric and behavioral effects of the antiepileptic drugs and their action as mood stabilizers",
                    "Efeitos psiqui\u00e1tricos e comportamentais das drogas antiepil\u00e9pticas e sua a\u00e7\u00e3o como moduladores de humor"
                ],
                "code": "S1676-26492011000200006"
            },
            {
                "url": "http://www.scielo.br/scielo.php?script=sci_arttext&pid=S1676-26492010000400007&lng=en&tlng=en",
                "source": "Journal of Epilepsy and Clinical Neurophysiology",
                "issn": "1676-2649",
                "titles": [
                    "Translation and cross-cultural adaptation of the Interictal Dysphoric Disorder Inventory (IDDI)",
                    "Tradu\u00e7\u00e3o e adapta\u00e7\u00e3o transcultural do Interictal Dysphoric Disorder Inventory (IDDI) para o Brasil"
                ],
                "code": "S1676-26492010000400007"
            }
        ]
    }


``GET /api/v1/meta/?title=The psychiatric comorbidity of epilepsy&metaonly=true``


Response::


    {
        "article": {
            "title": "The psychiatric comorbidity of epilepsy",
            "total_cited_by": 31,
            "year": "",
            "author": ""
        }

    }
