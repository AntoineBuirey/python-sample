
VERSION = $(shell python get_version.py)

DEPENDENCIES_NAMES = jsonschema requests tomlkit coverage pytest PyYAML

MODULES = cache colors config http_code version singleton

TARGETS = $(addprefix dist/,$(addsuffix -$(VERSION).tar.gz,$(MODULES)))
TARGETS += $(addprefix dist/,$(addsuffix -$(VERSION)-py3-none-any.whl,$(MODULES)))

PYTHON_PATH = $(shell if [ -d env/bin ]; then echo "env/bin/"; elif [ -d env/Scripts ]; then echo "env/Scripts/"; else echo ""; fi)
PYTHON_LIB = $(shell find env/lib -type d -name "site-packages" | head -n 1; if [ -d env/Lib/site-packages ]; then echo "env/Lib/site-packages/"; fi)
PYTHON = $(PYTHON_PATH)python

.PHONY: all clean tests

all: $(TARGETS)


# Dependencies handling

DEPENDENCIES_PATHS = $(addprefix $(PYTHON_LIB)/,$(DEPENDENCIES_NAMES))

$(PYTHON_LIB)/%: 
	$(PYTHON) -m pip install $*

install: $(DEPENDENCIES_PATHS)


dist/%-$(VERSION)-py3-none-any.whl: % %/pyproject.toml
	python build_package.py --version $(VERSION) --wheel --outdir dist $<
	@rm -rf $</$<.egg-info $</build

dist/%-$(VERSION).tar.gz: % %/pyproject.toml
	python build_package.py --version $(VERSION) --sdist --outdir dist $<
	@rm -rf $</$<.egg-info $</build

tests/%: % install
	-@coverage run --data-file $<.coverage --branch -m pytest --tb=short --disable-warnings --junitxml=tests_reports/$*/report.xml $<
	@coverage html -d tests_reports/$*/coverage --data-file $<.coverage
	@coverage xml -o tests_reports/$*/coverage.xml --data-file $<.coverage
	@coverage report -m --data-file $<.coverage
	@rm $<.coverage

tests: $(addprefix tests/,$(MODULES))

clean:
	rm -rf dist
	rm -rf **/*.egg-info **/build
