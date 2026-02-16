#!/usr/bin/env python3
"""Fetch publications from ORBilu and write to _data/publications.json."""

import json
import os
import ssl
import sys
import urllib.request
import xml.etree.ElementTree as ET

API_URL = (
    "https://orbilu.uni.lu/rest/items"
    "?query=(author_authority%3A%2850029240%29)"
    "&sort_1=issued_dt:desc"
    "&sort_2=author_sort:asc"
    "&sort_3=title_sort:asc"
    "&mode=apa"
    "&lang=en"
    "&limit=200"
)


def fetch_xml(url):
    """Fetch XML from the ORBilu REST API."""
    req = urllib.request.Request(url, headers={"Accept": "application/xml"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read()
    except urllib.error.URLError as e:
        if "CERTIFICATE_VERIFY_FAILED" in str(e):
            # Fallback for environments with missing CA certs (e.g. macOS)
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
                return resp.read()
        raise


def parse_items(xml_bytes):
    """Parse XML into a list of publication dicts."""
    root = ET.fromstring(xml_bytes)
    publications = []

    for item in root.findall("item"):
        type_el = item.find("type")
        pub_type = type_el.text if type_el is not None else None
        pub_type_code = type_el.get("code") if type_el is not None else None

        authors = [a.text for a in item.findall("author") if a.text]
        title = _text(item, "title")
        doi = _text(item, "doi")
        handle = _text(item, "handle")
        pub_date = _text(item, "publicationDate")
        citation = _text(item, "citation")

        peer_reviewed = False
        for r in item.findall("review"):
            if r.get("code") == "peerreviewed":
                peer_reviewed = True
                break

        publications.append({
            "type": pub_type,
            "type_code": pub_type_code,
            "authors": authors,
            "title": title,
            "doi": doi,
            "handle": handle,
            "publication_date": pub_date,
            "citation": citation,
            "peer_reviewed": peer_reviewed,
        })

    return publications


def _text(element, tag):
    """Get text of first matching child, or None."""
    child = element.find(tag)
    return child.text if child is not None and child.text else None


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    data_dir = os.path.join(repo_root, "_data")
    os.makedirs(data_dir, exist_ok=True)
    output_path = os.path.join(data_dir, "publications.json")

    print("Fetching publications from ORBilu...")
    try:
        xml_bytes = fetch_xml(API_URL)
    except Exception as e:
        print(f"Error fetching from ORBilu: {e}", file=sys.stderr)
        sys.exit(1)

    publications = parse_items(xml_bytes)
    print(f"Parsed {len(publications)} publications.")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(publications, f, ensure_ascii=False, indent=2)

    print(f"Written to {output_path}")


if __name__ == "__main__":
    main()
