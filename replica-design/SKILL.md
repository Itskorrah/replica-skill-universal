---
name: replica-design
description: >-
  Rebuilds an app's design system for a clone: colour roles, type scale,
  spacing, radius, shadows and every component with its states, as design
  tokens plus component specs, with original assets instead of the target's
  logos, icons, illustrations or licensed fonts. Includes a WCAG contrast
  checker. Use when the user says "match the design", "rebuild the design
  system", "get the colours and fonts", "make it look like X", "design tokens
  for my clone", or after /replica-architect.
---

# replica-design

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

Reads `replica/recon.md` and the screenshots in `replica/screens/`. Writes
`replica/design/tokens.json` (template in this folder), `tokens.css`, the
Tailwind mapping, and `replica/design/components.md`.

```bash
python "<PACK_ROOT>/replica-design/contrast.py" replica/design/tokens.json     # every text pair, WCAG ratio
```

## The rules

What you rebuild is the **system**: the roles, the scale, the patterns, the
way a form or a modal behaves. Those are not ownable, and users expect them.
What you never take:

- **Logos, icons, illustrations, photos, sounds.** Use an open icon set
  (Lucide, Phosphor, Heroicons, Tabler, all MIT or similar) and make or
  commission your own illustrations. Do not trace theirs.
- **Licensed fonts.** If the original uses a paid or proprietary font, pick
  an open one with the same job: Inter, Geist, IBM Plex, Manrope, Source Serif.
- **Their copy.** Every label and empty state gets written fresh.
- **Their brand colour.** Record it as a role (`accent`), use a neutral
  placeholder now, and replica-brand gives you your own. The signature colour
  plus the signature layout is trade dress, and it changes before launch.

## Step 1: measure, do not guess

From the screenshots (zoom in, use a colour picker on the user's machine):

- **Colour roles**, not colours: bg, surface, border, border-input, text,
  text-muted, accent, on-accent, danger, success, warning. Count how many
  greys the app really uses. Usually 5 to 7.
- **Type scale**: sizes, line heights, weights. Snap to a scale (12, 14, 16,
  20, 28, 40 is common). Note the font category, not the font file.
- **Spacing**: measure gaps between elements. It is almost always a 4 or 8
  base. Write the scale.
- **Radius, shadow, motion**: two or three of each.
- **Layout**: max content width, grid, breakpoints, sidebar width, header height.

## Step 2: write the tokens

Fill `tokens.json`. Keep the role names. replica-brand only changes values.
Generate `tokens.css` as custom properties and map them into Tailwind's theme
so components use `bg-surface text-muted`, never raw hex.

Add a `pairs` list for every text and background combination the app uses,
then:

```bash
python "<PACK_ROOT>/replica-design/contrast.py" replica/design/tokens.json
```

AA is the floor: 4.5:1 for body text, 3:1 for large text and for input
borders and focus rings. It exits 1 on a failure. Fix it in the tokens, not
per component.

## Step 3: component specs

For every component in the recon list, one block in `components.md`:

```
Button
  variants  primary, secondary, ghost, danger
  sizes     sm 32px, md 40px, lg 48px
  states    default, hover, active, focus-visible (2px ring, accent), disabled, loading
  tokens    bg accent, text on-accent, radius md, font sm/600
  a11y      real <button>, visible focus, loading keeps the label for screen readers
  used on   S02, S07, S09
```

Every state the recon saw, plus the ones it should have: focus, disabled,
loading, error, empty. Keyboard and screen reader behaviour is part of the
spec.

## Step 4: build the primitives

Build the components in code once, in isolation (a `/design` route or
Storybook), before any screen. Use an accessible base if the stack has one
(Radix, shadcn/ui, React Aria). Screenshot the page. That is the design system
check.

## Output

`tokens.json`, `tokens.css`, the Tailwind config, `components.md`, the
primitives built, and a contrast report with zero AA failures. Next:
`/replica-build`.
