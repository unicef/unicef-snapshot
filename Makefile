BUILDDIR=build
BUILD_NUMBER=0
PYPI_SERVER?=pypi.org
PYPI_INDEX?=https://${PYPI_SERVER}/simple/
DATABASE_URL?=

help:
	@echo '                                                                       '
	@echo 'Usage:                                                                 '
	@echo '   make clean                       remove the generated files         '
	@echo '   make fullclean                   clean + remove tox, cache          '
	@echo '   make coverage                    run coverage                       '
	@echo '   make test                        run tests                          '
	@echo '   make develop                     update develop environment         '
	@echo '   make requirements                generate requirements files from Pipfile'
	@echo '                                                                       '


.mkbuilddir:
	mkdir -p ${BUILDDIR}


.init-db:
	# initializing '${DBENGINE}' database '${DBNAME}'
	psql -c 'DROP DATABASE IF EXISTS test_snapshot;' -U postgres -h 127.0.0.1
	psql -c 'DROP DATABASE IF EXISTS snapshot;' -U postgres -h 127.0.0.1
	psql -c 'CREATE DATABASE snapshot;' -U postgres -h 127.0.0.1


develop: .init-db
	@${MAKE} clean
	pipenv install
	pip install -e .[test]


clean:
	# cleaning
	@rm -rf ${BUILDDIR} .pytest_cache src/unicef_snapshot.egg-info dist *.xml .cache *.egg-info .coverage .pytest MEDIA_ROOT MANIFEST .cache *.egg build STATIC
	@find . -name __pycache__  -prune | xargs rm -rf
	@find . -name "*.py?" -o -name "*.orig" -o -name "*.min.min.js" -o -name "*.min.min.css" -prune | xargs rm -rf
	@rm -f coverage.xml flake.out pep8.out pytest.xml


fullclean:
	rm -fr .tox
	rm -f *.sqlite
	make clean


lint:
	flake8 src/ tests/; exit 0;
	isort src/ tests/ --check-only -rc; exit 0;


requirements:
	pipenv lock -r > src/requirements/install.pip
	pipenv lock -r -d > src/requirements/testing.pip
	sed -i "" 's/\(.*\)==.*/\1/g' src/requirements/install.pip && sed -i "" '1d' src/requirements/install.pip
	sed -i "" 's/\(.*\)==.*/\1/g' src/requirements/testing.pip && sed -i "" '1d' src/requirements/testing.pip


test:
	pytest tests/ src/ \
            --cov=unicef_snapshot \
            --cov-config=tests/.coveragerc \
            --cov-report=html \
            --cov-report=term
