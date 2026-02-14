.SILENT:

# docker
build: 
	docker compose build

up: 
	docker compose up -d

down: 
	docker compose down

logs:
	docker compose logs -f

restart: 
	docker compose restart app

restart-full: 
	docker compose restart

# ruff
lint: 
	uv run ruff check . 

lint-fix: 
	uv run ruff check . --fix

lint-fix-all: 
	uv run ruff check . --fix --unsafe-fixes

# pyright
lint-type: 
	uv run pyright

# alembic
migrate-new:
	docker compose exec app uv run alembic stamp head

migrate-collect:
	docker compose exec app uv run alembic revision --autogenerate

migrate-head:
	docker compose exec app uv run alembic upgrade head

# uv
sync:
	uv sync --all-groups
lock:
	uv lock

# tree
tree:
	tree > tree.txt
	