all: build/main.pdf

plots: build/plot_charakteristik.pdf build/plot_strom.pdf
 
# hier Python-Skripte: 
build/plot_charakteristik.pdf: python/charakteristik.py data/Kennlinie.dat ../default/matplotlibrc ../default/header-matplotlib.tex | build
	python python/charakteristik.py
	python python/totzeit.py

build/plot_strom.pdf: python/strom.py data/Zaehlrohrstrom.dat ../default/matplotlibrc ../default/header-matplotlib.tex | build
	python python/strom.py

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
