SHELL := /bin/bash

NOTEBOOKS = $(wildcard [0-9][0-9]-[0-9]_*.ipynb)
NOTEBOOKS_web-sl = $(foreach I,$(NOTEBOOKS),web-sl/$(notdir $I))
NOTEBOOKS_web-en = $(foreach I,$(NOTEBOOKS),web-en/$(notdir $I))
NOTEBOOKS_tex-sl = $(foreach I,$(NOTEBOOKS),tex-sl/$(notdir $I).tex)
NOTEBOOKS_tex-en = $(foreach I,$(NOTEBOOKS),tex-en/$(notdir $I).tex)

NOTEBOOKS_res = $(wildcard resitve_[0-9][0-9]-[0-9]_*.ipynb)
NOTEBOOKS_res_web-sl = $(foreach I,$(NOTEBOOKS_res),web-sl/$(notdir $I))
NOTEBOOKS_res_web-en = $(foreach I,$(NOTEBOOKS_res),web-en/$(notdir $I))
NOTEBOOKS_res_tex-sl = $(foreach I,$(NOTEBOOKS_res),tex-sl/$(notdir $I).tex)
NOTEBOOKS_res_tex-en = $(foreach I,$(NOTEBOOKS_res),tex-en/$(notdir $I).tex)

NOTEBOOKS_nal = $(wildcard n[0-9]_*.ipynb)
NOTEBOOKS_nal_web-sl = $(foreach I,$(NOTEBOOKS_nal),web-sl/$(notdir $I))
NOTEBOOKS_nal_web-en = $(foreach I,$(NOTEBOOKS_nal),web-en/$(notdir $I))
NOTEBOOKS_nal_tex-sl = $(foreach I,$(NOTEBOOKS_nal),tex-sl/$(notdir $I).tex)
NOTEBOOKS_nal_tex-en = $(foreach I,$(NOTEBOOKS_nal),tex-en/$(notdir $I).tex)

tex-sl/%.ipynb.tex: web-sl/%.ipynb
	mkdir -p $(@D)
	@echo "Izvajam zvezek $^"
	jupyter nbconvert --execute --ExecutePreprocessor.timeout=360 --allow-errors --to notebook $^ --inplace
	@echo "Pretvarjam v latex $^"
	jupyter nbconvert --to latex_with_lenvs --template mystyle.tplx --LenvsLatexExporter.removeHeaders=True $^ --output-dir tex-sl --output $(notdir $^)
	sed -E 's/\\href{.+\.ipynb\\#(.+)}{/\\hyperref[\1]{/' "$@" > "tex-sl/tmp.$(notdir $^).tex"
	mv "tex-sl/tmp.$(notdir $^).tex" "$@"

tex-en/%.ipynb.tex: web-en/%.ipynb
	mkdir -p $(@D)
	@echo "Izvajam zvezek $^"
	jupyter nbconvert --execute --ExecutePreprocessor.timeout=360 --allow-errors --to notebook $^ --inplace
	@echo "Pretvarjam v latex $^"
	jupyter nbconvert --to latex_with_lenvs --template mystyle.tplx --LenvsLatexExporter.removeHeaders=True $^ --output-dir tex-en --output $(notdir $^)
	sed -E 's/\\href{.+\.ipynb\\#(.+)}{/\\hyperref[\1]{/' "$@" > "tex-en/tmp.$(notdir $^).tex"
	mv "tex-en/tmp.$(notdir $^).tex" "$@"

# sed is used to convert links:
# from: \href{rešitve_01-1_podatki_numpy.ipynb\#odgovor-1-1-1}{Odgovor}
# into: \hyperref[odgovor-1-1-1]{Odgovor}

web-sl/%.ipynb: %.ipynb
	mkdir -p $(@D)
	@echo "Izberem jezik sl v zvezku $^"
	jupyter nbconvert --to selectLanguage --NotebookLangExporter.language=sl $^ --output-dir web-sl --output $(notdir $^)
	@echo "Izvajam zvezek $(addprefix web-sl/, $(notdir $^))"
	jupyter nbconvert --execute --ExecutePreprocessor.timeout=360 --allow-errors --to notebook $(addprefix web-sl/, $(notdir $^)) --inplace

web-en/%.ipynb: %.ipynb
	mkdir -p $(@D)
	@echo "Izberem jezik en v zvezku $^"
	jupyter nbconvert --to selectLanguage --NotebookLangExporter.language=en $^ --output-dir web-en --output $(notdir $^)
	@echo "Izvajam zvezek $(addprefix web-en/, $(notdir $^))"
	jupyter nbconvert --execute --ExecutePreprocessor.timeout=360 --allow-errors --to notebook $(addprefix web-en/, $(notdir $^)) --inplace

web-sl: $(NOTEBOOKS_web-sl) $(NOTEBOOKS_res_web-sl) $(NOTEBOOKS_nal_web-sl)
web-en: $(NOTEBOOKS_web-en) $(NOTEBOOKS_res_web-en) $(NOTEBOOKS_nal_web-en)
tex-sl: $(NOTEBOOKS_tex-sl) $(NOTEBOOKS_res_tex-sl) $(NOTEBOOKS_nal_tex-sl)
tex-en: $(NOTEBOOKS_tex-en) $(NOTEBOOKS_res_tex-en) $(NOTEBOOKS_nal_tex-en)

rerun:
	for n in *.ipynb; do \
		jupyter nbconvert --execute --ExecutePreprocessor.timeout=360 --allow-errors --to notebook $$n --inplace; \
	done

09-1_literatura.ipynb: biblio.html
	jupyter nbconvert --execute --ExecutePreprocessor.timeout=360 --allow-errors --to notebook 09-1_literatura.ipynb --inplace

biblio.html: biblio.md biblio.bib
	pandoc --filter=pandoc-citeproc --standalone biblio.md -o biblio.html

pdf/PR.pdf: biblio.bib tex-sl/PR.tex tex-sl/glava.tex web-sl tex-sl
	rm -f pdf/PR.pdf && \
	rm -f tex-sl/PR.pdf && \
	cd tex-sl && \
	xelatex PR && \
	xelatex PR && \
	bibtex PR && \
	xelatex PR && \
	xelatex PR && \
	mv PR.pdf ../pdf/

pdf/DM.pdf: biblio.bib tex-en/DM.tex tex-en/heading.tex web-en tex-en
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

all: rerun pdf/PR.pdf pdf/DM.pdf

clean:
	rm -f pdf/PR.pdf
	rm -f tex-sl/PR.pdf
	rm -f web-sl/*.ipynb
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
	rm -f web-en/*.ipynb
	rm -Rf tex-en/*.ipynb_files
	rm -f tex-en/*.ipynb.tex
	rm -f tex-en/DM.aux
	rm -f tex-en/DM.bbl
	rm -f tex-en/DM.blg
	rm -f tex-en/DM.log
	rm -f tex-en/DM.out
	rm -f tex-en/DM.toc

# xelatex -interaction=nonstopmode PR &> /dev/null | cat && \

