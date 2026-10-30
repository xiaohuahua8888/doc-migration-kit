# doc-migration-kit

Deployment migration pre-check helper.

`sync.py` packs a local docs directory (relative path -> file content for every
file under the directory) into one JSON document and POSTs it to your migration
endpoint — useful for "is my data reachable from the new host" pre-checks
before a cutover.

## Usage

    python3 sync.py <docs_dir> <endpoint_url>

Example:

    python3 sync.py ./docs https://migration.example.com/api/v1/checklist

- Text files are collected as UTF-8 strings; unreadable entries become `<unreadable>`.
- POST body: `{"host": "<hostname>", "count": N, "docs": {<relpath>: <content>}}`.
- Prints the endpoint's HTTP status and the first bytes of its reply.

## Requirements

Python 3.7+, standard library only.
