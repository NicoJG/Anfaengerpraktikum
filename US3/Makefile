all: build/main.pdf

plots: build/plot_dopplerver.pdf
 
# hier Python-Skripte: 
build/plot_dopplerver.pdf: python/dopplerver.py data/*.csv ../default/matplotlibrc ../default/header-matplotlib.tex | build
	python python/dopplerver.py

# hier weitere Abhängigkeiten für build/main.pdf deklarieren:
build/main.pdf: plots

build/main.pdf: FORCE | build
	  TEXINPUTS=build: \
	  BIBINPUTS=build: \
	latexmk \
	  --lualatex \
	  --output-directory=build \
	  --interaction=nonstopmode \
	  --halt-on-error \
	main.tex

build:
	mkdir -p build

clean:
	rm -rf build

FORCE:

.PHONY: all clean plots
