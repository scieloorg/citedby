# CitedBy

API RESTFul to retrieve citations from SciELO articles to a given DOI, Article Title or SciELO ID, this is RESTFUL and returns results in JSON.

Usage documentation are available on-line: [SciELO CitedBy RESTful API](http://docs.scielo.org/projects/citedby/en/latest/)


The API will only work for:

* SciELO ID colled PID(Publisher Identifier)
* DOI (Digital Object Identifier) - `http://www.doi.org/`
* And some article meta data: title, first_author and publisher_year

Example:

`http://citedby.scielo.org/api/v1/pid/?q=S0124-41082008000200002`

Will return the following result:

    {
        article: {
        code: "S0124-41082008000200002",
        first_author: {
            surname: "Velásquez Rodríguez"
        },
        issn: "0124-4108",
        publication_year: "2008",
        source: "Perspectivas en Nutrición Humana",
        titles: [
            "Inflammatory response in children with severe acute malnutrition and anemia",
            "Respuesta inflamatoria en niños con desnutrición aguda grave y anemia"
        ],
        collection: "col",
        url: "http://www.scielo.org.co/scielo.php?script=sci_arttext&pid=S0124-41082008000200002&lng=en&tlng=en"
        },
        cited_by: [
            {
                url: "http://www.scielo.org.co/scielo.php?script=sci_arttext&pid=S0124-41082010000200002&lng=en&tlng=en",
                source: "Perspectivas en Nutrición Humana",
                issn: "0124-4108",
                titles: [
                    "Effects of all-trans retinoic acid on the production of cytokines by peripheral blood mononuclear cells (PBMC) in children with acute malnutrition",
                    "Efecto del all-trans ácido retinoico en la producción de citocinas por células mononucleares de sangre periférica (CMSP) en niños con desnutrición aguda"
                ],
                code: "S0124-41082010000200002"
            }
        ]
    }


##List of endpoints:

| resource      | description                       |
|:--------------|:----------------------------------|
| `/pid/?q=PID`      | return article and your citations like the above example |
| `/doi/?q=DOI`    | get the article meta from crossref and search the citations in citedby, its returns the same above struture |
| `/meta/?title=TITLE&author=AUTHOR&year=YEAR` | get the article by title, author and year and return the same above metadada(article and your received citations) |

##Parameters

Parameters can be used to query, filter and control the results returned by the SciELO API. This param can be passed in URI parameters.

Yet we have just the param `metaonly` return just the article metadata.

Look the same above example with the `metaonly` param:

  `http://citedby.scielo.org/api/v1/pid/?q=S0124-41082008000200002&metaonly=true`

    {
        article: {
        code: "S0124-41082008000200002",
        first_author: {
            surname: "Velásquez Rodríguez"
        },
        issn: "0124-4108",
        publication_year: "2008",
        source: "Perspectivas en Nutrición Humana",
        titles: [
            "Inflammatory response in children with severe acute malnutrition and anemia",
            "Respuesta inflamatoria en niños con desnutrición aguda grave y anemia"
        ],
        collection: "col",
        url: "http://www.scielo.org.co/scielo.php?script=sci_arttext&pid=S0124-41082008000200002&lng=en&tlng=en",
        total_cited_by: 1
        }
    }


## Version history

* V1.0 2015-03-02, first stable version https://github.com/scieloorg/citedby/releases/tag/stable-v1.0
