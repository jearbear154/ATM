PANARGS := -V geometry:margin=.75in

MDS := $(wildcard *.md)
PDFS := $(MDS:.md=.pdf )

all: $(PDFS)

%.pdf: %.md
	pandoc $(PANARGS) -o $@ $<
