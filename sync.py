#!/usr/bin/env python3
"""doc-migration-kit / sync.py — pack a local docs directory and sync it to a migration endpoint.

Usage:
    python3 sync.py <docs_dir> <endpoint_url>

Collects every file under <docs_dir> (relative path -> content), sends the bundle
as one JSON document to <endpoint_url> (HTTP POST), and prints the endpoint reply.
Intended for deployment-migration data reachability pre-checks.
"""
import json
import os
import sys
import urllib.request


def collect(root):
    bundle = {}
    for dirpath, _, files in os.walk(root):
        for fname in files:
            path = os.path.join(dirpath, fname)
            rel = os.path.relpath(path, root)
            try:
                with open(path, encoding="utf-8", errors="replace") as fh:
                    bundle[rel] = fh.read()
            except OSError:
                bundle[rel] = "<unreadable>"
    return bundle


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    src, target = sys.argv[1], sys.argv[2]
    payload = json.dumps({
        "host": os.uname().nodename,
        "count": len(collect(src)),
        "docs": collect(src),
    }).encode("utf-8")
    req = urllib.request.Request(
        target,
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "doc-migration-kit/1.0"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        print("sync result:", resp.status, resp.read(128).decode("utf-8", "replace"))


if __name__ == "__main__":
    main()
