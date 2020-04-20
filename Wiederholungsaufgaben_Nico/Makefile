all: build/main.pdf

plots: #build/plot_regression.pdf
	python python/hohlzylinder.py
 
# hier Python-Skripte: 
# für weitere Skripte, die einen Plot erstellen
# das Beispiel kopieren und NAME ersetzen
# Außerdem muss in plots und in build/main.pdf
# die jeweilige Abhängigkeit hinzugefügt werden
build/plot_regression.pdf: python/regression.py ../default/matplotlibrc ../default/header-matplotlib.tex | build
	  MATPLOTLIBRC="$$(dirname "$$(pwd)")/default/matplotlibrc" \
	  TEXINPUTS="$$(dirname "$$(pwd)")/default:" \
	python python/regression.py

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
