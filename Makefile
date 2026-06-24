SHELL := /bin/bash

.PHONY: paper clean check smoke pycheck citation-check placeholder-check test experiment-01 experiment-01-quick experiment-01-dry-run

paper:
	@if [ -f paper/main.tex ]; then \
		cd paper && pdflatex -interaction=nonstopmode main.tex && (bibtex8 main || bibtex main) && pdflatex -interaction=nonstopmode main.tex && pdflatex -interaction=nonstopmode main.tex; \
	else \
		echo "paper/main.tex is not present in this repository checkout."; \
		echo "Add the manuscript source before running make paper, or use this repository as the code/reproducibility companion."; \
		exit 1; \
	fi

clean:
	find paper -maxdepth 1 -type f \( -name '*.aux' -o -name '*.bbl' -o -name '*.blg' -o -name '*.log' -o -name '*.out' -o -name '*.toc' -o -name '*.lof' -o -name '*.lot' -o -name '*.fls' -o -name '*.fdb_latexmk' -o -name '*.synctex.gz' \) -delete 2>/dev/null || true
	rm -rf examples/smoke

pycheck:
	python -m py_compile scripts/*.py tests/*.py

test:
	python tests/test_repository_smoke.py

placeholder-check:
	@if [ -f paper/main.tex ]; then \
		python scripts/check_placeholders.py paper/main.tex; \
	else \
		echo "Skipping placeholder check: paper/main.tex not present."; \
	fi

citation-check:
	@if [ -f paper/main.tex ] && [ -f paper/references.bib ]; then \
		python scripts/check_citations.py paper/main.tex paper/references.bib; \
	else \
		echo "Skipping citation check: paper/main.tex and paper/references.bib are not both present."; \
	fi

smoke:
	bash scripts/run_smoke_tests.sh

experiment-01-dry-run:
	python scripts/run_experiment_01_prediction_lift.py --config configs/experiment_01_prediction_lift.json --out results/experiment_01 --dry-run

experiment-01-quick:
	python scripts/run_experiment_01_prediction_lift.py --config configs/experiment_01_prediction_lift.json --out results/experiment_01_quick --quick

experiment-01:
	python scripts/run_experiment_01_prediction_lift.py --config configs/experiment_01_prediction_lift.json --out results/experiment_01

check: pycheck test placeholder-check citation-check smoke
