.PHONY: prepare
prepare:
	rm -rf xdelta3/lib/ || true
	mkdir xdelta3/lib/
	cp xdelta/xdelta3/xdelta3*.c xdelta3/lib/
	cp xdelta/xdelta3/xdelta3*.h xdelta3/lib/
	rm xdelta3/lib/*test.h

.PHONY: install
install: prepare
	pip install -U setuptools pip
	pip install -U .
	pip install -r tests/requirements.txt

.PHONY: isort
isort:
	isort -rc -w 120 xdelta3
	isort -rc -w 120 tests

.PHONY: lint
lint:
	python setup.py check -rms
	flake8 xdelta3/ tests/
	pytest xdelta3 -p no:sugar -q

.PHONY: test
test: prepare
	pytest --cov=xdelta3

.PHONY: quickbuild
quickbuild: prepare
	rm *.so || true
	python setup.py build --build-lib . && printf "\n  build succeeded\n\n"

.PHONY: testcov
testcov: quickbuild
	pytest --cov=xdelta3 && (echo "building coverage html"; coverage html)

.PHONY: all
all: testcov lint

.PHONY: clean
clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -rf xdelta3/lib/
	rm -rf htmlcov
	rm -rf *.egg-info
	rm -rf *.so
	rm -rf dist
	rm -f .coverage
	rm -f .coverage.*
	rm -rf build
	python setup.py clean
