.PHONY: install deploy test

install:
	pip install -r requirements.txt

deploy:
	serverless deploy

test:
	python -m pytest

clean:
	rm -rf .serverless
	rm -rf __pycache__
	rm -rf .pytest_cache 