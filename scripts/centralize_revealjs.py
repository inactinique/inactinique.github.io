#!/usr/bin/env python3
"""Centralize reveal.js references in HTML files."""

import re
from pathlib import Path

PREZ_DIR = Path("/Users/frederic.clavert/GitHub/inactinique.github.io/prez")

def update_revealjs_paths():
    """Update all HTML files to use centralized reveal.js from /prez/lib/."""
    html_files = list(PREZ_DIR.rglob("*.html"))
    updated_count = 0
    
    for html_file in html_files:
        content = html_file.read_text()
        original_content = content
        
        # Pattern for reveal.js-4.2.1 in various contexts
        # Matches: src="...reveal.js-4.2.1/..." or href="...reveal.js-4.2.1/..."
        patterns = [
            (r'src="([^"]*)reveal\.js-4\.2\.1(/[^"]*)"', r'src="/prez/lib/reveal.js-4.2.1\2"'),
            (r'href="([^"]*)reveal\.js-4\.2\.1(/[^"]*)"', r'href="/prez/lib/reveal.js-4.2.1\2"'),
            (r'src="([^"]*)reveal\.js-3\.3\.0\.1(/[^"]*)"', r'src="/prez/lib/reveal.js-3.3.0.1\2"'),
            (r'href="([^"]*)reveal\.js-3\.3\.0\.1(/[^"]*)"', r'href="/prez/lib/reveal.js-3.3.0.1\2"'),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)
        
        # Also handle paths with _files/
        content = re.sub(
            r'src="([^"]*)_files/reveal\.js-4\.2\.1(/[^"]*)"',
            r'src="/prez/lib/reveal.js-4.2.1\2"',
            content
        )
        content = re.sub(
            r'href="([^"]*)_files/reveal\.js-4\.2\.1(/[^"]*)"',
            r'href="/prez/lib/reveal.js-4.2.1\2"',
            content
        )
        content = re.sub(
            r'src="([^"]*)_files/reveal\.js-3\.3\.0\.1(/[^"]*)"',
            r'src="/prez/lib/reveal.js-3.3.0.1\2"',
            content
        )
        content = re.sub(
            r'href="([^"]*)_files/reveal\.js-3\.3\.0\.1(/[^"]*)"',
            r'href="/prez/lib/reveal.js-3.3.0.1\2"',
            content
        )
        
        if content != original_content:
            html_file.write_text(content)
            updated_count += 1
            print(f"✅ Updated: {html_file.relative_to(PREZ_DIR)}")
    
    print(f"\n📊 Total HTML files updated: {updated_count}")
    return updated_count

if __name__ == "__main__":
    update_revealjs_paths()
