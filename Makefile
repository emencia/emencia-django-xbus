delpyc:
	find . -name "*\.pyc"|xargs rm -f

migrate:
	python runmigrations.py

test:
	tox
