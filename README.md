# The Replica skill - Universal

Eleven agent skills that clone any app. Works with Codex, Claude Code,
Antigravity, OpenCode, Cursor, Gemini CLI, GitHub Copilot, and other agents
through portable Markdown instructions. Free, MIT; no Replica account,
subscription or API key required. Your chosen agent and app services may
have their own requirements.

This fork preserves the original eleven skills, six Python tools, templates,
`replica/` outputs, clean-room rules and deployment approval. It adds portable
instructions, a cross-platform installer, and compatibility checks. See
[compatibility and verification](docs/compatibility.md) for supported paths
and the distinction between automated checks and pending live host sessions.

One reverse-engineers the app you want to clone. One rebuilds it. One tests it
for bugs. And one is the Entrepreneur: it reads what the app's users hate and
fixes it in yours, so you have an app you can sell.

In between, the others plan the stack and the database, rebuild the design
system, wire up auth and payments, score your clone against the original, give
it a name and a brand of its own, write the landing page and the store
listing, and put it live on your domain.

**It rebuilds what an app does, never what it owns.** Features and flows,
clean-room style. Not its code, its logo, its copy or its content. The
fine print is at the bottom, and the skills enforce it.

## Install

Clone this fork, then run the standard-library Python installer. These commands
work in PowerShell and POSIX shells; use `python3` or `py -3` if that is your
Python 3 command. Python 3.8+ is required. Nothing to pip install.

```text
git clone https://github.com/Itskorrah/replica-skill-universal.git
cd replica-skill-universal
python scripts/install.py install --host codex --project "/path/to/my app"
```

Replace the project path with your app directory, for example `"C:/work/My App"`
on Windows. The command installs **all eleven skills, tools and templates**
into that app's `.agents/skills/`. Run the skills while working in the app
project, not in this pack's checkout.

Choose a host with `--host`: `codex`, `claude`, `antigravity`, `antigravity-cli`,
`opencode`, `cursor`, `gemini`, `copilot`, `agents`, or `portable`. For example:

```text
python scripts/install.py install --host antigravity --project "/path/to/my app"
python scripts/install.py install --host opencode --project "/path/to/my app"
```

Codex and Antigravity share `.agents/skills/` in project scope, so install once
for both. `--host agents` also serves current OpenCode, Cursor, Gemini CLI and
Copilot versions that recognize this shared directory. Prefer one installation
to duplicate copies. See the [full path table](docs/compatibility.md).

For skills available across local projects on your machine:

```text
python scripts/install.py install --host codex --scope global
```

The installer copies files only. It does not configure agents, install
browsers, change permissions, choose a model, or start the Replica workflow.
It retains the MIT licence in every installed skill. Reload your agent's skills
or start a new session after installation.

### Start a skill

- **Codex:** `$replica-recon` followed by the target URL and scope.
- **Claude Code:** `/replica-recon` for a folder installation.
- **Antigravity, OpenCode, Cursor, Gemini CLI, Copilot:** ask the agent to
  `Use the replica-recon skill to map [URL] for [scope]`. Confirm it loads the
  skill. OpenCode uses its native skill tool; slash commands vary by host.
- **Other agents or ordinary chat:** follow [portable use](docs/portable.md).
  Load or paste a `SKILL.md` explicitly. Tool execution requires an environment
  with file and terminal access.

The `/replica-*` notation below is the original Claude invocation. Elsewhere,
use the same skill name through your host's loader, Codex's `$` invocation, or
an explicit file read. It is never a terminal command.

### Update and remove

After pulling updates in this checkout, rerun the same install command.
Preview changes with `--dry-run`. Updates and removals refuse to overwrite or
remove locally edited managed files; move or preserve those edits first.
Existing unmanaged skill folders are refused rather than adopted. User-added
files and unrelated skills are retained. A `.replica-install.json` checksum
manifest records ownership in the installation directory; keep it with the pack.
Each file is replaced atomically, but the full pack update is not a transaction;
keep a backup before updating an installation you have customized.

```text
python scripts/install.py install --host codex --project "/path/to/my app" --dry-run
python scripts/install.py uninstall --host codex --project "/path/to/my app"
```

Use the same host and scope for removal as for installation. Removing a shared
`.agents/skills/` pack removes that copy for every host that uses it. `replica/`
app outputs are never removed. Symbolic links and junctions in managed paths
are refused; choose an ordinary directory.

