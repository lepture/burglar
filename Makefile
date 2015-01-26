.PHONY: test coverage


test:
	@nosetests -s

coverage:
	@rm -f .coverage
	@nosetests --with-coverage --cover-package=burglar --cover-html
