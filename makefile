
VERSION = 0.1.0

MODULES = cache colors config http_code version

TARGETS = $(addprefix dist/,$(addsuffix -$(VERSION).tar.gz,$(MODULES)))
TARGETS += $(addprefix dist/,$(addsuffix -$(VERSION)-py3-none-any.whl,$(MODULES)))

.PHONY: all clean tests

all: $(TARGETS)

dist/%-$(VERSION)-py3-none-any.whl: dist/%-$(VERSION).tar.gz
	python -m pip wheel --no-deps --wheel-dir dist $<

dist/%-$(VERSION).tar.gz: %
	python build_package.py --version $(VERSION) --sdist --outdir dist $<

tests/%: % #with pytest
	-@coverage run --data-file $<.coverage --branch -m pytest --tb=short --disable-warnings --junitxml=tests_reports/$*/report.xml $<
	@coverage html -d tests_reports/$*/coverage --data-file $<.coverage
	@coverage xml -o tests_reports/$*/coverage.xml --data-file $<.coverage
	@coverage report -m --data-file $<.coverage
	@rm $<.coverage

tests: $(addprefix tests/,$(MODULES))

clean:
	rm -rf dist
