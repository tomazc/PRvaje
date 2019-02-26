Should follow this template w
Vprašanja in odgovori

##### Vprašanje X-Y-N

Besedilo

[Odgovor](rešitve_XX-Y_*.ipynb#odgovor-X-Y-N)


##### Odgovor X-Y-N


## Kazalo

* [1 - Priprava podatkov](01-1_podatki_numpy.ipynb)
* [2 - Prikazovanje podatkov](02-1_prikaz_matplotlib.ipynb)
* [3 - Porazdelitve in osamelci](03-1_porazdelitve.ipynb)
* [4 - Odkrivanje skupin](04-1_gručenje_voditelji.ipynb)
* [5 - Nadzorovano učenje](05-1_nadzorovano_linreg.ipynb)
* [6 - Nenegativna matrična faktorizacija in zlivanje podatkov](06-1_NMF.ipynb)
* [7 - Omrežja](07-1_omrežja_networkx.ipynb)
* [8 - Zaporedja](08-1_zaporedja_HMM.ipynb)


## Uporabne povezave
[Jupyter in binder](https://blog.jupyter.org/binder-2-0-a-tech-guide-2017-fd40515a3a84)


%config InlineBackend.figure_formats = ['jpeg']
get_ipython().display_formatter.formatters.pop('text/plain', None)


%config InlineBackend.figure_formats = ['jpeg']
import matplotlib
matplotlib.figure.Figure.__repr__ = lambda self: (
    f"<{self.__class__.__name__} size {self.bbox.size[0]:g}"
    f"x{self.bbox.size[1]:g} with {len(self.axes)} Axes>")

