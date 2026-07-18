# AGENTS.md

## Who Uses This File

Any AI coding agent (Claude, GPT, Gemini, Cursor, etc.) working on this
codebase MUST read this file before writing any code.

---

## Golden Rules

1. NEVER delete or rewrite large sections of code without explicit instruction.
2. ALWAYS write or update tests for any code you add or change.
3. ALWAYS update `CHANGELOG.md` after completing any task.
4. ALWAYS update `PLAN.md` to mark tasks complete and add new ones discovered.
5. NEVER hardcode secrets — use environment variables via `.env`.
6. ALWAYS keep `requirements.txt` in sync with new dependencies.
7. ASK (via a comment in `PLAN.md`) before making architectural decisions.
8. PREFER small, focused commits over large sweeping changes.
9. ALWAYS run linting (`ruff`, `black`) before considering a task done.
10. ALWAYS run the test suite before considering a task done.

---

## Build Cycle (Feature-by-Feature)

This project is built in stages. For each feature:

1. **PLAN** — Update `PLAN.md` with what you're about to build.
2. **BUILD** — Write the code, models, views, templates, tests.
3. **TEST** — Run `make test` — all tests must pass.
4. **FIX** — If bugs, fix them. Re-run tests.
5. **COMMIT** — Commit with a meaningful conventional-commit message.
6. **UPDATE** — Update `CHANGELOG.md` and mark done in `PLAN.md`.
7. **STOP** — Wait for the human to review before moving to the next feature.

---

## How to Start a New Task

1. Read `PLAN.md` → find the next uncompleted task.
2. Read `CHANGELOG.md` → understand what changed recently.
3. Write your plan in a comment at the top of `PLAN.md` before coding.
4. Code the feature/fix.
5. Write tests in `tests/`.
6. Run: `make test` — all tests must pass.
7. Update `CHANGELOG.md` with what you did.
8. Mark the task complete in `PLAN.md`.
9. Commit with a meaningful message: `feat(calibrations): add O-ring method flow`.

---

## Commit Message Format (Conventional Commits)

- `feat(scope): description`
- `fix(scope): description`
- `refactor(scope): description`
- `docs(scope): description`
- `test(scope): description`
- `chore(scope): description`

---

## When You're Unsure

- Leave a `# AGENT-QUESTION:` comment in the relevant file.
- Add the question to `PLAN.md` under "Open Questions".
- Do NOT guess on architecture or auth decisions.

---

## Dependency Rules

- Research the latest stable version before adding any new package.
- Add to `requirements.txt` AND document why it was added in `CHANGELOG.md`.
- Never add a package that duplicates existing functionality.

---

## Testing Rules

- Use `pytest-django` fixtures — do NOT use Django's TestCase class.
- Use `factory_boy` for model factories.
- Mock all external API calls (Discord, Telegram, OAuth providers).
- Tests live in `tests/` directory.
- Run via `make test`.

---

## Code Style

- Python: follow PEP8, enforced by `ruff` and `black`.
- Max line length: 88 characters.
- All public functions must have docstrings.
- All models must have `__str__` and `Meta` class defined.

---

## Task Management

All task tracking lives in these files:

| File | Purpose |
|------|---------|
| `PLAN.md` | Current sprint plan, features in progress, todo, done |
| `ROADMAP.md` | Long-term vision across phases |
| `CHANGELOG.md` | Chronological log of all completed work |

---

## Environment / Config

- `.env` — 4 variables only: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ENV`, `DATABASE_URL`.
- SQLite for local dev, PostgreSQL for prod (`DATABASE_URL=postgres://...`).
- `DJANGO_ENV=dev` loads `config.settings.dev`; `DJANGO_ENV=prod` loads `config.settings.prod`.

---

## Makefile

The Makefile ONLY runs `docker compose` commands. Use it:

```bash
make build      # Build Docker images
make up         # Start services
make down       # Stop services
make test       # Run tests
make shell      # Bash in web container
make migrate    # Run migrations
```
