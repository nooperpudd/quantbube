install:
	python3 setup.py install

test:
	py.test

build:
	python3 setup.py build

requirements:
	pip3 install -r requirements.txt --upgrade -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
	pip3 install -r requirements-dev.txt --upgrade -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com





