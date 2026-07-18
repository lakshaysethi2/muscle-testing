.PHONY: help build up down logs shell test lint migrate check clean

help: ## Show this help
	@echo "KineticTruth — Docker Compose Commands"
	@echo "======================================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'

build: ## Build Docker images
	docker compose build

up: ## Start all services
	docker compose up

down: ## Stop all services
	docker compose down

logs: ## Tail logs
	docker compose logs -f

shell: ## Open a shell in the web container
	docker compose exec web bash

dbshell: ## Open Django dbshell
	docker compose exec web python manage.py dbshell

test: ## Run test suite
	docker compose exec web pytest

lint: ## Run linting
	docker compose exec web ruff check apps/ config/ tests/ manage.py
	docker compose exec web black --check apps/ config/ tests/ manage.py

lintfix: ## Auto-fix linting issues
	docker compose exec web ruff check --fix apps/ config/ tests/ manage.py
	docker compose exec web black apps/ config/ tests/ manage.py

check: ## Run Django checks
	docker compose exec web python manage.py check

migrate: ## Run migrations
	docker compose exec web python manage.py migrate

makemigrations: ## Make migrations
	docker compose exec web python manage.py makemigrations

createsuperuser: ## Create a superuser
	docker compose exec web python manage.py createsuperuser

collectstatic: ## Collect static files
	docker compose exec web python manage.py collectstatic --noinput

restart: ## Restart web service
	docker compose restart web

clean: ## Remove containers and images
	docker compose down --rmi all --volumes --remove-orphans
