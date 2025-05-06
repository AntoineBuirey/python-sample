
MODULES = cache colors config http_code version

TARGETS = $(addprefix dist/,$(addsuffix -0.1.0.tar.gz,$(MODULES)))
TARGETS += $(addprefix dist/,$(addsuffix -0.1.0-py3-none-any.whl,$(MODULES)))

.PHONY: all clean tests

all: $(TARGETS)

dist/%-0.1.0-py3-none-any.whl: dist/%-0.1.0.tar.gz
	python3 -m pip wheel --no-deps --wheel-dir dist $<

dist/%-0.1.0.tar.gz: %
	python3 -m build --sdist --outdir dist $<

tests/%: % #with pytest
	-coverage run -m --branch pytest --tb=short --disable-warnings --junitxml=tests_reports/$*/report.xml $<
	@coverage report -m
	@coverage html -d tests_reports/$*/coverage
	@rm .coverage

tests: $(addprefix tests/,$(MODULES))

clean:
	rm -rf dist
