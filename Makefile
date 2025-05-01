.PHONY: install deploy test

install:
	pip install -r requirements.txt
	npm install
	echo "Done"

deploy:
	npx serverless deploy

test:
	PYTHONPATH=$PYTHONPATH:. python -m pytest -p no:warnings

clean:
	rm -rf .serverless
	rm -rf __pycache__
	rm -rf .pytest_cache 