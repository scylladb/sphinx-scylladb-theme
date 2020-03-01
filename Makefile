# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = bin/sphinx-build
PAPER         =
BUILDDIR      = _build

# Internal variables.
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .
# the i18n builder cannot share the environment and doctrees with the others
I18NSPHINXOPTS  = $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .

.PHONY: all
all: dirhtml

.PHONY: pristine
pristine: clean
	git clean -dfX

.PHONY: deploy
deploy: dirhtml
	./_utils/deploy.sh

.PHONY: sphinx-clean
sphinx-clean:
	rm -rf ./bin
	rm -rf ./lib
	rm -rf ./lib64

bin/sphinx-build:
	./_utils/setup.sh

.PHONY: clean
clean:
	rm -rf $(BUILDDIR)/*

.PHONY: preview
preview: dirhtml
	./_utils/preview.sh

.PHONY: dirhtml
dirhtml: $(SPHINXBUILD)
	$(SPHINXBUILD) -b dirhtml $(ALLSPHINXOPTS) $(BUILDDIR)/dirhtml
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/dirhtml."

.PHONY: singlehtml
singlehtml: $(SPHINXBUILD)
	$(SPHINXBUILD) -b singlehtml $(ALLSPHINXOPTS) $(BUILDDIR)/singlehtml
	@echo
	@echo "Build finished. The HTML page is in $(BUILDDIR)/singlehtml."

.PHONY: epub
epub: $(SPHINXBUILD)
	$(SPHINXBUILD) -b epub $(ALLSPHINXOPTS) $(BUILDDIR)/epub
	@echo
	@echo "Build finished. The epub file is in $(BUILDDIR)/epub."

.PHONY: epub3
epub3: $(SPHINXBUILD)
	$(SPHINXBUILD) -b epub3 $(ALLSPHINXOPTS) $(BUILDDIR)/epub3
	@echo
	@echo "Build finished. The epub3 file is in $(BUILDDIR)/epub3."

.PHONY: dummy
dummy: $(SPHINXBUILD)
	$(SPHINXBUILD) -b dummy $(ALLSPHINXOPTS) $(BUILDDIR)/dummy
	@echo
	@echo "Build finished. Dummy builder generates no files."

.PHONY: linkcheck
linkcheck: $(SPHINXBUILD)
	$(SPHINXBUILD) -b linkcheck . $(BUILDDIR)/linkcheck
