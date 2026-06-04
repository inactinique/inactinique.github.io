#!/usr/bin/env python3
"""Update image paths in HTML and CSS files to point to /prez/img/."""

import re
from pathlib import Path

PREZ_DIR = Path("/Users/frederic.clavert/GitHub/inactinique.github.io/prez")

def get_relative_prez_path(file_path):
    """Get the relative path from prez/ for a file."""
    try:
        return file_path.relative_to(PREZ_DIR)
    except ValueError:
        return None

def update_image_paths():
    """Update all image references in HTML and CSS files."""
    # Find all HTML and CSS files
    files = list(PREZ_DIR.rglob("*.html")) + list(PREZ_DIR.rglob("*.css"))
    updated_count = 0
    
    for file in files:
        content = file.read_text()
        original_content = content
        rel_path = get_relative_prez_path(file)
        
        if not rel_path:
            continue
            
        # Get the directory of the current file relative to prez/
        file_dir = rel_path.parent
        
        # Pattern 1: Simple img/ references
        # src="img/filename.png" -> src="/prez/img/{file_dir}/filename.png"
        content = re.sub(
            r'(src|href|url\(|background-image:\s*url\(\s*["\']?)img/([^"\')]+)(["\')]?)',
            lambda m: f"{m.group(1)}/prez/img/{file_dir}/{m.group(2)}{m.group(3)}",
            content
        )
        
        # Pattern 2: References with ../img/ (for files in subdirectories)
        content = re.sub(
            r'(src|href|url\(|background-image:\s*url\(\s*["\']?)(\.\./)+img/([^"\')]+)(["\')]?)',
            lambda m: f"{m.group(1)}/prez/img/{file_dir}/{m.group(3)}{m.group(4)}",
            content
        )
        
        # Pattern 3: References in *_files/img/ directories
        content = re.sub(
            r'(src|href|url\(|background-image:\s*url\(\s*["\']?)([^"\']*)_files/img/([^"\')]+)(["\')]?)',
            lambda m: f"{m.group(1)}/prez/img/{m.group(2)}{m.group(3)}{m.group(4)}",
            content
        )
        
        # Pattern 4: Absolute paths from root (shouldn't happen but just in case)
        content = re.sub(
            r'(src|href|url\(|background-image:\s*url\(\s*["\']?)/img/([^"\')]+)(["\')]?)',
            r'\1/prez/img/\2\3',
            content
        )
        
        if content != original_content:
            file.write_text(content)
            updated_count += 1
            print(f"✅ Updated: {rel_path}")
    
    print(f"\n📊 Total files updated: {updated_count}")
    return updated_count

if __name__ == "__main__":
    update_image_paths()
