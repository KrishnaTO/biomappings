# -*- coding: utf-8 -*-

"""Generate mappings from AGRO to AGROVOC."""

import time

from pyobo.gilda_utils import get_grounder
from pyobo.sources.agrovoc import ensure_agrovoc_graph
from tqdm import tqdm

from biomappings import PredictionTuple
from biomappings.resources import append_prediction_tuples
from biomappings.utils import get_script_url

import csv

# AGROVOC_VERSION = "2021-12-02"
# QUERY = """
# SELECT distinct ?id ?label {
#     ?term skosxl:prefLabel / skosxl:literalForm ?label .
#     OPTIONAL { ?term skos:scopeNote ?description } .
#     FILTER (lang(?label) = 'en') .
#     FILTER (strStarts(str(?term), "http://aims.fao.org/aos/agrovoc/c_")) .
#     BIND(strafter(str(?term), "_") as ?id)
# }
# """
# # TODO include additional ns labels from agrovoc in QUERY, per list in ../agrovoc-ns.csv

def main():
    """Generate mappings from AGRO to AGROVOC."""
    provenance = get_script_url(__file__)
    grounder = get_grounder("AGRO")
    print("got grounder for AGRO", grounder)
    t = time.time()
    # graph = ensure_agrovoc_graph(AGROVOC_VERSION)

    # print(
    #     f"got RDF graph for AGROVOC {graph} with {len(graph)} triples in {time.time() - t:.2f} seconds"
    # )
    rows = []
    # sparql_write = open("agrovoc_sparql_query.csv", 'a+', newline='')
    # csvwriter = csv.writer(sparql_write)
    for identifier, name in tqdm(graph.query(QUERY)):

        # csvwriter.writerow([identifier, name])
        for scored_match in grounder.ground(name):
            rows.append(
                PredictionTuple(
                    # "agrovoc",
                    # identifier,
                    # name,
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


if __name__ == "__main__":
    main()
