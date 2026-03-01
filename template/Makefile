# Makefile for building Doxygen documentation

# Variables
DOXYGEN_SH = ./doxygen.sh
DOXYFILE   = Doxyfile
DOCS_DIR   = docs
OUTDIR     = docs/html

# Default target
all:
	@echo "Use 'make build' 'make doc' to build README Template and generate the documentation for your code!"

# Build Documentation target
build:
	@echo "==> Running Doxygen setup script..."
	@$(DOXYGEN_SH)

# Make Documentation target
doc:
	@echo "==> Running Doxygen with $(DOXYFILE)..."
	@doxygen $(DOXYFILE)
	@echo "==> Documentation successfully generated in $(DOCS_DIR)/"
	@echo "==> Copying image assets to the HTML output folder..." 
	@cp -R Images $(OUTDIR) 2>/dev/null || true
	@echo "==> Copy completed."


# Clean target
clean:
	@echo "==> Removing documentation output directory..."
	@rm -rf $(DOCS_DIR)
	@echo "==> Clean completed."
