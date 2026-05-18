# Paper Build Instructions

Canonical source: `main.tex`  
Bibliography: `references.bib`

## Build with Make

From repository root:

```bash
make paper
```

## Build manually

```bash
cd paper
pdflatex -interaction=nonstopmode main.tex
bibtex8 main || bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

## Overleaf

Upload these files to Overleaf:

- `main.tex`
- `references.bib`

Set the compiler to pdfLaTeX and bibliography tool to BibTeX.

## Figures

Most figures are currently TikZ diagrams embedded directly in `main.tex`. The `figures/` directory is reserved for future external diagrams if the paper is later redesigned for a journal template.
