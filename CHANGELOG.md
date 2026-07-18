# CHANGELOG.md

All notable changes to KineticTruth are documented here.

---

## [Unreleased]

### Added (Session: 2026-07-18)

#### F-02 — Custom User Model
- `TestingMethod` TextChoices enum on User: O_RING, FINGER_OVER_FINGER, SWAY, INTERLOCKING_O, PROXY, OTHER
- `karma` integer field (community trust score)
- `display_name` property (full_name → email → username)
- `calibration_count` property (placeholder for calibrations FK)
- `get_absolute_url` → `/u/profile/<username>/`
- Profile view at `/u/profile/<username>/` (public)
- Edit profile view at `/u/profile/edit/` (login-required)
- Profile & edit_profile templates with Tailwind
- Admin panel: list_display + search + fieldsets for TestingMethod + karma
- Navbar: "Profile" link when logged in
- 12 tests: User model (7), profile views (5)

#### F-01 — Project Foundation
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

