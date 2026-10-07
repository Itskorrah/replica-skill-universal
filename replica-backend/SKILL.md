---
name: replica-backend
description: >-
  Builds the backend of an app clone: auth, database migrations and access
  rules, payments with Stripe, email, background jobs and third-party
  integrations through official APIs only, plus a security checklist. Use when
  the user says "add login", "set up auth", "wire up the database", "add
  payments", "connect Stripe", "add Google Calendar", "send emails",
  "backend for my clone", or when /replica-build is running on fake data.
---

# replica-backend

## Running on any agent

Use this skill with the host's native skill loader, or read this `SKILL.md`
explicitly. References such as `/replica-design` name another skill: use its
native invocation (for example `$replica-design` in Codex), or load that
sibling's `SKILL.md`. They are not shell commands. Continue stages only within
the user's requested scope.

Keep the working directory at the user's app project. All `replica/` paths
refer to that project; templates and Python scripts belong to the skill pack.
In command examples, replace `<PACK_ROOT>` with the absolute directory
containing the eleven `replica-*` skill folders (the parent of this skill's
folder). Keep script paths quoted. Use an available Python 3.8+ interpreter:
`python`, `python3`, or `py -3` on Windows. Create output directories first.

Use the host's available file, terminal, web and browser tools. If a required
capability is unavailable, record what was not run and provide the concrete
manual step; never invent observations, screenshots, reviews or passing tests.
A chat without file/terminal access can follow the method but cannot execute
the Python tools. Preserve the rules and user approval gates below.

Reads `replica/architecture.md`. Writes migrations and server code, and keeps
`replica/backend.md` (checklist below) up to date.

## The rules

- **Official, public APIs only, with the user's own keys.** Never call the
  original app's private endpoints, never reuse its OAuth client, never proxy
  through it.
- **The user creates accounts and keys.** The agent never signs up for services,
  never types a password, card or live key. The user creates the Stripe,
  Supabase, Resend or Google Cloud project and puts keys in `.env.local`.
  The agent writes `.env.example` with every variable name and no values.
- **Test mode first.** Stripe test keys and test cards until replica-deploy.

## Auth

- Email sign up with verification, password reset, magic link if the original
  has it. OAuth (Google, Apple) with the user's own developer apps.
- Sessions: http-only secure cookies. Sign out everywhere.
- Roles and teams if the recon map has them: owner, admin, member, with one
  function that answers "can this user do this to this record".
- Account deletion that actually deletes. Apple requires it for apps with
  sign up.

## Database

- Migrations from `architecture.md`, checked in, run by a script.
- Access rules on every table: row level security policies on Supabase, or
  the authorisation function called in every query. Test it: a second user
  must get nothing back.
- Seed script with realistic fake data (no real people).
- Backups on (the host's daily backups count, check they are enabled).

## Payments

- Stripe Checkout for sign up to a plan, the Customer Portal for changes and
  cancelling. Do not build card forms.
- Webhooks: verify the signature, store the event id, make every handler
  idempotent (Stripe retries). Handle `checkout.session.completed`,
  `customer.subscription.updated`, `customer.subscription.deleted`,
  `invoice.payment_failed`.
- Subscription status lives in your database, updated by webhooks, read by
  your app. Never trust the client.
- Cancelling is one click. Hard-to-cancel billing is a top complaint about
  most apps, and in many places it is illegal.

## Email and jobs

- Transactional email through Resend or Postmark from your own domain.
  Templates written fresh.
- Jobs for anything time-based (reminders, digests, sync, cleanup) with
  retries and a dead-letter log. Times in UTC, shown in the user's zone.

## Integrations

For each integration in the feature matrix: the official API, the OAuth
scopes needed (fewest possible), the provider's review process, rate limits.
Google scopes like Calendar need Google's OAuth verification before public
launch, which takes weeks. Start it early and write that in `backend.md`.

## Security checklist

- [ ] secrets only in env vars, `.env*` in `.gitignore`, nothing in client bundles
- [ ] input validated on the server (zod or similar) on every route
- [ ] authorisation checked on every read and write, tested with a second user
- [ ] rate limits on auth, sign up, and anything that sends email or SMS
- [ ] webhooks verify signatures
- [ ] uploads: size and type limits, served from a separate domain or bucket
- [ ] no user data in URLs or logs
- [ ] dependencies audited (`npm audit`)
- [ ] privacy policy lists every processor (Stripe, Resend, host, analytics)

## Output

Working auth, database, payments in test mode, email and the integrations,
`.env.example`, `replica/backend.md` with the checklist ticked, feature
matrix rows updated. Next: `/replica-test`.
