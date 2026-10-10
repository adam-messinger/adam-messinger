# Simplify provenance

The shared `simplify` skill is adapted from Anthropic's published `code-simplifier` agent in the official `anthropics/claude-plugins-official` repository. It is distinct from Claude Code's bundled `/simplify` command.

- Upstream repository: <https://github.com/anthropics/claude-plugins-official>
- Verified immutable revision: `b8e53f1c05dff3b6d751297f6527990ffc81c2f4`
- Source prompt: <https://github.com/anthropics/claude-plugins-official/blob/b8e53f1c05dff3b6d751297f6527990ffc81c2f4/plugins/code-simplifier/agents/code-simplifier.md>
- Source prompt Git blob: `05e361b4ef1b688203251989707f8a924a9ed266`
- Plugin metadata, naming the author as Anthropic: <https://github.com/anthropics/claude-plugins-official/blob/b8e53f1c05dff3b6d751297f6527990ffc81c2f4/plugins/code-simplifier/.claude-plugin/plugin.json>
- Applicable upstream license: Apache License, Version 2.0, included verbatim in [LICENSE](LICENSE), from <https://github.com/anthropics/claude-plugins-official/blob/b8e53f1c05dff3b6d751297f6527990ffc81c2f4/plugins/code-simplifier/LICENSE>
- License Git blob: `d645695673349e3947e8e5ae42332d0ac3164cd7` (the repository root LICENSE has the same blob).
- Verification date: 2026-10-10. The complete recursive repository tree at this revision contained no root or code-simplifier `NOTICE` file. The prompt contains no separate copyright notice. No copyright year or additional upstream notice has been invented.

The adapted file prominently identifies that it was modified. Its changes remove the provider-specific `model: opus` declaration and blanket JavaScript/React style preferences; use repository instructions and available host capabilities; broaden cleanup to supported reuse and efficiency improvements; review the complete supplied PR/diff; support report-only mode; and require meaningful validation. The local earlier simplify skill supplied additional cleanup considerations but is not a runtime dependency.

Apache-2.0 redistribution requires recipients to receive a copy of the license, modified files to identify their changes, and relevant upstream copyright, patent, trademark, and attribution notices to be retained. A relevant upstream NOTICE must also be retained when one exists. Keep this attribution and LICENSE with the skill in every installed copy. This attribution does not imply Anthropic endorsement.
