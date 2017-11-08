__author__ = 'martin'
from Bio import Entrez
from Bio import SeqIO
import json

species = [
    ("Homo sapiens",            "NC_012920.1"),
    ("Pan troglodytes",         "NC_001643.1"),
    ("Equus caballus",          "NC_001640.1"),
    ("Chamaeleo calyptratus",   "NC_012420.1"),
    ("Delphinus capensis",      "NC_012061.1"),
    ("Takifugu rubripes",       "NC_004299.1"),
    ("Canis lupus familiaris",  "NC_002008.4"),
    ("Gorilla gorilla",         "NC_001645.1"),
    ("Pongo abelii",            "NC_002083.1"),
    ("Sus scrofa",              "NC_000845.1"),
    ("Daboia russellii",        "NC_011391.1"),
    ("Carassius auratus auratus", "NC_006580.1"),
    ("Rattus norvegicus",       "AC_000022.2"),
    ("Homo sapiens neanderthalensis", "NC_011137.1"),
]

# Data loading
infile = "seqs.json"
seqs = dict()
for name, sid in species:
    print "Loading ...", name
    t = False
    while not t:
        try:
            handle = Entrez.efetch(db="nucleotide", rettype="gb", id=sid,
                           email="a@gmail.com")
            rec = SeqIO.read(handle, "gb")
            handle.close()
            t = True
        except:
            continue
    seqs[name] = str(rec.seq)   

json.dump(seqs, open(infile, "w"))
