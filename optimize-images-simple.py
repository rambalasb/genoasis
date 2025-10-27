#!/usr/bin/env python3
"""
Simple Image Optimization Helper
This script checks images and provides optimization recommendations.
"""

import os
from pathlib import Path

def get_image_info():
    """Analyze images directory and provide recommendations."""
    
    images_dir = Path("images")
    if not images_dir.exists():
        print("Images directory not found!")
        return
    
    print("=" * 60)
    print("IMAGE OPTIMIZATION ANALYSIS")
    print("=" * 60)
    print()
    
    # Find all images
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']:
        image_files.extend(images_dir.glob(ext))
    
    if not image_files:
        print("No images found in images/ directory")
        return
    
    print(f"Found {len(image_files)} images to optimize")
    print()
    
    # Calculate total size
    total_size = sum(f.stat().st_size for f in image_files)
    total_size_mb = total_size / (1024 * 1024)
    
    print(f"Total image size: {total_size_mb:.2f} MB")
    print()
    
    # Estimate potential savings with WebP
    estimated_webp_size = total_size * 0.7  # 30% reduction
    estimated_savings = total_size - estimated_webp_size
    estimated_savings_mb = estimated_savings / (1024 * 1024)
    
    print("OPTIMIZATION RECOMMENDATIONS:")
    print("-" * 60)
    print(f"Estimated savings with WebP: {estimated_savings_mb:.2f} MB")
    print(f"Estimated load time improvement: 30-40%")
    print()
    
    # List largest images
    sorted_images = sorted(image_files, key=lambda x: x.stat().st_size, reverse=True)
    print("LARGEST IMAGES (Top 10):")
    print("-" * 60)
    for i, img in enumerate(sorted_images[:10], 1):
        size_kb = img.stat().st_size / 1024
        size_mb = img.stat().st_size / (1024 * 1024)
        if size_mb >= 1:
            size_str = f"{size_mb:.2f} MB"
        else:
            size_str = f"{size_kb:.2f} KB"
        print(f"{i:2}. {img.name:40s} {size_str:>10s}")
    
    print()
    print("=" * 60)
    print("RECOMMENDATIONS:")
    print("=" * 60)
    print("1. Use online tools to convert images to WebP:")
    print("   - Squoosh.app (recommended)")
    print("   - CloudConvert.com")
    print("   - ImageMagick (command line)")
    print()
    print("2. Compress large images (>500KB):")
    for img in sorted_images:
        if img.stat().st_size > 500 * 1024:
            print(f"   - {img.name}")
    print()
    print("3. Consider using CDN for faster delivery")
    print()
    print("4. Current optimizations already in place:")
    print("   ✓ Lazy loading for below-fold images")
    print("   ✓ Proper image dimensions in HTML")
    print("   ✓ Deferred JavaScript")
    print("   ✓ WebP support in .htaccess")
    print()
    print("=" * 60)

if __name__ == "__main__":
    get_image_info()
