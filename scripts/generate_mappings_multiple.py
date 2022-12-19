
### 1) 1 file compared with many ontologies
### 2) many ontologies compared with many ontologies



from tqdm import tqdm
from pyobo.gilda_utils import get_grounder
from biomappings import PredictionTuple
from biomappings.resources import append_prediction_tuples
from rdflib.namespace import _RDFS, _SKOS, _OWL, _XSD, _DCTERMS
from rdflib import Graph

from os.path import exists

__all__ = [
    "ensure_graph",   
]

# Use bioregistry to get the ontology URL and abbreviation
ONT_URL_PATH = "http://purl.obolibrary.org/obo/doid.owl"
ONT_ABR = "doid"

TARGET_ONTOLOGIES = ["AGRO", "ENVO", "NCBITAXON", "CHEBI", "PATO", "PO", "TO", "UO", "PECO"] # TODO Issues: FOODON, GO


def choose_fmt(string):
    strsplit = string.split(".")[-1]
    if strsplit == "ttl":
        return "turtle"
    if strsplit == "rdf" or strsplit == "owl":
        return "xml"
    if strsplit == "nt":
        return "nt"
    if strsplit == "n3":
        return "n3"
    if strsplit == "jsonld":
        return "json-ld"

ONT_FORMAT = choose_fmt(ONT_URL_PATH)

def ensure_graph() -> Graph:  
    g = Graph()
    g.parse(ONT_URL_PATH, format= ONT_FORMAT)
    g.bind("skos", _SKOS)
    g.bind("dcterms", _DCTERMS)
    g.bind("rdfs-schema", _RDFS)
    g.bind("owl", _OWL)
    g.bind("xsd", _XSD)
    g.bind(ONT_ABR, ONT_URL_PATH)
    return g
g = ensure_graph() 

QUERY = """
SELECT distinct ?id ?label {
    ?term rdfs:label ?label .
    OPTIONAL { ?term skos:scopeNote ?description } .
    FILTER (strStarts(str(?term), \"""" + ONT_URL_PATH + """\")) .
    BIND(strafter(str(?term), "_") as ?id)
}
"""

def main():
    for ONT in TARGET_ONTOLOGIES:
        grounder = get_grounder(ONT)
        print(f"Getting predictions for {ONT}")
        provenance = ONT_URL_PATH
        rows = []
        for identifier, name in tqdm(g.query(QUERY)):
            for scored_match in grounder.ground(name):
                rows.append(
                    PredictionTuple(
                        ONT_ABR,
                        identifier,
                        name,
                        "skos:exactMatch",
                        scored_match.term.db.lower(),
                        scored_match.term.id,
                        scored_match.term.entry_name,
                        "lexical",
                        scored_match.score,
                        provenance,
                    )
                )
        append_prediction_tuples(rows)
    print("===Completed!===")

if __name__ == "__main__":
    main()
