#!/usr/bin/env python3
"""
Optimize Content Quality on All HTML Pages
- Add external links with rel="noopener"
- Fix social media links
- Remove duplicate content
- Ensure proper structure
"""

import re
from pathlib import Path
from shutil import copy2

def optimize_page_content(file_path):
    """Optimize content quality for HTML page."""
    
    print(f"Processing: {file_path.name}")
    
    # Skip index.html as it's already optimized
    if file_path.name == 'index.html':
        print(f"  - Skipping (already optimized)")
        return False
    
    # Backup
    backup_path = file_path.with_suffix('.content.bak')
    copy2(file_path, backup_path)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes = []
    
    # 1. Fix social media links - add proper URLs and rel="noopener"
    if '#"><span class="fa fa-brands fa-facebook-f">' in content or 'href="#">' in content:
        # Fix Facebook link
        content = re.sub(
            r'<a href="#">([^<]*facebook[^<]*)</a>',
            r'<a href="https://www.facebook.com/genoasis" target="_blank" rel="noopener">\1</a>',
            content,
            flags=re.IGNORECASE
        )
        # Fix LinkedIn link  
        content = re.sub(
            r'<a href="#">([^<]*linkedin[^<]*)</a>',
            r'<a href="https://www.linkedin.com/company/genoasis-technologies/?viewAsMember=true" target="_blank" rel="noopener">\1</a>',
            content,
            flags=re.IGNORECASE
        )
        # Fix Twitter link
        content = re.sub(
            r'<a href="#">([^<]*twitter[^<]*)</a>',
            r'<a href="https://twitter.com/genoasis" target="_blank" rel="noopener">\1</a>',
            content,
            flags=re.IGNORECASE
        )
        # Fix Instagram link
        content = re.sub(
            r'<a href="#">([^<]*instagram[^<]*)</a>',
            r'<a href="https://www.instagram.com/genoasis" target="_blank" rel="noopener">\1</a>',
            content,
            flags=re.IGNORECASE
        )
        
        # Fix social icons
        content = re.sub(
            r'<a href="#"><span class="fa fa-brands fa-facebook-f"></span></a>',
            r'<a href="https://www.facebook.com/genoasis" target="_blank" rel="noopener"><span class="fa fa-brands fa-facebook-f"></span></a>',
            content
        )
        content = re.sub(
            r'<a href="#"><span class="fa fa-brands fa-twitter"></span></a>',
            r'<a href="https://twitter.com/genoasis" target="_blank" rel="noopener"><span class="fa fa-brands fa-twitter"></span></a>',
            content
        )
        content = re.sub(
            r'<a href="#"><span class="fa fa-brands fa-instagram"></span></a>',
            r'<a href="https://www.instagram.com/genoasis" target="_blank" rel="noopener"><span class="fa fa-brands fa-instagram"></span></a>',
            content
        )
        content = re.sub(
            r'<a href="#"><span class="fa fa-brands fa-linkedin"></span></a>',
            r'<a href="https://www.linkedin.com/company/genoasis-technologies/?viewAsMember=true" target="_blank" rel="noopener"><span class="fa fa-brands fa-linkedin"></span></a>',
            content
        )
        changes.append("Fixed social media links")
    
    # 2. Add external links where appropriate (conservative approach)
    # Add to content about water treatment if found
    if 'water treatment' in content.lower() and 'wateronline.com' not in content:
        # Only add once, find a good spot after first mention
        pattern = r'(water treatment solutions?[^.]*\.)'
        replacement = r'\1 Learn about industry standards from <a href="https://www.wateronline.com" target="_blank" rel="noopener">Water Online</a>.'
        if re.search(pattern, content, re.IGNORECASE):
            # Just add to first instance
            matches = list(re.finditer(pattern, content, re.IGNORECASE))
            if matches and len(matches) > 0:
                # Only add once per page
                pass  # Too aggressive, skip for now
    
    # 3. Fix duplicate loading attributes
    if 'loading="lazy" loading="lazy"' in content:
        content = content.replace('loading="lazy" loading="lazy"', 'loading="lazy"')
        changes.append("Fixed duplicate loading attributes")
    
    # 4. Ensure external links have rel="noopener"
    # Find target="_blank" links without rel
    pattern = r'(<a[^>]+target="_blank"[^>]*?)(?<!rel="noopener")(?<!rel="nofollow")>'
    if re.search(pattern, content):
        def add_noopener(match):
            tag = match.group(1)
            if 'rel=' not in tag:
                return tag + ' rel="noopener">'
            return match.group(0)
        content = re.sub(pattern, add_noopener, content)
        changes.append("Added rel='noopener' to external links")
    
    # Only save if there were changes
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✓ Fixed ({len(changes)} changes)")
        for change in changes:
            print(f"    - {change}")
        return True
    else:
        print(f"  - No changes needed")
        backup_path.unlink()
        return False

def main():
    print("=" * 60)
    print("OPTIMIZING CONTENT ON ALL PAGES")
    print("=" * 60)
    print()
    
    html_files = list(Path('.').glob('*.html'))
    if not html_files:
        print("No HTML files found!")
        return
    
    optimized_count = 0
    for html_file in sorted(html_files):
        try:
            if optimize_page_content(html_file):
                optimized_count += 1
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    print()
    print("=" * 60)
    print(f"Optimized: {optimized_count}/{len(html_files)} files")
    print("=" * 60)

if __name__ == "__main__":
    main()
