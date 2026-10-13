# Security Policy

## Supported versions

| Version | Supported |
| ------- | --------- |
| 0.4.x   | yes       |
| 0.3.x   | no        |

## Reporting a vulnerability

Email `security@tarot-forge.dev` with a description, a proof of concept,
and the affected version. Do not open a public issue for security bugs.
We aim to acknowledge within 72 hours and ship a fix within 14 days for
high-severity issues.

## Scope

In scope:

- Arbitrary code execution via a crafted `deck.json` manifest.
- Path traversal in deck loading or render output paths.
- Unsafe deserialization of checkpoint files.
- Local privilege escalation from the installer or updater.

Out of scope:

- The content of AI-generated images. The generator renders whatever the
  checkpoint and prompts produce; we do not filter output.
- Prompts or deck content that a user finds objectionable.
- Bugs in third-party diffusion checkpoints.

## Hardening notes

- Deck manifests are parsed with pydantic and never `eval`'d.
- Render output paths are joined with `Path` and checked to stay under
  `output_dir`.
- Checkpoints are loaded via `safetensors`, not `torch.load` with
  `pickle`.