init:
	pip3 install -r requirements.txt --upgrade
	pip3 install -r requirements-dev.txt --upgrade

test:
	py.test -v

cov:
	py.test -v --cov=quantbube --cov-report html

publish:
	doc

docs:
	pass

flake8:
	pass





