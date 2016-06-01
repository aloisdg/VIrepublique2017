install-env:
	virtualenv -p python3 env

generate:
	env/bin/python3 scripts/generate.py
