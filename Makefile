SHELL := /bin/bash

.PHONY: paper clean check smoke pycheck citation-check placeholder-check

paper:
	cd paper && pdflatex -interaction=nonstopmode main.tex && (bibtex8 main || bibtex main) && pdflatex -interaction=nonstopmode main.tex && pdflatex -interaction=nonstopmode main.tex

clean:
	find paper -maxdepth 1 -type f \( -name '*.aux' -o -name '*.bbl' -o -name '*.blg' -o -name '*.log' -o -name '*.out' -o -name '*.toc' -o -name '*.lof' -o -name '*.lot' -o -name '*.fls' -o -name '*.fdb_latexmk' -o -name '*.synctex.gz' \) -delete
	rm -rf examples/smoke

pycheck:
	python -m py_compile scripts/*.py tests/*.py

placeholder-check:
	python scripts/check_placeholders.py paper/main.tex

citation-check:
	python scripts/check_citations.py paper/main.tex paper/references.bib

smoke:
	bash scripts/run_smoke_tests.sh

check: pycheck placeholder-check citation-check smoke
