install-pkg:
	apt install pandoc

install-env:
	virtualenv -p python3 env

install-lib:
	env/bin/pip3 install -r requirements.txt

generate:
	env/bin/python3 scripts/generate.py
