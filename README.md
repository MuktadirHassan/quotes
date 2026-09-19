# Quotes

A collection of words worth remembering.

The quotes come from history, books, speeches, anime, films, games, and people. You can use them in websites, apps, bots, writing tools, or other projects.

The collection is new, and contributions are welcome.

## Get the quotes

All quotes are in [`quotes.json`](quotes.json).

Download the latest copy:

```text
https://raw.githubusercontent.com/MuktadirHassan/quotes/main/quotes.json
```

For a copy that never changes, download `quotes.json` from the [Releases](https://github.com/MuktadirHassan/quotes/releases) page.

## Add a quote

Add an entry to the `quotes` list in `quotes.json`:

```json
{
  "id": "marcus-aurelius-meditations-001",
  "text": "Example text goes here.",
  "attributedTo": "Marcus Aurelius",
  "source": {
    "type": "book",
    "title": "Meditations",
    "citation": "Book and section number",
    "url": "https://example.org/source"
  },
  "language": "en",
  "tags": ["stoicism"],
  "verification": {
    "status": "verified",
    "evidenceUrl": "https://example.org/source"
  },
  "rights": {
    "status": "public-domain"
  }
}
```

Please include a trustworthy source when possible. If you cannot confirm a quote, mark it as `unverified` rather than presenting uncertain words as fact.

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) for more details.

## Keeping the collection reliable

Every quote has a permanent ID. Automatic checks catch missing information, repeated IDs, and other mistakes.

The collection keeps separate numbers for its contents and its file format. This allows new quotes to be added without unexpectedly breaking projects that use the collection.

The current format is described in [`schemas/v1.0.0.json`](schemas/v1.0.0.json).

## Check your changes

You need Python 3.12 or newer.

```sh
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate.py
```

## Rights and attribution

The code and original project information are available under the MIT License.

The quotes may still belong to their original authors, translators, publishers, or other owners. Adding a quote here does not make it free to use. Check its source and rights information before using it, especially if it comes from anime, film, television, games, or a modern translation.
