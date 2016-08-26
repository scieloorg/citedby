CitedBy
=======

API RESTFul to retrieve citations received from SciELO articles to a given DOI, Article Title or SciELO ID.

Usage documentation are available at: [SciELO CitedBy RESTFul API](http://docs.scielo.org/projects/citedby/en/latest/)


Build Status
============

.. image:: https://travis-ci.org/scieloorg/citedby.svg?branch=master
    :target: https://travis-ci.org/scieloorg/citedby

Docker Status
=============


.. image:: https://images.microbadger.com/badges/image/scieloorg/citedby.svg
    :target: https://hub.docker.com/r/scieloorg/citedby

Como Instalar e subir os serviços
=================================

Source
------

Ter ambiente virtual criado e inicializado.

block-code::

    git clone https://github.com/scieloorg/citedby.git
    cd citedby
    python setup.py install 
    pserver config.ini

Docker
------

block-code::

    docker pull scieloorg/citedby
    docker run --name citedby -e ELASTSEARCH_HOST=esd.scielo.org:9200 -p 6545:8000 -p 11622:11620 -d scieloorg/citedby
