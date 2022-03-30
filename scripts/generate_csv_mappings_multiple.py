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

#############
## Update Variables here
#############

csv_prj = "RAND"
csv_ns = "URL_Namespace_example"
provenance = csv_ns
file_csv = "/home/agar2/Documents/1Projects/7WorkProjects/NER/yake-tokens.csv"
col_num = 0                                     # Change to terms column number in csv file 
TARGET_ONTOLOGIES = ["AGRO", "ENVO", "PATO", "PO", 
                     "NCBITAXON", "CHEBI",      # large ontologies; comment out if not needed
                     "TO", "UO", "PECO", 
                    # TODO Issues: FOODON, GO
                    ]
#############

def create_csv_graph(file_csv, csv_ns, col_num=0) -> Graph:
    csv = pd.read_csv(file_csv, usecols=[col_num], header=None)
    csv_ns = csv_ns
    graph = Graph()
    graph.bind("rdfs-schema", RDFS)
    for index, entity in zip(range(0,len(csv)), csv):
        graph.add((Namespace.term(csv_ns, str(index)), 
                   RDFS.label, 
                   Literal(entity)))
    return graph

## Changed QUERY to multiline (variable update)
QUERY = (
f"{'SELECT distinct ?id ?label {'} \n"
    f"?term rdfs:label ?label . \n"
    f'FILTER (strStarts(str(?term), "{csv_ns}")) . \n'
    f'BIND(strafter(str(?term), "_") as ?id) \n'
f"{'}'}")

#############

def main():
    f"""Generate mappings from {csv_prj} to AGRO."""
    graph = create_csv_graph(file_csv, csv_ns, col_num)
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
