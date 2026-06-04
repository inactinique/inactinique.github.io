#!/usr/bin/env python3
"""Complete centralization script for reveal.js and images."""

import os
import re
import shutil
from pathlib import Path

PREZ_DIR = Path("/Users/frederic.clavert/GitHub/inactinique.github.io/prez")
TARGET_IMG = PREZ_DIR / "img"

def update_revealjs_paths():
    """Update all HTML files to use centralized reveal.js from /prez/lib/."""
    html_files = list(PREZ_DIR.rglob("*.html"))
    updated_count = 0
    
    for html_file in html_files:
        content = html_file.read_text()
        original_content = content
        
        # Patterns for reveal.js-4.2.1
        content = re.sub(
            r'src="([^"]*)reveal\.js-4\.2\.1(/[^"]*)"',
            r'src="/prez/lib/reveal.js-4.2.1\2"',
            content
        )
        content = re.sub(
            r'href="([^"]*)reveal\.js-4\.2\.1(/[^"]*)"',
            r'href="/prez/lib/reveal.js-4.2.1\2"',
            content
        )
        
        # Patterns for reveal.js-3.3.0.1
        content = re.sub(
            r'src="([^"]*)reveal\.js-3\.3\.0\.1(/[^"]*)"',
            r'src="/prez/lib/reveal.js-3.3.0.1\2"',
            content
        )
        content = re.sub(
            r'href="([^"]*)reveal\.js-3\.3\.0\.1(/[^"]*)"',
            r'href="/prez/lib/reveal.js-3.3.0.1\2"',
            content
        )
        
        # Patterns for _files/reveal.js
        content = re.sub(
            r'src="([^"]*)_files/reveal\.js-4\.2\.1(/[^"]*)"',
            r'src="/prez/lib/reveal.js-4.2.1\2"',
            content
        )
        content = re.sub(
            r'src="([^"]*)_files/reveal\.js-3\.3\.0\.1(/[^"]*)"',
            r'src="/prez/lib/reveal.js-3.3.0.1\2"',
            content
        )
        
        if content != original_content:
            html_file.write_text(content)
            updated_count += 1
            print(f"✅ Reveal.js paths updated: {html_file.relative_to(PREZ_DIR)}")
    
    return updated_count

def centralize_images():
    """Copy all images to prez/img/ preserving directory structure."""
    img_dirs = list(PREZ_DIR.rglob("img"))
    img_dirs = [d for d in img_dirs if d != TARGET_IMG]
    
    copied_count = 0
    for img_dir in img_dirs:
        rel_path = img_dir.relative_to(PREZ_DIR)
        target_dir = TARGET_IMG / rel_path.parent
        target_dir.mkdir(parents=True, exist_ok=True)
        
        for item in img_dir.iterdir():
            if item.is_file() and item.name != ".DS_Store":
                target_file = target_dir / item.name
                shutil.copy2(item, target_file)
                copied_count += 1
                print(f"✅ Image copied: {rel_path}/{item.name}")
    
    return copied_count

def update_image_paths():
    """Update all image references in HTML and CSS files."""
    files = list(PREZ_DIR.rglob("*.html")) + list(PREZ_DIR.rglob("*.css"))
    updated_count = 0
    
    for file in files:
        content = file.read_text()
        original_content = content
        rel_path = None
        
        try:
            rel_path = file.relative_to(PREZ_DIR)
        except ValueError:
            continue
        
        file_dir = rel_path.parent
        
        # Pattern 1: img/ with double quotes
        content = re.sub(
            r'(src|href|data-src)="img/([^"]+)"',
            lambda m: f'{m.group(1)}="/prez/img/{file_dir}/{m.group(2)}"',
            content
        )
        
        # Pattern 2: img/ with single quotes
        content = re.sub(
            r"(src|href|data-src)='img/([^']+)'",
            lambda m: f"{m.group(1)}='/prez/img/{file_dir}/{m.group(2)}'",
            content
        )
        
        # Pattern 3: img/ without quotes
        content = re.sub(
            r'(src|href|data-src)=img/([^\s>]+)',
            lambda m: f'{m.group(1)}=/prez/img/{file_dir}/{m.group(2)}',
            content
        )
        
        # Pattern 4: Markdown image syntax
        content = re.sub(
            r'\[!\]\(img/([^\)]+)\)',
            lambda m: f'![](/prez/img/{file_dir}/{m.group(1)})',
            content
        )
        
        # Pattern 5: CSS url()
        content = re.sub(
            r'url\(["\']?img/([^"\')\)]+)["\']?\)',
            lambda m: f'url(/prez/img/{file_dir}/{m.group(1)})',
            content
        )
        
        # Pattern 6: *_files/img/ with double quotes
        content = re.sub(
            r'(src|href|data-src)="([^"]*)_files/img/([^"]+)"',
            lambda m: f'{m.group(1)}="/prez/img/{m.group(2)}{m.group(3)}"',
            content
        )
        
        # Pattern 7: *_files/img/ with single quotes
        content = re.sub(
            r"(src|href|data-src)='([^']*)_files/img/([^']+)'",
            lambda m: f"{m.group(1)}='/prez/img/{m.group(2)}{m.group(3)}'",
            content
        )
        
        if content != original_content:
            file.write_text(content)
            updated_count += 1
            print(f"✅ Image paths updated: {rel_path}")
    
    return updated_count

def main():
    print("=== Step 1: Updating reveal.js paths ===")
    reveal_count = update_revealjs_paths()
    print(f"✅ Updated {reveal_count} files with reveal.js paths\n")
    
    print("=== Step 2: Centralizing images ===")
    TARGET_IMG.mkdir(parents=True, exist_ok=True)
    img_count = centralize_images()
    print(f"✅ Copied {img_count} images to prez/img/\n")
    
    print("=== Step 3: Updating image paths ===")
    path_count = update_image_paths()
    print(f"✅ Updated {path_count} files with image paths\n")
    
    print("=== Summary ===")
    print(f"Reveal.js updates: {reveal_count}")
    print(f"Images copied: {img_count}")
    print(f"Image paths updated: {path_count}")

if __name__ == "__main__":
    main()
