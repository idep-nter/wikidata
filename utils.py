def get_stdforms(entity, data):
    result = {}

    def get_query(entity, language):
        q = f"""
                PREFIX rdf: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX wd: <http://www.wikidata.org/entity/>
                SELECT ?name
                WHERE {{ wd:{entity} rdfs:label ?name.
                    FILTER langMatches(LANG(?name), '{language}')
                }}
            """

        return q

    for r in data.query(get_query(entity, "cs")):
        result["cs"] = r["name"]

    for r in data.query(get_query(entity, "en")):
        result["en"] = r["name"]

    return result


def get_labels(entity, data):
    result = {}

    def get_query(entity, language):
        q = f"""
                PREFIX wd: <http://www.wikidata.org/entity/>
                PREFIX rdf: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX rdf: <http://www.w3.org/2004/02/skos/core#>
                PREFIX rdf: <http://schema.org/alternateName>
                SELECT ?name
                WHERE {{
                    {{ wd:{entity} rdf:label ?name. }}
                    UNION
                     {{ wd:{entity} rdf:altLabel ?name. }}
                    UNION
                    {{ wd:{entity} ?p ?name. }}
                    FILTER langMatches(LANG(?name), '{language}')
                }}
            """

        return q

    for r in data.query(get_query(entity, "cs")):
        name = r["name"]
        result.setdefault("cs", {}).setdefault(name, {}).setdefault("text", name)
        if len(name.split(" ")) == 1:
            result["cs"][name].setdefault("stability", -10)

    for r in data.query(get_query(entity, "en")):
        name = r["name"]
        result.setdefault("en", {}).setdefault(name, {}).setdefault("text", name)
        if len(name.split(" ")) == 1:
            result["en"][name].setdefault("stability", -10)

    return result


def get_descriptions(entity, data):
    result = {}

    def get_query(entity, language):
        q = f"""
                PREFIX wd: <http://www.wikidata.org/entity/>
                PREFIX rdf: <http://schema.org/description>
                SELECT ?description     
                WHERE {{ wd:{entity} ?p ?description.
                    FILTER langMatches(LANG(?description), '{language}')
                }}
            """

        return q

    for r in data.query(get_query(entity, "cs")):
        result["cs"] = r["description"]

    for r in data.query(get_query(entity, "en")):
        result["en"] = r["description"]

    return result


def get_ids(entity, data):
    result = {"wikidata": entity}
    q = f"""
            PREFIX wd: <http://www.wikidata.org/entity/>
            PREFIX rdf: <http://www.wikidata.org/prop/direct/>
            SELECT ?id     
            WHERE {{ wd:{entity} rdf:P646 ?id.
            }}
        """

    for r in data.query(q):
        result["freebase"] = r["id"]

    return result


def get_rankings(entity, data):
    q = f"""
               PREFIX wd: <http://www.wikidata.org/entity/>
               PREFIX rdf: <http://wikiba.se/ontology#>
               SELECT ?num    
               WHERE {{ wd:{entity} rdf:sitelinks ?num.
               }}
        """

    for r in data.query(q):
        return r["num"]


def get_type(entity, data):
    """
    Tries to get a type of an item based on class hierarchy in wikidata.

    *** DOESN'T WORK PROPERLY. ***
    """
    types = {
        "organization": "Q43229",
        "persons": "Q5",
        "location": "Q17334923",
        "product": "Q15401930",
        "event": "Q1656682",
    }
    q = f"""
            PREFIX wd: <http://www.wikidata.org/entity/>
            PREFIX rdf: <http://www.wikidata.org/prop/direct/>
            SELECT ?class
            WHERE {{ 
            {{ wd:{entity} rdf:P279 ?class. }}
            UNION 
            {{ wd:{entity} rdf:P31 ?class. }}
            }}
        """

    for r in data.query(q):
        for k, v in types.items():
            v = f"http://www.wikidata.org/entity/{v}"
            if str(r["class"]) == v:
                return k

        return "general"
