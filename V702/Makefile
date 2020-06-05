all: build/main.pdf

plots: build/plot_Vanadium.pdf build/plot_Rhodium.pdf
 
# hier Python-Skripte: 
build/plot_Vanadium.pdf: python/Untergrund.py python/Vanadium.py data/*.csv ../default/matplotlibrc ../default/header-matplotlib.tex | build
	python python/Untergrund.py
	python python/Vanadium.py
build/plot_Rhodium.pdf: python/Untergrund.py python/Rhodium.py data/*.csv ../default/matplotlibrc ../default/header-matplotlib.tex | build
	python python/Rhodium.py

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