### Claude Code plugin

The original plugin interface remains available, now pointing at this fork:

```text
/plugin marketplace add Itskorrah/replica-skill-universal
/plugin install replica-skill@replica-skill
```

Plugin skills use `/replica-skill:replica-recon` and the corresponding names
for the other stages. Choose the plugin or a folder install, to avoid duplicates.
For manual installation on any host, copy the eleven complete `replica-*`
folders and the MIT licence into its documented skills directory.

## The eleven

| command | what it does |
| --- | --- |
| `/replica-recon` | Reverse-engineers any app: screens, flows, components, data model. From public pages, screenshots, store listings and your own account. |
| `/replica-architect` | Plans the stack, database schema and API for your clone. |
| `/replica-design` | Rebuilds the design system: colours, type, spacing, components. As tokens, with your own assets. |
| `/replica-build` | Rebuilds the app screen by screen from the recon map. |
| `/replica-backend` | Auth, database, payments and integrations. |
| `/replica-test` | Clicks through every flow and tests it for bugs. |
| `/replica-diff` | Compares your clone against the original. A parity score and what is missing. |
| `/replica-entrepreneur` | Reads what the app's users hate in real reviews and turns it into fixes and a positioning angle. |
| `/replica-brand` | Names and rebrands your version so it is yours. |
| `/replica-launch` | Landing page, pricing and App Store listing. |
| `/replica-deploy` | Ships it live on your own domain. |

## How to use it

Run them in order. Each one reads what the last one wrote, in a `replica/`
folder in your project.

```
recon -> architect -> design -> build -> backend -> test -> diff -> entrepreneur -> brand -> launch -> deploy
```

An example: cloning a scheduling app, the kind where you share a link and
people book a time with you.

1. **`/replica-recon`** with the app's URL. It reads the help center, the
   pricing page, the store listing and public walkthroughs, and you click
   through your own account with it. Out comes `replica/recon.md`: 18
   screens, 7 flows (guest books a meeting, host sets availability, guest
   reschedules...), the components, an inferred data model (users, event
   types, availability, bookings) and `features.csv`. The partner
   marketplace is marked out of scope: that is their network, not a feature.
2. **`/replica-architect`** picks Next.js, Postgres, Stripe and Resend, writes
   the schema (with a constraint so two guests can never book the same slot)
   and orders the build: the booking flow end to end first.
3. **`/replica-design`** measures the screenshots into tokens: colour roles,
   type scale, 8px spacing, the date picker and slot button specs. Open
   icons, an open font, your own words.
4. **`/replica-build`** builds the shell, then the booking flow, then every
   screen with all its states, ticking off `features.csv` as it goes.
5. **`/replica-backend`** adds sign up, Google Calendar through Google's own
   API with your keys, Stripe for paid bookings, reminder emails.
6. **`/replica-test`** writes a test plan from the 7 flows, Playwright specs
   for the happy paths and edge cases (time zones, a slot taken mid-booking,
   double submit), and logs bugs by severity until no S1 or S2 is open.
7. **`/replica-diff`** scores it. Features 86, all must-haves done, booking
   page layout 91. Missing: round-robin for teams, the website embed.
8. **`/replica-entrepreneur`** reads 140 real reviews across the App Store,
   G2, Capterra and Reddit. Top complaints: per-seat price jumps, no text
   reminders, guests confused by time zones. Each with counts and linked
   quotes. Fix plan: flat pricing, SMS reminders, a time zone confirm step.
   Angle: booking links for small teams that hate per-seat pricing.
9. **`/replica-brand`** names it (with the trademark and domain checks to
   run), gives it a new palette, a logo brief and a voice, then sweeps the
   codebase until nothing of the original is left.
10. **`/replica-launch`** writes the landing page around the angle, sets
    pricing against the original's public page, and lints the store listing.
11. **`/replica-deploy`** runs the preflight (tests, parity, sweep, listing),
    sets up production, gives you the DNS records for your domain, and ships
    it when you say go.

You can also run any one on its own. `/replica-entrepreneur` on an app you
are only thinking about cloning is a good way to find out if you should.

## The tools

Six of them, all standard-library Python. None touch the network.

The examples below run from this checkout. When running against your app,
keep its directory as the working directory and use quoted absolute paths to
the installed scripts, as each skill explains. That keeps `replica/` inputs
and outputs in your app. See [a Windows example](docs/portable.md).

