# PLAN.md

## Current Sprint Goal

**Phase 1 — MVP Foundation**: Scaffold the entire project with Docker, Django, core apps,
task-management files, and a working landing page. Then build features one-by-one.

---

## In Progress

> _(Agent: move the task you're working on here before starting)_

- [ ] **F-04: Guest/Anonymous Mode** — Session-based usage without login

---

## To Do (Feature Queue)

> Each feature is built → tested → committed → moved to Done.
> Build ONE feature at a time.

### Auth & Accounts
- [x] **F-02: Custom User Model** — Extend AbstractUser, add bio, avatar, testing preferences
- [x] **F-03: OAuth Integration** — Google, Facebook, Discord, Telegram via django-allauth
- [ ] **F-04: Guest/Anonymous Mode** — Session-based usage without login
- [ ] **F-05: User Profile Pages** — Display name, avatar, bio, calibration history

### Core Muscle Testing
- [ ] **F-06: Calibration Model** — Subject, result (strong/weak), scale value, method, visibility
- [ ] **F-07: Guided Testing Wizard** — Step-by-step interactive flow (prerequisites → method selection → test → result)
- [ ] **F-08: Testing Methods Content** — O-ring, finger-over-finger, sway test, interlocking O-ring

### Community Database
- [ ] **F-09: Public Calibration Feed** — Browse, filter, search community calibrations
- [ ] **F-10: Voting & Verification** — Upvote/verify community entries
- [ ] **F-11: Moderation System** — Flagging, admin review queue

### Practice & Dashboard
- [ ] **F-12: Practice Mode** — Reference items, accuracy tracking, challenges
- [ ] **F-13: Personal Dashboard** — History, charts, streaks, export

### Bots
- [ ] **F-14: Discord Bot** — /calibrate, /lookup, /practice, /myhistory, /leaderboard
- [ ] **F-15: Telegram Bot** — Same commands as Discord

### Polish
- [ ] **F-16: Mobile Responsiveness Audit** — Test all pages on mobile
- [ ] **F-17: Accessibility Audit** — WCAG 2.1 AA check
- [ ] **F-18: Rate Limiting** — django-ratelimit on all public endpoints
- [ ] **F-19: i18n Scaffolding** — Mark strings for translation
- [ ] **F-20: README** — Full setup instructions

---

## Done ✅

- [x] **F-01: Project Foundation** — Directory structure, Docker, Makefile, Django scaffold, landing page
- [x] **F-03: OAuth Integration** — Google, Facebook, Discord, Telegram via django-allauth, styled login/signup/logout, social_providers context processor, 35 tests
- [x] **F-02: Custom User Model** — TestingMethod enum, karma, display_name, profile views + templates, 17 tests

---

## Open Questions / Agent Questions

> _(Agent: add questions here instead of guessing)_

1. Frontend approach: Django Templates + HTMX + Alpine.js (chosen) vs Next.js SPA?
   - **Decision:** Django Templates + HTMX + Alpine.js — simpler, avoids separate frontend build.

---

## Discovered Tasks

> _(Agent: add newly discovered necessary tasks here)_
