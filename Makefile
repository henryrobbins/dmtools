test:
	coverage run -m pytest

cov:
	coverage report --include=dmtools/*

cov-html:
	coverage html
	open htmlcov/index.html

dist:
	python3 -m build
	twine upload dist/*