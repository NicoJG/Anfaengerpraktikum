all: build/main.pdf

plots: build/plot_verschiebung.pdf
 
# hier Python-Skripte: 
build/plot_verschiebung.pdf: python/verschiebung.py ../default/matplotlibrc ../default/header-matplotlib.tex | build
	python python/verschiebung.py

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
