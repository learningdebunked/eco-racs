.PHONY: install test lint format run docker-build docker-up clean

install:
	pip install -r requirements.txt
	pip install -e .

test:
	pytest tests/ -v --cov=src/cac

lint:
	flake8 src/ tests/
	mypy src/

format:
	black src/ tests/
	isort src/ tests/

run:
	uvicorn cac.api.checkout_api:app --reload

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov dist build *.egg-info
