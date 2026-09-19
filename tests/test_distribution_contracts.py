import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DistributionContractsTest(unittest.TestCase):
    def test_package_version_is_patch_release(self):
        manifest = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        self.assertEqual(manifest["version"], "1.0.1")

    def test_consumer_dispatch_uses_registry_without_legacy_host_repos(self):
        workflow = (ROOT / ".github/workflows/notify-consumers.yml").read_text()
        self.assertIn("docs/CONSUMERS.md", workflow)
        self.assertNotRegex(workflow, r"partme-ai/codex-[a-z-]+-plugin")

        consumers = (ROOT / "docs/CONSUMERS.md").read_text().splitlines()
        repos = [line for line in consumers if re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", line)]
        self.assertIn("full-stack-plugins/stitch-design-plugin", repos)
        self.assertIn("full-aigc-plugins/image-factory-plugin", repos)

    def test_release_template_never_moves_published_tag(self):
        workflow = (ROOT / "workflows/release-tag.yml").read_text()
        self.assertNotIn("git push --force", workflow)
        self.assertIn("immutable tag", workflow)
        self.assertIn("gh release create", workflow)

    def test_sync_template_fetches_branch_and_does_not_require_label(self):
        workflow = (ROOT / "workflows/skill-sync.yml").read_text()
        self.assertIn("git fetch origin refs/heads/chore/skills-sync", workflow)
        self.assertNotIn("--label", workflow)

    def test_public_overview_has_no_legacy_repository_identity(self):
        overview = (ROOT / "skills/toolchain-overview/SKILL.md").read_text()
        self.assertNotIn("codex-stitch-plugin", overview)
        self.assertIn("stitch-design-plugin/scripts/vendor/skill_vendor.py", overview)


if __name__ == "__main__":
    unittest.main()
