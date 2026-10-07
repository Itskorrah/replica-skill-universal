# Use Replica with any agent

An agent that can read Markdown can follow the Replica method. Native skill
discovery is optional. Executing tools needs file and terminal access; live
research and screenshots need web/browser access or user-provided evidence.

## Agent with local files

Keep this checkout available, or install a portable copy:

```text
python scripts/install.py install --host portable --project "/path/to/my app"
```

In the agent working on your app, paste this prompt and substitute your paths:

```text
Use replica-recon from /absolute/path/to/.replica-skills/replica-recon/SKILL.md.
Read that file before starting. The pack root is /absolute/path/to/.replica-skills.
My app project is /absolute/path/to/my-app; keep all replica/ outputs there.
The target is [URL], platform [web/iOS/Android/desktop], scope [features].
Follow the skill's rules. Use your available tools and report anything you cannot
inspect or execute. When another Replica skill is needed within this request,
read its sibling SKILL.md. Do not deploy without my go-ahead.
```

For the source checkout, the pack root is the checkout directory itself.
Substitute it for `.replica-skills` in the prompt. This is also how to use the
pack with editors that support Markdown instructions but do not discover skills.

Each skill explains `<PACK_ROOT>`: the absolute directory containing all eleven
skill folders. It is a placeholder to replace before executing an example,
not an environment variable. Keep the app project as the working directory.
For example, a PowerShell command after installing into a Windows project is:

```powershell
python "C:/work/My App/.replica-skills/replica-diff/parity.py" replica/features.csv
```

Use `python3` on systems where that is the Python 3 command, or `py -3` on
Windows if appropriate. Forward slashes work in Python paths on Windows.

## Chat without local files

Paste the selected `SKILL.md` into the chat and provide the relevant templates
and inputs. Include previous stage outputs when continuing in another chat.
The assistant can draft the recon, architecture or other documents, but cannot
claim it saved files or ran tools if it has no environment to do so. Run the
listed Python commands locally and provide their results for later stages.

The original clean-room rules, real-source requirements, rebranding checks and
deployment approval still apply. A new chat, a different model, or changing
agents does not itself authorize deployment.

## Continue in a different agent

Open the same app project, load the requested skill, and read its existing
`replica/` inputs. Recon screen IDs, the feature matrix, build log, bug reports,
parity report and deployment checklist remain ordinary project files. There is
no private Claude session state required by Replica. Have one agent write these
shared files at a time, or coordinate changes through Git.
