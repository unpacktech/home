generate:
	python build/generate.py

deps:
	pip install -r build/requirements.txt
	mkdir -p static

env:
	python3 -m virtualenv env

clean:
	rm -rf ./static/*

serve:
	python build/serve.py

.PHONY: deps generate clean serve theme
