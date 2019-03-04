import sys
import nbformat

fn = sys.argv[1]

with open(fn, 'rt') as fnb:
    notebook = nbformat.read(fnb, as_version=4)

notebook['metadata'].setdefault('nbTranslate', {})['displayLangs'] = ["sl"]

with open(fn, 'wt') as fnb:
    nbformat.write(notebook, fnb)

