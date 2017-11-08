SHELL := /bin/bash

NOTEBOOKS= $(wildcard [0-9][0-9]-*/*.ipynb)
NOTEBOOKS_tex = $(foreach I,$(NOTEBOOKS),tex/$(notdir $I).tex)

tex/%.ipynb.tex: */%.ipynb
	mkdir -p $(@D)
	@echo "Izvajam zvezek $^"
	jupyter nbconvert --execute --ExecutePreprocessor.timeout=180 --allow-errors --to notebook $^ --inplace
	@echo "Pretvarjam v latex $^"
	jupyter nbconvert --to latex_with_lenvs --LenvsLatexExporter.removeHeaders=True $^ --output-dir tex --output $(notdir $^)

PR.pdf: tex/PR.tex tex/glava.tex $(NOTEBOOKS_tex)
	cd tex && \
	xelatex -interaction=nonstopmode PR.tex &> /dev/null | cat && \
	xelatex -interaction=nonstopmode PR.tex &> /dev/null | cat && \
    mv PR.pdf ..

