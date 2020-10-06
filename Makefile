clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	rm -rf .cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf htmlcov
	rm -rf .tox/
	rm -rf docs/_build
	pip install -e .[dev] --upgrade --no-cache
	
install:
	pip install -e .['dev']

run:
	python manager.py run
	
db_init:
	python manager.py db init

db_upgrade:
	python manager.py db upgrade

db_downgrade:
	python manager.py db downgrade
	
pip_freeze_requirements:
	pip freeze > requirements.txt