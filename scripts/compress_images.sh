#!/bin/bash
# Compress images in prez/ directory
# Uses ImageMagick (magick) for JPEG and OptiPNG for PNG

set -e

echo "🔍 Searching for images to compress..."

# Find all JPEG/JPG images and compress with quality 85%
find prez -type f \( -iname "*.jpg" -o -iname "*.jpeg" \) -print0 | while IFS= read -r -d $'\0' file; do
    echo "📄 Compressing JPEG: $file"
    # Create a temporary file
    temp_file="${file}.tmp"
    # Compress with quality 85 and progressive encoding
    magick "$file" -quality 85 -sampling-factor 4:2:0 -interlace Plane "$temp_file"
    # Replace original with compressed version
    mv "$temp_file" "$file"
    echo "  ✅ Done: $(du -h "$file" | cut -f1)"
done

echo ""
echo "🔍 Searching for PNG images to compress..."

# Find all PNG images and compress with OptiPNG
find prez -type f -iname "*.png" -print0 | while IFS= read -r -d $'\0' file; do
    echo "📄 Compressing PNG: $file"
    # Compress with OptiPNG (level 2 for good compression/speed balance)
    optipng -o2 -quiet "$file"
    echo "  ✅ Done: $(du -h "$file" | cut -f1)"
done

echo ""
echo "🎉 All images compressed!"
