SHELL := /bin/bash

NOTEBOOKS = $(wildcard [0-9][0-9]-[0-9]_*.ipynb)
NOTEBOOKS_tex = $(foreach I,$(NOTEBOOKS),tex/$(notdir $I).tex)

NOTEBOOKS_res = $(wildcard rešitve_[0-9][0-9]-[0-9]_*.ipynb)
NOTEBOOKS_res_tex = $(foreach I,$(NOTEBOOKS_res),tex/$(notdir $I).tex)

NOTEBOOKS_nal = $(wildcard naloge/*.ipynb)
NOTEBOOKS_nal_tex = $(foreach I,$(NOTEBOOKS_nal),tex/$(notdir $I).tex)

tex/%.ipynb.tex: %.ipynb
	mkdir -p $(@D)
	@echo "Izvajam zvezek $^"
	jupyter nbconvert --execute --ExecutePreprocessor.timeout=180 --allow-errors --to notebook $^ --inplace
	@echo "Pretvarjam v latex $^"
	jupyter nbconvert --to latex_with_lenvs --template mystyle.tplx --LenvsLatexExporter.removeHeaders=True $^ --output-dir tex --output $(notdir $^)
	sed -E 's/\\href{.+\.ipynb\\#(.+)}{/\\hyperref[\1]{/' "$@" > tex/tmp.tex
	mv tex/tmp.tex "$@"

# sed is used to convert links:
# from: \href{rešitve_01-1_podatki_numpy.ipynb\#odgovor-1-1-1}{Odgovor}
# into: \hyperref[odgovor-1-1-1]{Odgovor}


tex/%.ipynb.tex: naloge/%.ipynb
	mkdir -p $(@D)
	@echo "Izvajam zvezek $^"
	jupyter nbconvert --execute --ExecutePreprocessor.timeout=180 --allow-errors --to notebook $^ --inplace
	@echo "Pretvarjam v latex $^"
	jupyter nbconvert --to latex_with_lenvs --template mystyle.tplx --LenvsLatexExporter.removeHeaders=True $^ --output-dir tex --output $(notdir $^)
	sed -E 's/\\href{.+\.ipynb\\#(.+)}{/\\hyperref[\1]{/' "$@" > tex/tmp.tex
	mv tex/tmp.tex "$@"


all: PR.pdf


09-1_literatura.ipynb: biblio.bib
	jupyter nbconvert --execute --ExecutePreprocessor.timeout=180 --allow-errors --to notebook 09-1_literatura.ipynb --inplace


biblio.html: biblio.md biblio.bib 09-1_literatura.ipynb
	pandoc --filter=pandoc-citeproc --standalone biblio.md -o biblio.html


PR.pdf: biblio.bib tex/PR.tex tex/glava.tex $(NOTEBOOKS_tex) $(NOTEBOOKS_res_tex) $(NOTEBOOKS_nal_tex)
	rm -f PR.pdf && \
	rm -f tex/PR.pdf && \
	cd tex && \
	xelatex PR && \
	xelatex PR && \
	bibtex PR && \
	xelatex PR && \
	xelatex PR && \
	mv PR.pdf ..


clean:
	rm -f tex/*.ipynb.tex
	rm -Rf tex/*.ipynb_files
	rm -f tex/PR.pdf
	rm -f PR.pdf
# xelatex -interaction=nonstopmode PR &> /dev/null | cat && \

