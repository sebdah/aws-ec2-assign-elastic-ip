install:
	python setup.py build
	python setup.py install
release:
	python setup.py sdist
	python setup.py register
	python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
