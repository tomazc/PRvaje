import sys
import nbformat

print(sys.argv)
fn = sys.argv[1]
lang = sys.argv[2]
print(fn, lang)

with open(fn, 'rt') as fnb:
    notebook = nbformat.read(fnb, as_version=4)

notebook['metadata'].setdefault('nbTranslate', {})['displayLangs'] = [lang]
notebook['metadata'].pop('celltoolbar', None)

with open(fn, 'wt') as fnb:
    nbformat.write(notebook, fnb)

