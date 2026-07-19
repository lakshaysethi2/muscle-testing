# TruthCheck

A community-driven muscle testing platform inspired by the teachings of Dr. David R. Hawkins (Power vs. Force, The Map of Consciousness).

## Quick Start

```bash
# Copy environment file
cp .env.example .env

# Build and start
make build
make up
```

The app will be available at **http://localhost:8000**.

## Requirements

- Docker & Docker Compose

## Makefile Commands

| Command | Description |
|---------|-------------|
| `make build` | Build Docker images |
| `make up` | Start all services |
| `make down` | Stop all services |
| `make test` | Run test suite |
| `make shell` | Open shell in web container |
| `make migrate` | Run database migrations |
| `make lint` | Run ruff + black check |
| `make lintfix` | Auto-fix lint issues |
| `make logs` | Tail container logs |

## Tech Stack

- **Backend:** Django 5.x, Django REST Framework
- **Frontend:** Django Templates + HTMX + Alpine.js + Tailwind CSS
- **Database:** SQLite (dev), PostgreSQL (prod)
- **Cache:** Redis 7
- **Auth:** django-allauth (Google, Facebook, Discord, Telegram)

## Environment Variables

Only 4 variables needed in `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `DJANGO_SECRET_KEY` | — | Django secret key (required) |
| `DJANGO_DEBUG` | `True` | Debug mode |
| `DJANGO_ENV` | `dev` | `dev` or `prod` |
| `DATABASE_URL` | `sqlite:///data/db.sqlite3` | Database URL |

## Disclaimer

The calibrations on this platform are user-reported for spiritual and personal exploration purposes only. They are not medical diagnoses, professional advice, or claims of scientific fact. Always consult a qualified professional for health decisions.
