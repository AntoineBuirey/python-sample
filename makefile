
VERSION = $(shell python get_version.py)

MODULES = cache colors config http_code version singleton

TARGETS = $(addprefix dist/,$(addsuffix -$(VERSION).tar.gz,$(MODULES)))
TARGETS += $(addprefix dist/,$(addsuffix -$(VERSION)-py3-none-any.whl,$(MODULES)))

.PHONY: all clean tests

all: $(TARGETS)

dist/%-$(VERSION)-py3-none-any.whl: % %/pyproject.toml
	python build_package.py --version $(VERSION) --wheel --outdir dist $<
	@rm -rf $</$<.egg-info $</build

dist/%-$(VERSION).tar.gz: % %/pyproject.toml
	python build_package.py --version $(VERSION) --sdist --outdir dist $<
	@rm -rf $</$<.egg-info $</build

tests/%: % #with pytest
	-@coverage run --data-file $<.coverage --branch -m pytest --tb=short --disable-warnings --junitxml=tests_reports/$*/report.xml $<
	@coverage html -d tests_reports/$*/coverage --data-file $<.coverage
	@coverage xml -o tests_reports/$*/coverage.xml --data-file $<.coverage
	@coverage report -m --data-file $<.coverage
	@rm $<.coverage

tests: $(addprefix tests/,$(MODULES))

clean:
	rm -rf dist
	rm -rf **/*.egg-info **/build
