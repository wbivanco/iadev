from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from aidev.codex import ROLE_SKILLS, setup_codex, skill_for_role
from aidev.core import OrchestratorError


def make_root(path: Path) -> Path:
    system = path / "ai-system"
    (system / "targets" / "codex").mkdir(parents=True)
    (system / "targets" / "codex" / "AGENTS.md.template").write_text("Reglas IADev", encoding="utf-8")
    (system / "guidance" / "skills").mkdir(parents=True)
    for source in ("planning.md", "implementation.md", "review.md", "closeout.md", "coordinator.md", "visual-design.md", "smart-commit.md"):
        (system / "guidance" / "skills" / source).write_text(f"# {source}\n\nInstrucciones", encoding="utf-8")
    return path


class CodexSetupTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = make_root(Path(self.temporary.name))

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_setup_generates_skills_and_preserves_existing_guidance(self) -> None:
        workspace = self.root / "workspace"
        workspace.mkdir()
        guidance = workspace / "AGENTS.md"
        guidance.write_text("# Reglas existentes\n", encoding="utf-8")
        result = setup_codex(self.root)
        self.assertEqual(len(result.created), 7)
        self.assertEqual(len(result.updated), 1)
        content = guidance.read_text(encoding="utf-8")
        self.assertIn("Reglas existentes", content)
        self.assertIn("<!-- aidev:codex:start -->", content)
        skill = workspace / ".agents" / "skills" / "aidev-planning" / "SKILL.md"
        self.assertIn("name: aidev-planning", skill.read_text(encoding="utf-8"))

    def test_setup_refreshes_only_its_guidance_block(self) -> None:
        workspace = self.root / "workspace"
        workspace.mkdir()
        guidance = workspace / "AGENTS.md"
        guidance.write_text("# Reglas existentes\n", encoding="utf-8")
        setup_codex(self.root)
        guidance.write_text(guidance.read_text(encoding="utf-8") + "\n# Regla posterior\n", encoding="utf-8")
        setup_codex(self.root)
        content = guidance.read_text(encoding="utf-8")
        self.assertEqual(content.count("<!-- aidev:codex:start -->"), 1)
        self.assertIn("# Reglas existentes", content)
        self.assertIn("# Regla posterior", content)

    def test_setup_protects_modified_skill_unless_forced(self) -> None:
        setup_codex(self.root)
        skill = self.root / "workspace" / ".agents" / "skills" / "aidev-planning" / "SKILL.md"
        skill.write_text(skill.read_text(encoding="utf-8") + "\nCambio manual\n", encoding="utf-8")
        with self.assertRaisesRegex(OrchestratorError, "--force"):
            setup_codex(self.root)
        setup_codex(self.root, force=True)
        self.assertNotIn("Cambio manual", skill.read_text(encoding="utf-8"))

    def test_setup_rejects_an_empty_canonical_skill(self) -> None:
        skill = self.root / "ai-system" / "guidance" / "skills" / "smart-commit.md"
        skill.write_text("", encoding="utf-8")

        with self.assertRaisesRegex(OrchestratorError, "está vacío"):
            setup_codex(self.root)

    def test_roles_have_explicit_skills(self) -> None:
        for role, skill in ROLE_SKILLS.items():
            self.assertEqual(skill_for_role(role), skill)
        self.assertIsNone(skill_for_role("unknown"))


if __name__ == "__main__":
    unittest.main()
