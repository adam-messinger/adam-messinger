# Shared skill source

Author the three developer skills under `skills/` once. Consumer copies are
generated from an immutable commit; update this source rather than editing copies.
Keep provider-specific tools/model declarations out of portable workflow text.
Repository requirements and narrower user instructions take precedence.

Changing or installing these skills never invokes their delivery/backlog workflows.
Use inert fixtures and independent read-only simulations. Do not close real issues,
execute backlog tasks, or use production writes to validate skill installation.

Retain simplify's upstream attribution, Apache-2.0 license, and modified-file notice
in every installed copy. Keep the GitHub profile purpose and existing history.

For updater changes, run `python3 -m unittest discover -s tests -v`, inspect both
consumer preflight and rollback behavior, and verify exact source/file hashes and
relative Claude links. Preserve unrelated consumer instructions, work, private
settings, global skills, and Geddy's public research plugin.
