=============
API Reference
=============

GET Services
=============

--------------------------------------------------------
Retrieve "cited by" documents of a given PID (SciELO ID)
--------------------------------------------------------

    **resource:** /api/v1/pid/

Mandatory Parameters
--------------------

    **q:** any code that uniquely represents an article

Query Sample
------------

    /api/v1/pid/?q=S0101-31222002000100038

Response Sample::

    {

        "article": {
            "url": "http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0101-31222002000100038",
            "source": "Revista Brasileira de Sementes",
            "issn": "0101-3122",
            "code": "S0101-31222002000100038",
            "title": "Adequação do teste de condutividade elétrica para determinar a qualidade fisiológica de sementes de jacarandá-da-bahia (Dalbergia nigra (Vell.) Fr.All. ex Benth.)"
        },
        "cited_by": [
            {
                "url": "http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0001-37652012000100020",
                "source": "Anais da Academia Brasileira de Ciências",
                "issn": "0001-3765",
                "code": "S0001-37652012000100020",
                "title": "Germination of Croton urucurana L. seeds exposed to different storage temperatures and pre-germinative treatments"
            },
            {
                "url": "http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0101-31222005000200020",
                "source": "Revista Brasileira de Sementes",
                "issn": "0101-3122",
                "code": "S0101-31222005000200020",
                "title": "Teste de condutividade elétrica para avaliação da qualidade fisiológica de sementes Sebastiania commersoniana (Bail) Smith & Downs - Euphorbiaceae"
            }
        ]
    }

--------------------------------------------
Retrieve "cited by" documents of a given DOI
--------------------------------------------

    **resource:** /api/v1/doi/

Mandatory Parameters
--------------------

    **q:** any code that uniquely represents an article

Query Sample
------------

    /api/v1/doi?q=10.1161/01.res.59.2.178

Response Sample::

    {

        "article": {
            "normalizedScore": 100,
            "doi": "http://dx.doi.org/10.1161/01.res.59.2.178",
            "title": "Power spectral analysis of heart rate and arterial pressure variabilities as a marker of sympatho-vagal interaction in man and conscious dog",
            "coins": "ctx_ver=Z39.88-2004&amp;rft_id=info%3Adoi%2Fhttp%3A%2F%2Fdx.doi.org%2F10.1161%2F01.res.59.2.178&amp;rfr_id=info%3Asid%2Fcrossref.org%3Asearch&amp;rft.atitle=Power+spectral+analysis+of+heart+rate+and+arterial+pressure+variabilities+as+a+marker+of+sympatho-vagal+interaction+in+man+and+conscious+dog&amp;rft.jtitle=Circulation+Research&amp;rft.date=1986&amp;rft.volume=59&amp;rft.issue=2&amp;rft.spage=178&amp;rft.epage=193&amp;rft.aufirst=M.&amp;rft.aulast=Pagani&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Ajournal&amp;rft.genre=article&amp;rft.au=M.+Pagani&amp;rft.au=+F.+Lombardi&amp;rft.au=+S.+Guzzetti&amp;rft.au=+O.+Rimoldi&amp;rft.au=+R.+Furlan&amp;rft.au=+P.+Pizzinelli&amp;rft.au=+G.+Sandrone&amp;rft.au=+G.+Malfatto&amp;rft.au=+S.+Dell%27Orto&amp;rft.au=+E.+Piccaluga",
            "fullCitation": "M. Pagani, F. Lombardi, S. Guzzetti, O. Rimoldi, R. Furlan, P. Pizzinelli, G. Sandrone, G. Malfatto, S. Dell'Orto, E. Piccaluga, 1986, 'Power spectral analysis of heart rate and arterial pressure variabilities as a marker of sympatho-vagal interaction in man and conscious dog', <i>Circulation Research</i>, vol. 59, no. 2, pp. 178-193",
            "score": 18.42057,
            "year": "1986"
        },
        "cited_by": [
            {
                "url": "http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0066-782X2012001200005",
                "source": "Arquivos Brasileiros de Cardiologia",
                "issn": "0066-782X",
                "code": "S0066-782X2012001200005",
                "title": "Efeitos da idade e da aptidão aeróbica na recuperação da frequência cardíaca em homens adultos"
            },
            {
                "url": "http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0100-879X1998000300015",
                "source": "Brazilian Journal of Medical and Biological Research",
                "issn": "1414-431X",
                "code": "S0100-879X1998000300015",
                "title": "A comparative analysis of preprocessing techniques of cardiac event series for the study of heart rhythm variability using simulated signals"
            }
        ]
    }

---------------------------------------------------------------------------
Retrieve "cited by" documents of a given title, author and publication year
---------------------------------------------------------------------------

    **resource:** /api/v1/meta/

Mandatory Parameters
--------------------

    **title:** a string that represents title of the article

Optional Parameters
-------------------

    **author:** a string that represents the **first author** of the article
    
    **year:** a string that represents the publication year of the article

Query Sample
------------

    /api/v1/meta?title=Power spectral analysis of heart rate and arterial pressure variabilities as a marker of sympatho-vagal interaction in man and conscious dog&author=M. Pagani&year=1986

    /api/v1/meta?title=Power spectral analysis of heart rate and arterial pressure variabilities as a marker of sympatho-vagal interaction in man and conscious dog

    .. warning:: The values may be different when giving more metadata.

Response Sample::

    { 
        'article':{
            "title": u'Power spectral analysis of heart rate and arterial pressure variabilities as a marker of sympatho-vagal interaction in man and conscious dog',
            "author": u'M. Pagani',
            "year": u"1986"
        },
        'cited_by':[{
                'code': u'S0104-07072013000100023',
                'title': u'title en',
                'issn': u'0104-0707',
                'source': u'Texto & Contexto - Enfermagem',
                'url': u'http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0104-07072013000100023'
            },{
                'code': u'S1414-81452012000300003',
                'title': u'title pt',
                'issn': u'1414-8145',
                'source': u'Escola Anna Nery',
                'url': u'http://www.scielo.br/scielo.php?script=sci_arttext&pid=S1414-81452012000300003'
            }
        ]
    }