```bash
python replica-diff/imgdiff.py original.png clone.png --out diff.png   # layout diff, ignores colour
python replica-diff/parity.py replica/features.csv                     # parity score + missing list
python replica-entrepreneur/reviews.py replica/reviews.csv             # what users hate, ranked, linked
python replica-design/contrast.py replica/design/tokens.json           # WCAG contrast on your tokens
python replica-brand/sweep.py . --avoid "Original App"                 # anything of the original left?
python replica-launch/listing.py replica/launch/listing.json           # store limits + copycat checks
```

**`imgdiff.py`** reads PNGs with no libraries, turns both screenshots into
edge maps and compares where things are, so your new colours do not count
against you. It tells you which regions differ, in the original's pixels.

**`parity.py`** weights must, should and could, counts partial as half, and
never scores what you left out on purpose or what you added. Missing
must-haves means not shippable, and it says so.

**`reviews.py`** drops every review without a link. Every quote it prints is
copied from a row you gave it, with that row's URL. Themes with under three
reviews or one source are marked thin.

**`sweep.py`** finds the original's name, domain and colours anywhere in your
code, including inside identifiers like `OriginalAppEmbed`, and blocks the
deploy until it is clean.

**`listing.py`** checks App Store and Google Play limits, ranking claims in
the title, wasted keyword characters, and the original's name anywhere in
your listing.

```bash
python -m unittest discover -s tests -v
```

## Fine print

**It rebuilds functionality and UX patterns, clean-room style.** It studies
what the app does and how people move through it, then writes everything
fresh. It never copies the target's source code, proprietary assets, logos,
trademarks, copy or private APIs.

**It only reads what you are allowed to read.** Public pages and your own
account. It never scrapes behind a login or against a site's terms, never
logs into anyone else's account, and never gets past a paywall. If your
account's terms forbid using it to build a competitor, it says so and sticks
to public sources.

**It always rebrands before launch.** New name, new palette, new logo, new
words. `/replica-deploy` will not ship until the sweep is clean.

**"Clone any app" means the features and the flow.** Not the content, the
network or the licences an app owns. You can rebuild a music app's player,
playlists and sharing. You cannot clone its catalogue.

**No guarantee of a "perfect" clone.** Results depend on how complex the app
is. A booking tool is weeks. A spreadsheet engine is not. `/replica-recon`
sizes it honestly before you start, and `/replica-diff` gives you a real
number, not a vibe.

**The Entrepreneur never makes things up.** No invented reviews, quotes or
numbers. Every claim has a link, and the sample size is stated.

**Check before you sell.** Run the trademark checks `/replica-brand` lists,
read the terms of anything you used, and talk to a lawyer before launch if
there is money on the line. This is not legal advice.

## Files

```
replica-recon/         SKILL.md, recon-map.md, features.csv (the matrix template)
replica-architect/     SKILL.md, architecture.md
replica-design/        SKILL.md, tokens.json, contrast.py
replica-build/         SKILL.md
replica-backend/       SKILL.md
replica-test/          SKILL.md, test-plan.md, bug-report.md, e2e.example.spec.ts
replica-diff/          SKILL.md, imgdiff.py, parity.py
replica-entrepreneur/  SKILL.md, reviews.py, themes.json
replica-brand/         SKILL.md, sweep.py
replica-launch/        SKILL.md, listing.py, listing.example.json
replica-deploy/        SKILL.md, preflight.md
scripts/install.py     cross-platform install, update and removal
docs/                  compatibility evidence and portable use
tests/                 tool, installation and integration tests
.github/workflows/     Linux, Windows and macOS CI
```

Your own files live in `replica/` in your project. The skills read each
other's.

## Credit

Original Replica skill pack by Jake Schincariol, [opusjake.ai](https://opusjake.ai),
from the [upstream repository](https://github.com/Jakeschincariol/replica-skill).
Universal compatibility maintained in
[Itskorrah/replica-skill-universal](https://github.com/Itskorrah/replica-skill-universal).

Other skills by the original author:
[Arena](https://github.com/Jakeschincariol/arena-skill),
[X](https://github.com/Jakeschincariol/x-agent-skill),
[LinkedIn](https://github.com/Jakeschincariol/linkedin-agent-skill),
[Instagram](https://github.com/Jakeschincariol/instagram-agent-skill).

## License

MIT. Take it, change it, ship it.
