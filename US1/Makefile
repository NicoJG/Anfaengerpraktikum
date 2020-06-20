all: build/main.pdf

plots: build/plot_Durchschallung.pdf build/plot_Impulsecho.pdf
 
# hier Python-Skripte: 
build/plot_Durchschallung.pdf: python/Durchschallung.py data/*.csv ../default/matplotlibrc ../default/header-matplotlib.tex | build
	python python/Durchschallung.py

build/plot_Impulsecho.pdf: python/Impulsecho.py data/*.csv ../default/matplotlibrc ../default/header-matplotlib.tex | build
	python python/Impulsecho.py
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
