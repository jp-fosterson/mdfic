"""
mdfic.makefile - Create project makefiles
"""

SINGLE_TEMPLATE = """


default: pdf html docx

all: pdf html docx epub mobi tex

pdf: out/$(STORY)-article.pdf out/$(STORY)-sffms.pdf

html: out/$(STORY).html

docx: out/$(STORY)-plain.docx out/$(STORY)-sffms.docx

epub: out/$(STORY).epub

mobi: out/$(STORY).mobi

tex: $(STORY)-article.tex $(STORY)-sffms.tex

css: out/$(STORY).css

view: .view

##############################
%-article.tex: metadata.yaml %.md
	mdfic latex --documentclass=article --output=$@ $^

%-sffms.tex: metadata.yaml %.md
	mdfic latex --documentclass=sffms --output=$@ $^

out/%.pdf: %.tex | out
	pdflatex $<
	pdflatex $<
	mv `basename $@` $@


# out/%.pdf: out/%.docx | out
# 	mdfic pages-to-pdf $< --output=$@

out/%.html: %.md out/%.css | out
	mdfic html --css=out/$*.css  $< -o $@ 

out/%-plain.docx: %.md | out
	mdfic docx --no-sffms --output=$@ $<

out/%-sffms.docx: %.md | out
	mdfic docx --sffms --output=$@ $<

out/%.epub: %.md | out
	pandoc metadata.yaml $< -o $@

out/%.mobi: %.md | out
	pandoc metadata.yaml $< -o $@

out/%.css: | out
	mdfic css -o $@

out:
	mkdir out

.view: out/$(STORY).html
	open out/$(STORY).html
	touch .view


###########################
clean:
	rm -vf  *.aux *.log *.synctex.gz *.toc *.out *~ 
	rm -vf $(STORY).tex $(STORY)-article.tex $(STORY)-sffms.tex

out-clean:
	rm -vrf out

all-clean: clean out-clean
"""


#-----------------------------------

MULTI_TEMPLATE = """
HTMLPARTS := $(patsubst %.md,out/%.html,$(wildcard $(STORY)-*.md))

default: pdf html htmlparts docx 

all: default epub mobi tex

pdf: out/$(STORY)-article.pdf out/$(STORY)-sffms.pdf

html: out/$(STORY).html

htmlparts: $(HTMLPARTS)

docx: out/$(STORY)-plain.docx out/$(STORY)-sffms.docx

epub: out/$(STORY).epub

mobi: out/$(STORY).mobi

tex: $(STORY).tex

view: .view

$(STORY).md: $(STORY)-*.md metadata.yaml
	cat $(STORY)-*.md > $@
	
#######################
# Parts

%-article.tex: metadata.yaml %.md 
	mdfic latex --documentclass=article --output=$@  $^

%-sffms.tex: metadata.yaml %.md 
	mdfic latex --documentclass=sffms --output=$@ $^


out/%.pdf: %.tex | out
	pdflatex $<
	pdflatex $<
	mv `basename $@` $@

out/%.html: %.md out/%.css | out
	mdfic html --css=out/$*.css  $< -o $@ 

out/%-plain.docx: %.md metadata.yaml | out
	mdfic docx --no-sffms --output=$@ metadata.yaml $<

out/%-sffms.docx: %.md metadata.yaml | out
	mdfic docx --sffms --output=$@ metadata.yaml $<

out/%.epub: %.md metadata.yaml | out
	pandoc metadata.yaml $< -o $@

out/%.mobi: %.md metadata.yaml | out
	pandoc metadata.yaml $< -o $@

out/%.css: | out
	mdfic css -o $@

out:
	mkdir out

.view: out/$(STORY).html
	open out/$(STORY).html
	touch .view

###########################
clean:
	rm -vf  *.aux *.log *.synctex.gz *.toc *.out *~ 
	rm -vf $(STORY).md 
	rm -vf $(STORY).tex $(STORY)-article.tex $(STORY)-sffms.tex

out-clean:
	rm -vrf out

all-clean: clean out-clean
"""

def makefile(name, template='single'):
	"""
	"""
	return "STORY={}\n\n".format(name) + globals()[template.upper()+'_TEMPLATE']
