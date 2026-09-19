# Contributing

Contributions are welcome. You can add a quote, correct its wording, improve its source, or fix the project tools.

## Add or correct a quote

1. Edit `quotes.json`.
2. Give each new quote a permanent ID written in lowercase with hyphens.
3. Include the clearest source you can find. An original source is best.
4. Use `verified` only when the wording and attribution can be checked through `evidenceUrl`.
5. Record rights information when it is known, and keep copyrighted excerpts brief.
6. Run the checks before opening a pull request.

```sh
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate.py
```

Do not change `datasetVersion`, `version.txt`, `.release-please-manifest.json`, or `CHANGELOG.md` by hand. The release workflow updates them together.

## Commit messages

Clear commit messages help prepare releases automatically:

- `feat: add quotes from Meditations` means the collection gained something.
- `fix: correct a quote attribution` means existing information was corrected.
- `docs: explain source requirements` means only documentation changed.
- Add `!` for a change that requires users to update their code, such as `feat!: introduce format version 2`. This moves the collection to its next major release.

## Change the file format

Small additions receive a new file such as `schemas/v1.1.0.json`. Changes that break older readers receive a new file such as `schemas/v2.0.0.json`.

Never rewrite a published schema file. Add a new one and explain how users can move to it.

## Maintainer setup

In the repository's GitHub Actions settings, give workflows read and write access and allow them to create pull requests. This lets the release workflow prepare release notes and publish tagged releases.

If `main` requires checks on every pull request, add a repository secret named `RELEASE_PLEASE_TOKEN`. It should be a fine-grained token with permission to write repository contents and pull requests.
