install-pkg:
	sudo apt install pandoc

install-env:
	virtualenv -p python3 .virtualenv
	.virtualenv/bin/pip3 install -r requirements.txt

generate:
	.virtualenv/bin/python3 scripts/generate.py

clean:
	rm -rf .virtualenv
