all: build/main.pdf

# klappt leider nicht: MATPLOTLIBRC="$$(dirname "$$(pwd)")/default/matplotlibrc":
# hier Python-Skripte: 
build/plot.pdf: plot.py matplotlibrc ../default/header-matplotlib.tex | build
	  TEXINPUTS="$$(dirname "$$(pwd)")/default": \
	python plot.py

# hier weitere Abhängigkeiten für build/main.pdf deklarieren:
build/main.pdf: build/plot.pdf

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

.PHONY: all clean
