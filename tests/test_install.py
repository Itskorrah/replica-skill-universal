"""Exercise real installations and tools in isolated projects and home folders."""

import contextlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from _load import load, ROOT

installer = load("scripts", "install")


class Install(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="replica test ")
        # macOS /var is a system symlink; exercise an ordinary canonical path.
        self.base = Path(self.temp.name).resolve()
        self.project = self.base / "app project"
        self.project.mkdir()
        self.dest = self.project / ".agents/skills"

    def tearDown(self):
        self.temp.cleanup()

    def snapshot(self):
        return {p.relative_to(self.project).as_posix(): p.read_bytes()
                for p in self.project.rglob("*") if p.is_file()}

    def test_every_host_project_and_global_bundle(self):
        expected = {
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
        for host, locations in expected.items():
            for index, scope in enumerate(("project", "global")):
                with self.subTest(host=host, scope=scope):
                    project = self.base / host / "app"
                    home = self.base / host / "home"
                    dest = installer.destination(host, scope, project, home=home)
                    self.assertEqual(dest, (project if index == 0 else home) / locations[index])
                    installer.install(dest)
                    for skill in installer.SKILLS:
                        self.assertEqual((dest / skill / "SKILL.md").read_bytes(),
                                         (Path(ROOT) / skill / "SKILL.md").read_bytes())
                        self.assertEqual((dest / skill / "LICENSE").read_bytes(),
                                         (Path(ROOT) / "LICENSE").read_bytes())
                    self.assertTrue((dest / "replica-entrepreneur/themes.json").is_file())
                    self.assertTrue((dest / "replica-test/e2e.example.spec.ts").is_file())

    def test_dry_run_does_not_create_destination(self):
        self.assertGreater(installer.install(self.dest, dry_run=True), 11)
        self.assertFalse(self.dest.exists())

    def test_reinstall_is_idempotent_and_shared_between_agents(self):
        installer.install(self.dest)
        before = self.snapshot()
        same = installer.destination("antigravity", "project", self.project)
        installer.install(same)
        self.assertEqual(before, self.snapshot())

    def test_refuses_unmanaged_skill_before_any_writes(self):
        folder = self.dest / "replica-launch"
        folder.mkdir(parents=True)
        (folder / "SKILL.md").write_text("mine", encoding="utf-8")
        before = self.snapshot()
        with self.assertRaisesRegex(installer.InstallError, "Unmanaged skill"):
            installer.install(self.dest)
        self.assertEqual(before, self.snapshot())

    def test_modified_managed_file_blocks_update_and_uninstall(self):
        installer.install(self.dest)
        (self.dest / "replica-build/SKILL.md").write_text("my edit", encoding="utf-8")
        before = self.snapshot()
        for action in (installer.install, installer.uninstall):
            with self.assertRaisesRegex(installer.InstallError, "Locally modified"):
                action(self.dest)
            self.assertEqual(before, self.snapshot())

    def test_update_and_remove_only_owned_files(self):
        installer.install(self.dest)
        added = self.dest / "replica-build/my-notes.md"
        added.write_text("keep me", encoding="utf-8")
        unrelated = self.dest / "other-skill/SKILL.md"
        unrelated.parent.mkdir()
        unrelated.write_text("also keep", encoding="utf-8")
        source = self.base / "new source"
        source.mkdir()
        shutil.copy2(Path(ROOT) / "LICENSE", source / "LICENSE")
        for skill in installer.SKILLS:
            shutil.copytree(Path(ROOT) / skill, source / skill,
                            ignore=shutil.ignore_patterns("__pycache__"))
        changed = source / "replica-build/SKILL.md"
        changed.write_text(changed.read_text(encoding="utf-8") + "\nUpdated.\n", encoding="utf-8")
        (source / "replica-recon/features.csv").unlink()
        installer.install(self.dest, source=source)
        self.assertIn("Updated.", (self.dest / "replica-build/SKILL.md").read_text(encoding="utf-8"))
        self.assertFalse((self.dest / "replica-recon/features.csv").exists())
        before = self.snapshot()
        installer.uninstall(self.dest, dry_run=True)
        self.assertEqual(before, self.snapshot())
        installer.uninstall(self.dest)
        self.assertEqual(added.read_text(encoding="utf-8"), "keep me")
        self.assertEqual(unrelated.read_text(encoding="utf-8"), "also keep")
        self.assertFalse((self.dest / installer.MANIFEST).exists())
        self.assertFalse((self.dest / "replica-recon").exists())

    def test_missing_managed_files_can_be_repaired(self):
        installer.install(self.dest)
        path = self.dest / "replica-design/contrast.py"
        path.unlink()
        installer.install(self.dest)
        self.assertTrue(path.is_file())

    def test_new_source_file_cannot_overwrite_user_addition(self):
        installer.install(self.dest)
        source = self.base / "source"
        source.mkdir()
        shutil.copy2(Path(ROOT) / "LICENSE", source / "LICENSE")
        for skill in installer.SKILLS:
            shutil.copytree(Path(ROOT) / skill, source / skill,
                            ignore=shutil.ignore_patterns("__pycache__"))
        (source / "replica-build/new.md").write_text("upstream", encoding="utf-8")
        (self.dest / "replica-build/new.md").write_text("local", encoding="utf-8")
        before = self.snapshot()
        with self.assertRaisesRegex(installer.InstallError, "Unmanaged file"):
            installer.install(self.dest, source=source)
        self.assertEqual(before, self.snapshot())

    def test_manifest_cannot_escape_destination(self):
        self.dest.mkdir(parents=True)
        outside = self.project / "keep.txt"
        outside.write_text("keep", encoding="utf-8")
        for key in ("../keep.txt", "replica-build/../../keep.txt",
                    "/replica-build/x", "replica-build\\..\\keep.txt",
                    "replica-build/x:stream", "replica-build//x"):
            record = {"package": installer.PACKAGE, "schema": 1,
                      "files": {key: "0" * 64}}
            (self.dest / installer.MANIFEST).write_text(json.dumps(record), encoding="utf-8")
            with self.assertRaises(installer.InstallError):
                installer.uninstall(self.dest)
            self.assertEqual(outside.read_text(encoding="utf-8"), "keep")

    def test_invalid_manifest_does_not_get_adopted(self):
        self.dest.mkdir(parents=True)
        manifest = self.dest / installer.MANIFEST
        for content in ("not json", "[]", '{}', '{"package":"other","schema":1,"files":{}}'):
            manifest.write_text(content, encoding="utf-8")
            before = self.snapshot()
            with self.assertRaises(installer.InstallError):
                installer.install(self.dest)
            self.assertEqual(before, self.snapshot())

    def test_symlink_target_is_rejected(self):
        outside = self.base / "outside"
        outside.mkdir()
        try:
            (self.project / ".agents").symlink_to(outside, target_is_directory=True)
        except OSError:
            self.skipTest("Host does not permit symlink creation")
        with self.assertRaisesRegex(installer.InstallError, "symbolic link"):
            installer.destination("codex", "project", self.project)
        self.assertEqual(list(outside.iterdir()), [])

    def test_cli_runs_from_outside_checkout(self):
        result = subprocess.run([sys.executable, str(Path(ROOT) / "scripts/install.py"),
                                 "install", "--host", "codex", "--project", str(self.project)],
                                cwd=str(self.base), capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.dest / "replica-recon/SKILL.md").is_file())
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(installer.main(["uninstall", "--host", "codex",
                                             "--project", str(self.base / "absent")]), 1)

    def test_all_six_installed_tools_run_in_separate_app(self):
        installer.install(self.dest)
        out = self.project / "replica"
        out.mkdir()
        (out / "features.csv").write_text(
            "feature,area,priority,original,clone,notes\nBook,booking,must,yes,yes,\n",
            encoding="utf-8")
        shutil.copy2(self.dest / "replica-design/tokens.json", out / "tokens.json")
        shutil.copy2(self.dest / "replica-launch/listing.example.json", out / "listing.json")
        (out / "reviews.csv").write_text(
            'source,url,date,rating,text\nStore,https://example.com/review,2026-10-01,2,"Too expensive"\n',
            encoding="utf-8")
        (out / "brand.json").write_text('{"avoid":["Original App"]}', encoding="utf-8")
        imgdiff = load("replica-diff", "imgdiff")
        imgdiff.write_png(str(out / "a.png"), 8, 8,
                          [[(255, 255, 255)] * 8 for _ in range(8)])
        commands = [
            ("replica-diff/parity.py", ["replica/features.csv", "--json"], {0}),
            ("replica-diff/imgdiff.py", ["replica/a.png", "replica/a.png", "--json"], {0}),
            ("replica-design/contrast.py", ["replica/tokens.json", "--json"], {0}),
            ("replica-brand/sweep.py", [".", "--config", "replica/brand.json"], {0}),
            ("replica-launch/listing.py", ["replica/listing.json", "--json"], {0}),
            ("replica-entrepreneur/reviews.py", ["replica/reviews.csv", "--out", "replica/feedback.md"], {0}),
        ]
        for script, args, codes in commands:
            with self.subTest(script=script):
                result = subprocess.run([sys.executable, str(self.dest / script)] + args,
                                        cwd=str(self.project), capture_output=True, text=True)
                self.assertIn(result.returncode, codes, result.stdout + result.stderr)
        self.assertIn("Too expensive", (out / "feedback.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
