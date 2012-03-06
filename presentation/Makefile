# Makefile for latex

LATEX     = pdflatex
BIBTEX    = bibtex
MAKEINDEX = makeindex
XPDF      =xpdf 

RERUN = "(There were undefined references|Rerun to get (cross-references|the bars) right)"
RERUNBIB = "No file.*\.bbl|Citation.*undefined"
MAKEIDX = "^[^%]*\\makeindex"
MPRINT = "^[^%]*print"
USETHUMBS = "^[^%]*thumbpdf"

DATE=$(shell date +%Y-%m-%d)

COPY = if test -r $(<:%.tex=%.toc); then cp $(<:%.tex=%.toc) $(<:%.tex=%.toc.bak); fi
RM = rm -f
OUTDATED = echo "EPS-file is out-of-date!" && false

SRC := presentation.tex
TRG  = $(SRC:%.tex=%.dvi)
PSF  = $(SRC:%.tex=%.ps)
PDF  = $(SRC:%.tex=%.pdf)

define run-latex
  $(COPY);$(LATEX) $<
  egrep $(MAKEIDX) $< && ($(MAKEINDEX) $(<:%.tex=%);$(COPY);$(LATEX) $<) >/dev/null; true
  egrep -c $(RERUNBIB) $(<:%.tex=%.log) && ($(BIBTEX) $(<:%.tex=%);$(COPY);$(LATEX) $<) ; true
  egrep $(RERUN) $(<:%.tex=%.log) && ($(COPY);$(LATEX) $<) >/dev/null; true
  egrep $(RERUN) $(<:%.tex=%.log) && ($(COPY);$(LATEX) $<) >/dev/null; true
  if cmp -s $(<:%.tex=%.toc) $(<:%.tex=%.toc.bak); then true ;else $(LATEX) $< ; fi
  $(RM) $(<:%.tex=%.toc.bak)
  # Display relevant warnings
  egrep -i "(Reference|Citation).*undefined" $(<:%.tex=%.log) ; true
endef

define get_dependencies
  deps=`perl -ne '($$_)=/^[^%]*\\\(?:include|input)\{(.*?)\}/;@_=split /,/;foreach $$t (@_) {print "$$t.tex "}' $<`
endef

define getbibs
  bibs=`perl -ne '($$_)=/^[^%]*\\\bibliography\{(.*?)\}/;@_=split /,/;foreach $$b (@_) {print "$$b.bib "}' $< $$deps`
endef

define geteps
  epses=`perl -ne '@foo=/^[^%]*\\\(includegraphics|psfig)(\[.*?\])?\{(.*?)\}/g;if (defined($$foo[2])) { if ($$foo[2] =~ /.eps$$/) { print "$$foo[2] "; } else { print "$$foo[2].eps "; }}' $< $$deps`
endef

define manconf
  mandeps=`if test -r $(basename $@).cnf ; then cat $(basename $@).cnf |tr -d '\n\r' ; fi`
endef

all: $(PDF)

.PHONY: all show clean pdf

clean:
	-rm -f *.log *.aux *.dvi *.bbl *.blg *.ilg *.toc *.lof *.lot *.idx *.ind *.~ presentation.pdf

$(PDF): %.pdf : %.tex
	@$(run-latex)

show: $(PDF)
	@for i in $(PDF) ; do $(XPDF) $$i & done

pdf: $(PDF)
