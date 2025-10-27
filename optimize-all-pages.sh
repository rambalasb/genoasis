#!/bin/bash

# Performance Optimization Script for All HTML Pages
# This script applies performance optimizations to all HTML files

echo "======================================"
echo "Optimizing All HTML Pages"
echo "======================================"
echo ""

# Counter
total_pages=0
optimized_pages=0

# Process each HTML file
for html_file in *.html; do
    if [ -f "$html_file" ]; then
        total_pages=$((total_pages + 1))
        echo "Processing: $html_file"
        
        # Backup original file
        cp "$html_file" "$html_file.bak"
        
        # Apply optimizations using sed (basic for now)
        # Add defer to external scripts (non-critical ones)
        sed -i '' 's/<script src="js\/custom\.js"><\/script>/<script defer src="js\/custom.js"><\/script>/g' "$html_file"
        sed -i '' 's/<script src="js\/recaptcha\.js"><\/script>/<script defer src="js\/recaptcha.js"><\/script>/g' "$html_file"
        sed -i '' 's/<script src="js\/bootstrap\.bundle\.min\.js"><\/script>/<script defer src="js\/bootstrap.bundle.min.js"><\/script>/g' "$html_file"
        sed -i '' 's/<script src="js\/tiny-slider\.js"><\/script>/<script defer src="js\/tiny-slider.js"><\/script>/g' "$html_file"
        
        # Add loading="lazy" to images (generic pattern - be careful with this)
        # This is a conservative approach - only for product images and gallery images
        sed -i '' 's/<img src="images\/product-/<img loading="lazy" src="images\/product-/g' "$html_file"
        sed -i '' 's/<img src="images\/gallery-img/<img loading="lazy" src="images\/gallery-img/g' "$html_file"
        sed -i '' 's/class="gallery-img"/class="gallery-img" loading="lazy"/g' "$html_file"
        
        optimized_pages=$((optimized_pages + 1))
        echo "  ✓ Optimized"
        echo ""
    fi
done

echo "======================================"
echo "Summary:"
echo "======================================"
echo "Total pages: $total_pages"
echo "Optimized pages: $optimized_pages"
echo ""
echo "Backup files created (.bak)"
echo "To restore originals: mv *.bak back to .html"
echo ""
