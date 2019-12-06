all: build/main.pdf

plots:build/plot_frequenzentheorie.pdf build/plot_amplitudentheorie.pdf


# hier Python-Skripte: 
build/plot_frequenzentheorie.pdf: frequenzentheorie.py ../default/matplotlibrc ../default/header-matplotlib.tex | build
	  MATPLOTLIBRC="$$(dirname "$$(pwd)")/default/matplotlibrc" \
	  TEXINPUTS="$$(dirname "$$(pwd)")/default:" \
	python frequenzentheorie.py
build/plot_amplitudentheorie.pdf: amplitudentheorie.py ../default/matplotlibrc ../default/header-matplotlib.tex | build
	  MATPLOTLIBRC="$$(dirname "$$(pwd)")/default/matplotlibrc" \
	  TEXINPUTS="$$(dirname "$$(pwd)")/default:" \
	python amplitudentheorie.py	

# hier weitere Abhängigkeiten für build/main.pdf deklarieren:
build/main.pdf: build/plot_frequenzentheorie.pdf build/plot_amplitudentheorie.pdf

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
