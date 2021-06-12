.PHONY: clean quick_test test develop

plugin.ankiaddon:
	python setup.py build
	cd build/lib/anki_guess_ease/ && zip plugin.ankiaddon -r *
	mv build/lib/anki_guess_ease/plugin.ankiaddon .

clean:
	-rm -r build dist **/*.egg-info plugin.ankiaddon
	pyclean .

quick_test:
	flake8 anki_guess_ease
	mypy anki_guess_ease
	black --check .

test:
	tox

develop:
	ln -s ${PWD}/anki_guess_ease ~/.local/share/Anki2/addons21/$$(basename ${PWD})_develop
