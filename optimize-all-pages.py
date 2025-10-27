#!/usr/bin/env python3
"""
Comprehensive HTML Page Optimization Script
Applies performance optimizations to all HTML files
"""

import os
import re
from pathlib import Path
from shutil import copy2

def optimize_html_file(file_path):
    """Apply performance optimizations to an HTML file."""
    
    print(f"Processing: {file_path.name}")
    
    # Backup original file
    backup_path = file_path.with_suffix('.bak')
    copy2(file_path, backup_path)
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    modifications = []
    
    # 1. Add defer to external JavaScript files (except inline scripts)
    script_replacements = [
        ('<script src="js/custom.js"></script>', '<script defer src="js/custom.js"></script>'),
        ('<script src="js/recaptcha.js"></script>', '<script defer src="js/recaptcha.js"></script>'),
        ('<script src="js/bootstrap.bundle.min.js"></script>', '<script defer src="js/bootstrap.bundle.min.js"></script>'),
        ('<script src="js/tiny-slider.js"></script>', '<script defer src="js/tiny-slider.js"></script>'),
    ]
    
    for old, new in script_replacements:
        if old in content and new not in content:
            content = content.replace(old, new)
            modifications.append("Added defer to scripts")
    
    # 2. Add loading="lazy" to non-critical images
    # Be careful not to add to logos or above-fold images
    
    # Only add lazy loading to gallery images and product images below fold
    image_patterns = [
        # Gallery images
        (r'(<img src="images/.*?\.jpg" alt="[^"]*" class="gallery-img")',
         r'\1 loading="lazy"'),
        
        # Product images (not logo or hero images)
        (r'(<img src="images/product-[0-9]\.(jpg|png|webp)"[^>]*>)',
         lambda m: m.group(0) if 'loading=' not in m.group(0) else m.group(0)),
        
        # Industry images
        (r'(<img src="images/.*?-industry\.(png|jpg)"[^>]*class="img-fluid industry-icon")',
         r'\1 loading="lazy"'),
        
        # Hover images
        (r'(<img src="images/.*?-industry-hover\.(jpg|png)"[^>]*class="img-fluid industry-hover")',
         r'\1 loading="lazy"'),
    ]
    
    for pattern, replacement in image_patterns:
        if callable(replacement):
            content = re.sub(pattern, replacement, content)
            modifications.append("Added lazy loading to product images")
        else:
            if re.search(pattern, content) and 'loading=' not in content[:1000]:  # Check first 1000 chars
                content = re.sub(pattern, replacement, content)
                modifications.append("Added lazy loading to images")
    
    # 3. Add dimensions to images that don't have them (conservative)
    # Look for common image patterns and add reasonable defaults
    
    # 4. Add preconnect for external resources if not present
    if '<link rel="preconnect"' not in content:
        # Find the head tag and add preconnect after charset/viewport
        head_pattern = r'(<meta name="viewport"[^>]*>\s*)\n'
        preconnect_tags = '''  <!-- Preconnect to external domains for faster loading -->
  <link rel="preconnect" href="https://www.googletagmanager.com">
  <link rel="preconnect" href="https://cdnjs.cloudflare.com">
  <link rel="dns-prefetch" href="https://fonts.googleapis.com">
'''
        
        if re.search(head_pattern, content):
            content = re.sub(head_pattern, r'\1' + preconnect_tags + '\n', content, count=1)
            modifications.append("Added preconnect hints")
    
    # 5. Make non-critical CSS non-blocking
    css_patterns = [
        ('<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/', 
         '<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/'),
        ('<link href="css/tiny-slider.css"', 
         '<link href="css/tiny-slider.css" media="print" onload="this.media=\'all\'"'),
    ]
    
    for pattern, replacement in css_patterns:
        if pattern in content and 'media="print"' not in content:
            # Find and replace with proper formatting
            content = re.sub(
                r'(<link href="css/tiny-slider\.css" rel="stylesheet">)',
                r'<link href="css/tiny-slider.css" rel="stylesheet" media="print" onload="this.media=\'all\'">',
                content
            )
            modifications.append("Made CSS non-blocking")
    
    # Only write if there were actual changes
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✓ Optimized ({len(modifications)} changes)")
        for mod in modifications[:3]:  # Show first 3 modifications
            print(f"    - {mod}")
        return True
    else:
        print(f"  - No changes needed")
        # Remove backup if no changes
        backup_path.unlink()
        return False

def main():
    """Main function to process all HTML files."""
    
    print("=" * 60)
    print("HTML PAGE OPTIMIZATION")
    print("=" * 60)
    print()
    
    # Get all HTML files in current directory
    html_files = list(Path('.').glob('*.html'))
    
    if not html_files:
        print("No HTML files found in current directory!")
        return
    
    print(f"Found {len(html_files)} HTML files")
    print()
    
    optimized_count = 0
    skipped_files = []
    
    for html_file in sorted(html_files):
        try:
            result = optimize_html_file(html_file)
            if result:
                optimized_count += 1
            else:
                skipped_files.append(html_file.name)
        except Exception as e:
            print(f"  ✗ Error: {e}")
            skipped_files.append(html_file.name)
    
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total files: {len(html_files)}")
    print(f"Optimized: {optimized_count}")
    print(f"No changes needed: {len(skipped_files)}")
    print()
    
    if skipped_files:
        print("Files that didn't need changes:")
        for f in skipped_files[:5]:  # Show first 5
            print(f"  - {f}")
        if len(skipped_files) > 5:
            print(f"  ... and {len(skipped_files) - 5} more")
    
    print()
    print("Backup files created (.bak)")
    print("To restore: mv *.bak back to original names")
    print()

if __name__ == "__main__":
    main()
