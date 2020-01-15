all: build/main.pdf

plots: build/plot_hysterese.pdf build/plot_kupfer_Ib.pdf build/plot_kupfer_Iq.pdf build/plot_silber_Ib.pdf build/plot_silber_Iq.pdf build/plot_zink_Ib.pdf build/plot_zink_Iq.pdf
 
# hier Python-Skripte: 
# für weitere Skripte, die einen Plot erstellen
# das Beispiel kopieren und NAME ersetzen
# Außerdem muss in plots und in build/main.pdf
# die jeweilige Abhängigkeit hinzugefügt werden
build/plot_hysterese.pdf: python/hysterese.py data/*.csv ../default/matplotlibrc ../default/header-matplotlib.tex | build
	  MATPLOTLIBRC="$$(dirname "$$(pwd)")/default/matplotlibrc" \
	  TEXINPUTS="$$(dirname "$$(pwd)")/default:" \
	python python/hysterese.py

build/plot_kupfer_Ib.pdf: python/kupfer_Ib.py data/*.csv ../default/matplotlibrc ../default/header-matplotlib.tex | build
	  MATPLOTLIBRC="$$(dirname "$$(pwd)")/default/matplotlibrc" \
	  TEXINPUTS="$$(dirname "$$(pwd)")/default:" \
	python python/kupfer_Ib.py

build/plot_kupfer_Iq.pdf: python/kupfer_Iq.py data/*.csv ../default/matplotlibrc ../default/header-matplotlib.tex | build
	  MATPLOTLIBRC="$$(dirname "$$(pwd)")/default/matplotlibrc" \
	  TEXINPUTS="$$(dirname "$$(pwd)")/default:" \
	python python/kupfer_Iq.py

build/plot_silber_Iq.pdf: python/silber_Iq.py data/*.csv ../default/matplotlibrc ../default/header-matplotlib.tex | build
	  MATPLOTLIBRC="$$(dirname "$$(pwd)")/default/matplotlibrc" \
	  TEXINPUTS="$$(dirname "$$(pwd)")/default:" \
	python python/silber_Iq.py

build/plot_silber_Ib.pdf: python/silber_Ib.py data/*.csv ../default/matplotlibrc ../default/header-matplotlib.tex | build
	  MATPLOTLIBRC="$$(dirname "$$(pwd)")/default/matplotlibrc" \
	  TEXINPUTS="$$(dirname "$$(pwd)")/default:" \
	python python/silber_Ib.py

build/plot_zink_Ib.pdf: python/zink_Ib.py data/*.csv ../default/matplotlibrc ../default/header-matplotlib.tex | build
	  MATPLOTLIBRC="$$(dirname "$$(pwd)")/default/matplotlibrc" \
	  TEXINPUTS="$$(dirname "$$(pwd)")/default:" \
	python python/zink_Ib.py

build/plot_zink_Iq.pdf: python/zink_Iq.py data/*.csv ../default/matplotlibrc ../default/header-matplotlib.tex | build
	  MATPLOTLIBRC="$$(dirname "$$(pwd)")/default/matplotlibrc" \
	  TEXINPUTS="$$(dirname "$$(pwd)")/default:" \
	python python/zink_Iq.py
# hier weitere Abhängigkeiten für build/main.pdf deklarieren:
build/main.pdf: build/plot_hysterese.pdf build/plot_kupfer_Ib.pdf build/plot_kupfer_Iq.pdf build/plot_silber_Ib.pdf build/plot_silber_Iq.pdf build/plot_zink_Ib.pdf build/plot_zink_Iq.pdf

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
