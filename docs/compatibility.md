# Compatibility and verification

Replica uses ordinary Agent Skills folders: YAML `name` and `description`,
Markdown instructions, adjacent templates and standard-library Python tools.
The model is selected by your coding agent. Replica does not call a model API.

## Installer profiles

Paths are relative to the app project for project scope and the user home
directory for global scope. The installer uses the operating system's home
directory on Windows, macOS and Linux. Run it with Python 3.8 or newer.

| `--host` | Project location | Global location |
| --- | --- | --- |
| `agents` | `.agents/skills/` | `~/.agents/skills/` |
| `codex` | `.agents/skills/` | `~/.agents/skills/` |
| `claude` | `.claude/skills/` | `~/.claude/skills/` |
| `antigravity` (IDE) | `.agents/skills/` | `~/.gemini/config/skills/` |
| `antigravity-cli` | `.agents/skills/` | `~/.gemini/antigravity-cli/skills/` |
| `opencode` | `.opencode/skills/` | `~/.config/opencode/skills/` |
| `cursor` | `.cursor/skills/` | `~/.cursor/skills/` |
| `gemini` (CLI) | `.gemini/skills/` | `~/.gemini/skills/` |
| `copilot` | `.github/skills/` | `~/.copilot/skills/` |
| `portable` | `.replica-skills/` | `~/.replica-skills/` |

Codex and Antigravity use the same project directory. Install once there.
Current OpenCode, Cursor, Gemini CLI and Copilot also recognize `.agents/skills`;
`--host agents` offers one shared installation. Avoid installing duplicate
copies in multiple discovery directories. Global Antigravity IDE and CLI
locations differ, so choose the matching profile.

OpenCode's global profile follows its documented `~/.config/opencode/skills`
location. If your host uses a custom configuration directory, manually copy
the eleven complete skill folders there instead. Do not copy only `SKILL.md`:
the neighbouring scripts and templates are part of the pack.

`portable` supplies files for explicit loading; it does not register commands
with a host. No installer action edits `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`,
host settings, permissions or API keys. Project outputs stay in `replica/`.

## Invocation

| Host | How to start |
| --- | --- |
| Codex | `$replica-recon` with the target app and scope |
| Claude Code, folder install | `/replica-recon` |
| Claude Code, plugin install | `/replica-skill:replica-recon` |
| Antigravity IDE | Ask: `Use replica-recon to map this app...`; inspect Customizations |
| Antigravity CLI | Ask for the skill by name, or use its generated `/replica-recon` command |
| OpenCode | Ask: `Load the replica-recon skill and map this app...`; uses the native `skill` tool |
| Cursor / Gemini CLI / Copilot | Ask the agent to use `replica-recon`; verify it loads the skill |
| Other agents / ordinary chat | Explicitly load or paste the skill, following [portable use](portable.md) |

Reload skills or open a fresh session after installing. Discovery can depend
on host version, workspace trust and permissions. If the host cannot discover
the skill, explicitly load its file; do not assume that a slash command exists.

## Evidence and limits

- Automated checks install all eleven skills and their resources into isolated
  project and global locations for every profile. They exercise reinstall,
  update, removal, conflicting files, invalid manifests and separate app paths.
- An integration test executes all six installed Python tools from a separate
  app project, including a pack location with spaces.
- Existing scoring, PNG diff, review, contrast and listing tests remain. The
  brand sweep excludes root skill installation directories while still checking
  app source and GitHub workflows. Agent metadata must not be shipped as public
  app assets. Nested public copies are still checked.
- CI runs the complete suite on Linux, Windows and macOS with Python 3.13,
  plus Python 3.8 on Linux and Windows. See the current [Actions results](https://github.com/Itskorrah/replica-skill-universal/actions).
- **Live agent sessions are pending verification** for the installer profiles.
  Filesystem and subprocess tests do not prove discovery, model behaviour,
  browser access, or successful production deployment in each host. Claude's
  plugin manifests are retained and checked structurally; plugin installation
  in a signed-in Claude session is also pending.
- A host needs file and terminal access to execute tools, and web/browser access
  to observe live apps. Without those, provide explicit manual steps and mark
  the missing evidence. Chat-only use supports the method, not tool execution.

## Host documentation

Locations and invocation guidance were checked on 7 October 2026. Host releases
can change these conventions; use their documentation when troubleshooting.

- [Codex skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Antigravity skills, IDE and CLI](https://antigravity.google/docs/skills)
- [OpenCode skills](https://opencode.ai/docs/skills/)
- [Cursor skills](https://cursor.com/docs/skills)
- [Gemini CLI skills](https://geminicli.com/docs/cli/skills/)
- [Copilot skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)
