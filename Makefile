test:
	coverage run -m pytest

cov:
	coverage report --include=dmtools/*

cov-html:
	coverage html
	open htmlcov/index.html

lint:
	flake8 dmtools

.PHONY: dist
dist:
	rm -rf dist/*
	python3 -m build
	twine upload dist/*