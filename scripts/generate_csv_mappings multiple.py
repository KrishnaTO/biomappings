# -*- coding: utf-8 -*-

"""Generate mappings from AGRO to AGROVOC."""

import time

from pyobo.gilda_utils import get_grounder
from tqdm import tqdm

from biomappings import PredictionTuple
from biomappings.resources import append_prediction_tuples
from biomappings.utils import get_script_url

from rdflib import Graph, Literal, Namespace
import pandas as pd
from rdflib.namespace import RDFS

def create_csv_graph(file_csv, csv_ns) -> Graph:
    csv = pd.read_csv(file_csv)
    csv_ns = csv_ns
    graph = Graph()
    graph.bind("rdfs-schema", RDFS)
    for index, entity in zip(range(0,len(csv)), csv.Entity):
        graph.add((Namespace.term(csv_ns, str(index)), 
                   RDFS.label, 
                   Literal(entity)))
    return graph

csv_prj = "ERA"
csv_ns = "https://era.ccafs.cgiar.org/ontology/ERA_"
provenance = csv_ns
file_csv = "/home/agar2/Documents/1Projects/7WorkProjects/2Projects/ERA/ttl-terms-export-v2.csv"
TARGET_ONTOLOGIES = ["AGRO", "ENVO", "NCBITAXON", 
                     "CHEBI", "PATO", "PO", 
                     "TO", "UO", "PECO"] 
                    # TODO Issues: FOODON, GO
QUERY = """
SELECT distinct ?id ?label {
    ?term rdfs:label ?label .
}
"""

def main():
    f"""Generate mappings from {csv_prj} to AGRO."""
    graph = create_csv_graph(file_csv, csv_ns)
    for ONT in TARGET_ONTOLOGIES:
        print(f"Getting predictions for {ONT}")
        grounder = get_grounder(ONT)
        rows = []
        for identifier, name in tqdm(graph.query(QUERY)):
            for scored_match in grounder.ground(name):
                rows.append(
                    PredictionTuple(
                        csv_prj,
                        identifier,
                        name,
                        "skos:exactMatch",
                        scored_match.term.db.lower(),
                        scored_match.term.id,
                        scored_match.term.entry_name,
                        "lexical",
                        scored_match.score,
                        provenance
                    )
                )
        append_prediction_tuples(rows)
    print("===Completed!===")


if __name__ == "__main__":
    main()
