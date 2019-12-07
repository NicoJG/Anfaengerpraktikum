all: build/main.pdf

plots: build/plot_einseitig_rund.pdf build/plot_einseitig_eckig.pdf build/plot_zweiseitig_eckig.pdf
 
# hier Python-Skripte: 
# für weitere Skripte, die einen Plot erstellen
# das Beispiel kopieren und NAME ersetzen
# Außerdem muss in plots und in build/main.pdf
# die jeweilige Abhängigkeit hinzugefügt werden
build/plot_einseitig_rund.pdf: python/einseitig_rund.py ../default/matplotlibrc ../default/header-matplotlib.tex data/*.csv | build
	  MATPLOTLIBRC="$$(dirname "$$(pwd)")/default/matplotlibrc" \
	  TEXINPUTS="$$(dirname "$$(pwd)")/default:" \
	python python/einseitig_rund.py

build/plot_einseitig_eckig.pdf: python/einseitig_eckig.py ../default/matplotlibrc ../default/header-matplotlib.tex data/*.csv | build
	  MATPLOTLIBRC="$$(dirname "$$(pwd)")/default/matplotlibrc" \
	  TEXINPUTS="$$(dirname "$$(pwd)")/default:" \
	python python/einseitig_eckig.py

build/plot_zweiseitig_eckig.pdf: python/zweiseitig_eckig.py ../default/matplotlibrc ../default/header-matplotlib.tex data/*.csv | build
	  MATPLOTLIBRC="$$(dirname "$$(pwd)")/default/matplotlibrc" \
	  TEXINPUTS="$$(dirname "$$(pwd)")/default:" \
	python python/zweiseitig_eckig.py
# hier weitere Abhängigkeiten für build/main.pdf deklarieren:
build/main.pdf: build/plot_einseitig_rund.pdf build/plot_einseitig_eckig.pdf build/plot_zweiseitig_eckig.pdf

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
