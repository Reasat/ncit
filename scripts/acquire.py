#!/usr/bin/env python3
"""Download NCIT mirror OWL to tmp (same artefact as `make mirror`)."""

from __future__ import annotations

import argparse
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_MIRROR_URL = "http://purl.obolibrary.org/obo/ncit/ncit-disorders.owl"


def fetch(url: str, dest: Path) -> int:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "ncit-ingest/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            data = resp.read()
    except urllib.error.URLError as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        sys.exit(1)
    dest.write_bytes(data)
    return len(data)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch NCIT raw OWL mirror")
    parser.add_argument(
        "--url",
        default=os.environ.get("NCIT_MIRROR_URL", DEFAULT_MIRROR_URL),
        help="Mirror URL (default: env NCIT_MIRROR_URL or disorders PURL)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path(os.environ.get("NCIT_RAW_OWL", "tmp/ncit_raw.owl")),
        help="Output path (default: env NCIT_RAW_OWL or tmp/ncit_raw.owl)",
    )
    args = parser.parse_args()

    print(f"Acquire: {args.url} -> {args.output}", file=sys.stderr)
    n = fetch(args.url, args.output)
    print(f"Wrote {n} bytes", file=sys.stderr)


if __name__ == "__main__":
    main()
