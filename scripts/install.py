#!/usr/bin/env python3
"""Install the complete Replica skill pack without overwriting user-owned files.

Python 3.8+, standard library only. No network access or host configuration edits.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import sys

ROOT = Path(__file__).resolve().parent.parent
SKILLS = (
    "replica-recon", "replica-architect", "replica-design", "replica-build",
    "replica-backend", "replica-test", "replica-diff", "replica-entrepreneur",
    "replica-brand", "replica-launch", "replica-deploy",
)
# (project location, home-relative global location)
HOSTS = {
    "agents": (".agents/skills", ".agents/skills"),
    "codex": (".agents/skills", ".agents/skills"),
    "claude": (".claude/skills", ".claude/skills"),
    "antigravity": (".agents/skills", ".gemini/config/skills"),
    "antigravity-cli": (".agents/skills", ".gemini/antigravity-cli/skills"),
    "opencode": (".opencode/skills", ".config/opencode/skills"),
    "cursor": (".cursor/skills", ".cursor/skills"),
    "gemini": (".gemini/skills", ".gemini/skills"),
    "copilot": (".github/skills", ".copilot/skills"),
    "portable": (".replica-skills", ".replica-skills"),
}
MANIFEST = ".replica-install.json"
PACKAGE = "Itskorrah/replica-skill-universal"


class InstallError(Exception):
    pass


def digest(data):
    return hashlib.sha256(data).hexdigest()


def no_links(path):
    """Check before resolving: a link must never redirect an install or removal."""
    for part in (path,) + tuple(path.parents):
        if part.is_symlink():
            raise InstallError("Refusing symbolic link: %s" % part)
        if part.exists():
            attrs = getattr(part.lstat(), "st_file_attributes", 0)
            if attrs & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0):
                raise InstallError("Refusing junction/reparse point: %s" % part)


def destination(host, scope, project, home=None):
    base = Path(project) if scope == "project" else Path(home or Path.home())
    location = HOSTS[host][0 if scope == "project" else 1]
    path = Path(os.path.abspath(str(base.expanduser() / location)))
    no_links(path)
    return path


def payload(source=ROOT):
    files = {}
    for skill in SKILLS:
        folder = source / skill
        if not (folder / "SKILL.md").is_file():
            raise InstallError("Missing source skill: %s" % folder)
        for path in sorted(folder.rglob("*")):
            if "__pycache__" in path.parts or path.suffix == ".pyc":
                continue
            no_links(path)
            if path.is_file():
                files[path.relative_to(source).as_posix()] = path.read_bytes()
        # Each installed bundle retains the original MIT attribution.
        files[skill + "/LICENSE"] = (source / "LICENSE").read_bytes()
    return files


def safe_key(key):
    if not isinstance(key, str):
        raise InstallError("Invalid manifest path")
    parts = PurePosixPath(key).parts
    if (len(parts) < 2 or parts[0] not in SKILLS or ".." in parts
            or "\\" in key or ":" in key or PurePosixPath(key).as_posix() != key):
        raise InstallError("Invalid manifest path: %s" % key)
    return key


def read_manifest(dest):
    path = dest / MANIFEST
    no_links(path)
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if data["package"] != PACKAGE or data["schema"] != 1:
            raise ValueError("wrong package or schema")
        files = data["files"]
        if not isinstance(files, dict) or not files:
            raise ValueError("files must be a nonempty mapping")
        for key, sha in files.items():
            safe_key(key)
            if (not isinstance(sha, str) or len(sha) != 64
                    or any(c not in "0123456789abcdef" for c in sha)):
                raise ValueError("invalid checksum")
        return files
    except (ValueError, KeyError, TypeError) as exc:
        raise InstallError("Invalid install manifest: %s" % exc)


def preflight(dest, old, new):
    """Validate the entire plan before changing any file."""
    no_links(dest)
    if dest.exists() and not dest.is_dir():
        raise InstallError("Destination is not a directory: %s" % dest)
    owned = {PurePosixPath(key).parts[0] for key in old}
    for skill in SKILLS:
        folder = dest / skill
        no_links(folder)
        if folder.exists() and skill not in owned:
            raise InstallError("Unmanaged skill already exists: %s" % folder)
        if folder.exists() and not folder.is_dir():
            raise InstallError("Skill path is not a directory: %s" % folder)
    for key in sorted(set(old) | set(new)):
        path = dest / safe_key(key)
        no_links(path)
        for parent in path.parents:
            if parent == dest:
                break
            if parent.exists() and not parent.is_dir():
                raise InstallError("Parent is not a directory: %s" % parent)
        if path.exists():
            if not path.is_file():
                raise InstallError("Expected a file: %s" % path)
            if key not in old:
                raise InstallError("Unmanaged file already exists: %s" % path)
            if digest(path.read_bytes()) != old[key]:
                raise InstallError("Locally modified file; preserve or move it first: %s" % path)


def atomic_write(path, data):
    """Replace one file atomically; never leave a half-written manifest."""
    import tempfile
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=".replica-", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
        os.replace(temp, str(path))
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def prune_empty(dest, keys):
    parents = {parent for key in keys for parent in (dest / key).parents
               if parent != dest and dest in parent.parents}
    for path in sorted(parents, key=lambda p: len(p.parts), reverse=True):
        # No recursive removal: user-added files and containing config survive.
        if path.exists() and not any(path.iterdir()):
            path.rmdir()


def install(dest, source=ROOT, dry_run=False):
    files = payload(source)
    old = read_manifest(dest)
    preflight(dest, old, files)
    if dry_run:
        return len(files)
    for key, data in files.items():
        atomic_write(dest / key, data)
    removed = set(old) - set(files)
    for key in removed:
        path = dest / key
        if path.exists():
            path.unlink()
    prune_empty(dest, removed)
    record = {"schema": 1, "package": PACKAGE,
              "files": {key: digest(data) for key, data in sorted(files.items())}}
    atomic_write(dest / MANIFEST, (json.dumps(record, indent=2) + "\n").encode("utf-8"))
    return len(files)


def uninstall(dest, dry_run=False):
    old = read_manifest(dest)
    if not old:
        raise InstallError("No managed Replica installation at %s" % dest)
    preflight(dest, old, {})
    if not dry_run:
        for key in old:
            path = dest / key
            if path.exists():
                path.unlink()
        prune_empty(dest, old)
        (dest / MANIFEST).unlink()
    return len(old)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("install", "uninstall"))
    parser.add_argument("--host", choices=sorted(HOSTS), required=True)
    parser.add_argument("--scope", choices=("project", "global"), default="project")
    parser.add_argument("--project", default=".", help="target project (default: current directory)")
    parser.add_argument("--dry-run", action="store_true", help="check and print the plan without writing")
    args = parser.parse_args(argv)
    if args.scope == "global" and args.project != ".":
        parser.error("--project applies only to --scope project")
    try:
        dest = destination(args.host, args.scope, args.project)
        if args.action == "install":
            count = install(dest, dry_run=args.dry_run)
        else:
            count = uninstall(dest, dry_run=args.dry_run)
    except (InstallError, OSError) as exc:
        print("replica: %s" % exc, file=sys.stderr)
        return 1
    print("%s%s: %d files at %s" % (
        "Would " if args.dry_run else "", args.action, count, dest))
    if args.action == "install":
        print("Open/reload the target agent, then ask it to use replica-recon.")
        if args.host == "portable":
            print("Load %s/replica-recon/SKILL.md explicitly; this path has no native discovery." % dest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
