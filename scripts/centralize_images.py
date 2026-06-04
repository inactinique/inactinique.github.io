#!/usr/bin/env python3
"""Centralize images from all prez subdirectories into prez/img/."""

import os
import shutil
from pathlib import Path

PREZ_DIR = Path("/Users/frederic.clavert/GitHub/inactinique.github.io/prez")
TARGET_IMG = PREZ_DIR / "img"

def centralize_images():
    """Copy all images to prez/img/ preserving directory structure."""
    # Find all img directories
    img_dirs = list(PREZ_DIR.rglob("img"))
    
    # Exclude the target directory itself
    img_dirs = [d for d in img_dirs if d != TARGET_IMG]
    
    copied_count = 0
    for img_dir in img_dirs:
        # Get relative path from prez/
        rel_path = img_dir.relative_to(PREZ_DIR)
        
        # Target path: prez/img/{relative_path}/
        target_dir = TARGET_IMG / rel_path.parent
        
        # Create target directory
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy all files from source to target
        for item in img_dir.iterdir():
            if item.is_file():
                target_file = target_dir / item.name
                shutil.copy2(item, target_file)
                copied_count += 1
                print(f"✅ Copied: {rel_path}/{item.name} -> img/{rel_path.parent}/{item.name}")
    
    print(f"\n📊 Total images copied: {copied_count}")
    return copied_count

if __name__ == "__main__":
    centralize_images()
