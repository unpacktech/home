generate:
	python build/generate.py
	cp -r assets/* static

sync:
	python build/sync.py

deps:
	pip install -r build/requirements.txt
	mkdir -p static
	mkdir -p content

env:
	python3 -m virtualenv env

clean:
	rm -rf ./static/*

serve:
	python build/serve.py

.PHONY: deps generate clean serve theme
