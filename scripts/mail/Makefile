install-pkg:
	sudo apt install pandoc

install-env:
	rm -rf .virtualenv
	virtualenv -p python3 .virtualenv
	.virtualenv/bin/pip3 install -r requirements.txt

mail:
	.virtualenv/bin/python3 script.py
