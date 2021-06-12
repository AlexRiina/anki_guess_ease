.PHONY: clean test build build_test develop

plugin.ankiaddon:
	zip plugin.zip -j -r src

clean:
	rm -r build dist **/*.egg-info plugin.zip || true
	pyclean .

build:
	pip install .

build_test:
	pip install .[test]

test:
	flake8 src
	mypy src
	black --check .

develop:
	ln -s ${PWD}/src ~/.local/share/Anki2/addons21/$$(basename ${PWD})_develop
