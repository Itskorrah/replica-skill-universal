---
name: replica-launch
description: >-
  Writes the launch for an app clone: the landing page built on the
  positioning angle, pricing set against the original's public pricing and
  its users' complaints, and the App Store and Google Play listing linted
  against the stores' limits and copycat rules. Use when the user says
  "landing page", "pricing", "how much should I charge", "App Store
  listing", "store screenshots", "launch plan", "Product Hunt", or after
  /replica-brand.
---

# replica-launch

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

Reads `replica/fixes.md` (the angle and the evidence), `replica/brand.md`,
and `replica/brand.json`. Writes `replica/launch/`: `landing.md`,
`pricing.md`, `listing.json`, `launch-plan.md`.

```bash
python "<PACK_ROOT>/replica-launch/listing.py" replica/launch/listing.json      # limits, claims, the original's name
```

Start from `listing.example.json` in this folder.

## The rules

- **No fake proof.** No invented testimonials, user counts, star ratings,
  press logos or "trusted by" rows. An empty proof section is better than a
  fake one. Real beta users, with permission, are fine.
- **No reviewer quotes as testimonials.** The original's reviews are research.
- **The original's name stays out** of your app name, store listing, keywords
  and ads. Apple and Google reject it, and it invites a takedown.

## Step 1: landing page

`landing.md`, section by section, then build it in the project:

1. **Hero**: the angle as a headline (what you do, for whom), one line under
   it, one button. Screenshot of the real product.
2. **The problem**: the top two "hate" themes, in plain words. Paraphrase,
   do not quote reviewers.
3. **How it works**: three steps, from the core flow.
4. **Features**: each tied to a fix from `fixes.md`. Lead with the fixes,
   not the parity features. Parity is the price of entry.
5. **Pricing**: the table from step 2.
6. **FAQ**: the real objections, including "can I import from {{category}}
   tools?" if you built an importer.
7. **Final call to action.**

Copy in the brand voice. Run replica-design's contrast check on the page.

## Step 2: pricing

`pricing.md`:

- The original's public pricing page and 2 or 3 alternatives, in one table,
  with the URL and the date read. Prices change, so the date matters.
- What reviewers said about price and billing, from `feedback.md`, with counts.
- The model: free plan or trial, per seat or flat, monthly and annual
  (annual usually 2 months free).
- Three tiers at most. Name them by who they are for.
- Fix the billing complaints in the product: one-click cancel, clear renewal
  emails, no surprise per-seat jumps.
- The Stripe products and prices to create (the user creates them).

## Step 3: store listing

Fill `listing.json`, then:

```bash
python "<PACK_ROOT>/replica-launch/listing.py" replica/launch/listing.json
```

It checks App Store limits (name 30, subtitle 30, promotional text 170,
keywords 100, description 4000) and Google Play's (title 30, short
description 80, full 4000), counts characters the way a person does, flags
ranking and price claims in short fields, emoji, wasted keyword characters,
and **any name from `avoid`** anywhere in the listing. Exit 1 on an error.

Apple's App Review Guideline 4.1 (Copycats) rejects apps that simply copy a
popular app or make minor changes to another app's name or UI. Your fixes
and your own brand are what get you through review, so make them visible in
the screenshots and the first lines of the description.

Also prepare: screenshots at the current required sizes (check App Store
Connect and Play Console when you upload, they change), privacy labels and
the data safety form, privacy policy and support URLs, age rating, and review
notes with a demo account the reviewer can use.

## Step 4: launch plan

`launch-plan.md`: a waitlist or beta list before launch, analytics and error
tracking live, where the original's unhappy users talk (the Reddit threads
and communities from the research), a Product Hunt or Hacker News post that
leads with the fix, and the first 10 users to talk to by hand.

## Output

`replica/launch/` complete, the landing page built, `listing.py` passing.
Next: `/replica-deploy`.
