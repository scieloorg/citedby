# CitedBy

The API is generally RESTFUL and returns results in JSON.

The API will only work for:

* SciELO PID(SciELO Publisher Identifier)
* DOI
* Some meta data: title, first_author and publisher_year

Example:

http://citedby.scielo.org/api/v1/pid/?q=S0124-41082008000200002

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


List of endpoints:

| resource      | description                       |
|:--------------|:----------------------------------|
| `/pid/?q=PID`      | return article and your citations like the above example |
| `/doi/?q=DOI`    | get the article meta from crossref and search the citations in citedby, its  returns the same above struture |
| `/meta/?title=TITLE&author=AUTHOR&year=YEAR` | get the article by title, author and year and return the same above metadada(article and your received citations) |



## Version history

* V1 2015-03-02, first stable version
