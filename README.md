# Adam Messinger

This remains the repository associated with Adam Messinger's GitHub profile.
The earlier application moved to `adam-messinger/iris`; its reset/history is
preserved. This repository also serves as the canonical source for shared
developer skills used by Codex and Claude Code in Geddy and Cashflow.

The portable packages under `skills/` are `go`, `simplify`, and `triage-and-go`.
Creating or installing them does not execute their workflows.

See [shared skill installation and compatibility](docs/shared-agent-skills.md)
for invocation, a pinned one-command update of both consumers, upstream
attribution, cloud prerequisites, and validation evidence.

Run the source installer tests with:

```sh
python3 -m unittest discover -s tests -v
```
