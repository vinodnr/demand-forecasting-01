.PHONY: up seed-dev seed-users seed-orgs logs stop

# Adjust these if your compose file or service names differ
COMPOSE_FILE=backend/monitoring/docker-compose.dev.yml
BACKEND_SERVICE=backend
POSTGRES_SERVICE=postgres

up:
	docker compose -f $(COMPOSE_FILE) up -d --build

stop:
	docker compose -f $(COMPOSE_FILE) down

logs:
	docker compose -f $(COMPOSE_FILE) logs -f $(BACKEND_SERVICE)

# Seed all dev data: users + orgs
seed-dev: seed-users seed-orgs

seed-users:
	docker compose -f $(COMPOSE_FILE) exec -T $(BACKEND_SERVICE) python backend/scripts/seed_test_users.py

seed-orgs:
	docker compose -f $(COMPOSE_FILE) exec -T $(BACKEND_SERVICE) python backend/scripts/seed_orgs_and_users.py
