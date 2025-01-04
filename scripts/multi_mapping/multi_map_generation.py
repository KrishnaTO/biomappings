# Generate biomappings for list of ontologies


### 1) 1 file compared with many ontologies
### 2) many ontologies compared with many ontologies

#---Original list (working)
#TARGET_ONTOLOGIES = ["AGRO", "ENVO", "NCBITAXON", "CHEBI", "PATO", "PO", "TO", "UO", "PECO", 'iobc', 'sweet', 'bero', 'ecso', 'cob', 'pto'] # TODO Issues: FOODON, GO

from combo_search_list import search_list

core_ontologies = [ 'envo', 'chebi', 'ncbitaxon'] # 'agrovoc',
pop_ontologies = ['iobc', 'sweet', 'bero', 'pato', 'po', 'ecso', 'cob', 'agro', 'pto', 'peco']
TARGET_ONTOLOGIES = search_list(core_ontologies, pop_ontologies, all = True)

import generate_mappings_multiple 
for ONT in TARGET_ONTOLOGIES:
    generate_mappings_multiple.main(ONT)