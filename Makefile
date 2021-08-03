.PHONY deps

deps:
	pip3 install -r requirements.in

qualys_rss.zip:
	./build-package.sh
