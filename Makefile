SHELL := /bin/bash

NOTEBOOKS = $(wildcard notebooks/[0-9][0-9][0-9]-*.ipynb)
NOTEBOOKS_tex-sl = $(foreach I,$(NOTEBOOKS),tex-sl/$(notdir $I).tex)
NOTEBOOKS_tex-en = $(foreach I,$(NOTEBOOKS),tex-en/$(notdir $I).tex)

all: pdf/PR.pdf pdf/DM.pdf

tex-sl/%.ipynb.tex: notebooks/%.ipynb
	mkdir -p $(@D)
	@echo "Izberem jezik sl v zvezku $^"
	jupyter nbconvert --to selectLanguage --NotebookLangExporter.language=sl $^ --output-dir tex-sl --output $(notdir $^)
	@echo "Izvajam zvezek $(addprefix tex-sl/, $(notdir $^))"
	jupyter nbconvert --execute --ExecutePreprocessor.timeout=360 --allow-errors --to notebook $(addprefix tex-sl/, $(notdir $^)) --inplace
	@echo "Pretvarjam v latex $^"
	jupyter nbconvert --to latex_with_lenvs --template mystyle.tplx --LenvsLatexExporter.removeHeaders=True $(addprefix tex-sl/, $(notdir $^)) --output-dir tex-sl --output $(notdir $^)
	sed -E 's/\\href{.+\.ipynb\\#(.+)}{/\\hyperref[\1]{/' "$@" > "tex-sl/tmp.$(notdir $^).tex"
	mv "tex-sl/tmp.$(notdir $^).tex" "$@"

tex-en/%.ipynb.tex: notebooks/%.ipynb
	mkdir -p $(@D)
	@echo "Izberem jezik en v zvezku $^"
	jupyter nbconvert --to selectLanguage --NotebookLangExporter.language=en $^ --output-dir tex-en --output $(notdir $^)
	@echo "Izvajam zvezek $(addprefix tex-en/, $(notdir $^))"
	jupyter nbconvert --execute --ExecutePreprocessor.timeout=360 --allow-errors --to notebook $(addprefix tex-en/, $(notdir $^)) --inplace
	@echo "Pretvarjam v latex $^"
	jupyter nbconvert --to latex_with_lenvs --template mystyle.tplx --LenvsLatexExporter.removeHeaders=True $(addprefix tex-en/, $(notdir $^)) --output-dir tex-en --output $(notdir $^)
	sed -E 's/\\href{.+\.ipynb\\#(.+)}{/\\hyperref[\1]{/' "$@" > "tex-en/tmp.$(notdir $^).tex"
	mv "tex-en/tmp.$(notdir $^).tex" "$@"

# sed is used to convert links:
# from: \href{rešitve_01-1_podatki_numpy.ipynb\#odgovor-1-1-1}{Odgovor}
# into: \hyperref[odgovor-1-1-1]{Odgovor}

tex-sl: $(NOTEBOOKS_tex-sl)
tex-en: $(NOTEBOOKS_tex-en)

fixlangs:
	for n in notebooks/*.ipynb; do \
		python fix_metadata.py $$n; \
	done

rerun:
	for n in notebooks/*.ipynb; do \
		jupyter nbconvert --execute --ExecutePreprocessor.timeout=360 --allow-errors --to notebook $$n --inplace; \
	done

900-lit.ipynb: notebooks/biblio.html
	jupyter nbconvert --execute --ExecutePreprocessor.timeout=360 --allow-errors --to notebook $^ --inplace

notebooks/biblio.html: notebooks/biblio.md notebooks/biblio.bib
	pandoc --filter=pandoc-citeproc --standalone notebooks/biblio.md -o notebooks/biblio.html

pdf/PR.pdf: notebooks/biblio.bib tex-sl/PR.tex tex-sl/glava.tex tex-sl
	rm -f pdf/PR.pdf && \
	rm -f tex-sl/PR.pdf && \
	cd tex-sl && \
	xelatex PR && \
	xelatex PR && \
	bibtex PR && \
	xelatex PR && \
	xelatex PR && \
	mv PR.pdf ../pdf/

pdf/DM.pdf: notebooks/biblio.bib tex-en/DM.tex tex-en/heading.tex tex-en
	rm -f pdf/DM.pdf && \
	rm -f tex-en/DM.pdf && \
	cd tex-en && \
	xelatex DM && \
	xelatex DM && \
	bibtex DM && \
	xelatex DM && \
	xelatex DM && \
	mv DM.pdf ../pdf/

pdfs: pdf/PR.pdf pdf/DM.pdf

clean:
	rm -f pdf/PR.pdf
	rm -f tex-sl/PR.pdf
	rm -f tex-sl/*.ipynb
	rm -Rf tex-sl/*.ipynb_files
	rm -f tex-sl/*.ipynb.tex
	rm -f tex-sl/PR.aux
	rm -f tex-sl/PR.bbl
	rm -f tex-sl/PR.blg
	rm -f tex-sl/PR.log
	rm -f tex-sl/PR.out
	rm -f tex-sl/PR.toc
 
	rm -f pdf/DM.pdf
	rm -f tex-en/DM.pdf
	rm -f tex-en/*.ipynb
	rm -Rf tex-en/*.ipynb_files
	rm -f tex-en/*.ipynb.tex
	rm -f tex-en/DM.aux
	rm -f tex-en/DM.bbl
	rm -f tex-en/DM.blg
	rm -f tex-en/DM.log
	rm -f tex-en/DM.out
	rm -f tex-en/DM.toc

