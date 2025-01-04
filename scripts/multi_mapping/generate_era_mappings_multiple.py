from tqdm import tqdm
from pyobo.gilda_utils import get_grounder
from biomappings import PredictionTuple
from biomappings.resources import append_prediction_tuples
from rdflib.namespace import RDFS, SKOS, OWL, XSD, DCTERMS
from rdflib import Graph


__all__ = [
    "ensure_era_graph",
]

def ensure_era_graph() -> Graph:
    g = Graph()
    g.parse("./ERA/era_kos.ttl", format='turtle')
    g.bind("skos", SKOS)
    g.bind("dcterms", DCTERMS)
    g.bind("rdfs-schema", RDFS)
    g.bind("owl", OWL)
    g.bind("xsd", XSD)
    g.bind("era", "https://era.ccafs.cgiar.org/ontology/")
    return g

g = ensure_era_graph()


QUERY = """
SELECT distinct ?id ?label {
    ?term rdfs:label ?label .
    OPTIONAL { ?term skos:scopeNote ?description } .
    FILTER (strStarts(str(?term), "https://era.ccafs.cgiar.org/ontology/")) .
    BIND(strafter(str(?term), "_") as ?id)
}
"""

def main():
    TARGET_ONTOLOGIES = ["AGRO", "ENVO", "NCBITAXON", "CHEBI", "PATO", "PO", "TO", "UO", "PECO"] # TODO Issues: FOODON, GO
    for ONT in TARGET_ONTOLOGIES:
        grounder = get_grounder(ONT)
        print(f"Getting predictions for {ONT}")
        provenance = "https://era.ccafs.cgiar.org/ontology/"
        rows = []
        for identifier, name in tqdm(g.query(QUERY)):
            for scored_match in grounder.ground(name):
                rows.append(
                    PredictionTuple(
                        "era",
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
