SHELL := /bin/bash

NOTEBOOKS = $(wildcard [0-9][0-9]-[0-9]_*.ipynb)
NOTEBOOKS_tex = $(foreach I,$(NOTEBOOKS),tex/$(notdir $I).tex)

NOTEBOOKS_res = $(wildcard rešitve_[0-9][0-9]-[0-9]_*.ipynb)
NOTEBOOKS_res_tex = $(foreach I,$(NOTEBOOKS_res),tex/$(notdir $I).tex)

tex/%.ipynb.tex: %.ipynb
	mkdir -p $(@D)
	@echo "Izvajam zvezek $^"
	jupyter nbconvert --execute --ExecutePreprocessor.timeout=180 --allow-errors --to notebook $^ --inplace
	@echo "Pretvarjam v latex $^"
	jupyter nbconvert --to latex_with_lenvs --template thmsInNb_book --LenvsLatexExporter.removeHeaders=True $^ --output-dir tex --output $(notdir $^)

PR.pdf: tex/PR.tex tex/glava.tex $(NOTEBOOKS_tex) $(NOTEBOOKS_res_tex)
	cd tex && \
	xelatex -interaction=nonstopmode PR &> /dev/null | cat && \
    bibtex PR && \
	xelatex -interaction=nonstopmode PR &> /dev/null | cat && \
    mv PR.pdf ..

