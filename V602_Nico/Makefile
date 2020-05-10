all: build/main.pdf

plots: data/Vorbereitung_Ergebnis.csv build/plot_emission.pdf build/plot_bragg.pdf build/plot_Zink.pdf
 
# hier Python-Skripte: 
data/Vorbereitung_Ergebnis.csv: python/Vorbereitung.py data/Vorbereitung.csv
	python python/Vorbereitung.py

build/plot_emission.pdf: python/emission.py data/*.csv ../default/matplotlibrc ../default/header-matplotlib.tex | build
	python python/emission.py

build/plot_bragg.pdf: python/bragg.py data/*.csv ../default/matplotlibrc ../default/header-matplotlib.tex | build
	python python/bragg.py

build/plot_Zink.pdf: python/absorption.py data/*.csv ../default/matplotlibrc ../default/header-matplotlib.tex | build
	python python/absorption.py

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
