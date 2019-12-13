all: build/main.pdf

plots: build/plot_winkelrichtgroesse.pdf build/plot_eigentraegheit.pdf brauner_zylinder weisser_zylinder
 
# hier Python-Skripte: 
# für weitere Skripte, die einen Plot erstellen
# das Beispiel kopieren und NAME ersetzen
# Außerdem muss in plots und in build/main.pdf
# die jeweilige Abhängigkeit hinzugefügt werden
build/plot_winkelrichtgroesse.pdf: python/winkelrichtgroesse.py data/*.csv ../default/matplotlibrc ../default/header-matplotlib.tex | build
	  MATPLOTLIBRC="$$(dirname "$$(pwd)")/default/matplotlibrc" \
	  TEXINPUTS="$$(dirname "$$(pwd)")/default:" \
	python python/winkelrichtgroesse.py

build/plot_eigentraegheit.pdf: build/plot_winkelrichtgroesse.pdf python/eigentraegheit.py data/*.csv ../default/matplotlibrc ../default/header-matplotlib.tex | build
	  MATPLOTLIBRC="$$(dirname "$$(pwd)")/default/matplotlibrc" \
	  TEXINPUTS="$$(dirname "$$(pwd)")/default:" \
	python python/eigentraegheit.py

# Python Dateien ohne Plots
brauner_zylinder: build/plot_eigentraegheit.pdf build/plot_winkelrichtgroesse.pdf python/brauner_zylinder.py data/*.csv
	python python/brauner_zylinder.py

weisser_zylinder: build/plot_eigentraegheit.pdf build/plot_winkelrichtgroesse.pdf python/weisser_zylinder.py data/*.csv
	python python/weisser_zylinder.py

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
