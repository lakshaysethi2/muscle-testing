# CHANGELOG.md

All notable changes to TruthCheck are documented here.

---

## [Unreleased]

### Added (Session: 2026-07-19)

#### F-03 — OAuth Integration
- Styled allauth templates: login (social buttons + email/password), signup, logout
- Custom `social_providers` context processor — social buttons only shown when providers configured in Django admin
- Google, Facebook, Discord SVG icons inline on login page
- ACCOUNT_LOGOUT_ON_GET=True for simple sign-out flow
- ACCOUNT_EMAIL_VERIFICATION=none for dev convenience
- No new .env vars — social providers configured via Django admin (allauth SocialApp)
- 13 auth tests: login (4), signup (6), logout (2), context processor (1)
- Total test suite: 35 tests

### Added (Session: 2026-07-18)

#### F-02 — Custom User Model
- `TestingMethod` TextChoices enum on User: O_RING, FINGER_OVER_FINGER, SWAY, INTERLOCKING_O, PROXY, OTHER
- `karma` integer field (community trust score)
- `display_name` property (full_name → email → username)
- `calibration_count` property (guarded with `hasattr` until Calibration model exists)
- `get_absolute_url` → `/u/profile/<username>/`
- Profile view at `/u/profile/<username>/` (public)
- Edit profile view at `/u/profile/edit/` (login-required) — uses `ProfileEditForm` with `ChoiceField` validation
- Profile & edit_profile templates with Tailwind
- Admin panel: list_display + search + fieldsets for TestingMethod + karma
- Navbar: "Profile" link when logged in
- **PR review fixes:** docker-entrypoint.sh for auto-migrate, form validation on testing_method, guarded calibration_count, mandatory SECRET_KEY in prod
- **UX fix:** Coming-soon placeholder pages at /test/, /community/, /practice/, /dashboard/ with "🚧 Coming Soon" + feature code
- Homepage "Start Testing" and "Community DB" buttons now link to real URLs (no more dead `href="#"`)
- Navbar: "Test" and "Community" links
- 22 tests: User model (8), profile views (7), core (6), prod settings (1)

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

