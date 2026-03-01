# Makefile for building Doxygen documentation and C_Linux

# Variables
DOXYGEN_SH = ./doxygen.sh
DOXYFILE   = Doxyfile
DOCS_DIR   = docs
OUTDIR     = docs/html
CC         = gcc
CFLAGS     = -Wall -O2
SRC_DIR    = src

# Find all .c files in src subfolders
SRCS := $(shell find $(SRC_DIR) -name "*.c")
OBJS := $(SRCS:.c=.o)

# Find all subfolders in src
SUBDIRS := $(shell find $(SRC_DIR) -mindepth 1 -type d)

# Default target
all: build doc_build doc link_all

# Build .o files for all .c files
build: $(OBJS)
	@echo "==> Build of object files completed."

# Link all .o in each folder to one executable named as the folder
link_all: $(SUBDIRS)
	@echo "==> Linking completed for all subfolders."

$(SUBDIRS):
	@echo "Linking objects in $@..."
	@OBJS_IN_DIR=$$(find $@ -maxdepth 1 -name "*.o"); \
	if [ ! -z "$$OBJS_IN_DIR" ]; then \
		$(CC) $(CFLAGS) $$OBJS_IN_DIR -o $@; \
		echo "Executable created: $@"; \
	fi

# Pattern rule to build .o from .c
%.o: %.c
	@echo "Compiling $<..."
	$(CC) $(CFLAGS) -c $< -o $@

# Build Documentation target (Doxygen setup script)
doc_build:
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
	@echo "==> Removing object files in src..."
	@find $(SRC_DIR) -name "*.o" -type f -exec rm -f {} \;
	@echo "==> Removing executables in src..."
	@find $(SRC_DIR) -mindepth 1 -type f ! -name "*.c" ! -name "*.txt" ! -name "*.h" ! -name "*.hpp" -executable -exec rm -f {} \;
	@echo "==> Removing documentation output directory..."
	@rm -rf $(DOCS_DIR)
	@echo "==> Clean completed."