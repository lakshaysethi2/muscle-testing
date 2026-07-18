# CHANGELOG.md

All notable changes to KineticTruth are documented here.

---

## [Unreleased]

### Added (Session: 2026-07-18)
- Project foundation: directory structure, Docker, Makefile, Django scaffold
- `AGENTS.md`, `PLAN.md`, `ROADMAP.md`, `CHANGELOG.md` — task-management files
- `config/settings/base.py`, `dev.py`, `prod.py` — environment-aware settings
- SQLite for dev, PostgreSQL for prod via `DATABASE_URL`
- Docker Compose with `web` and `redis` services
- Makefile wrapping all `docker compose` commands
- `.env` with 4 variables: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ENV`, `DATABASE_URL`
- `apps/core`, `apps/accounts`, `apps/calibrations`, `apps/community`, `apps/practice`, `apps/dashboard`, `apps/bots` — app stubs
- `templates/base.html` — base template with Tailwind, Alpine.js, HTMX, disclaimer footer
- `templates/pages/home.html` — landing page
- `requirements.txt` and `requirements-dev.txt` with pinned version ranges
