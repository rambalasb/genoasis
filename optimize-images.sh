#!/bin/bash

# Image Optimization Script
# This script converts images to WebP format and optimizes them

# Check if imagemagick is installed
if ! command -v convert &> /dev/null
then
    echo "ImageMagick is not installed. Please install it first:"
    echo "brew install imagemagick  # For macOS"
    exit 1
fi

# Check if cwebp is installed
if ! command -v cwebp &> /dev/null
then
    echo "WebP tools are not installed. Please install them first:"
    echo "brew install webp  # For macOS"
    exit 1
fi

# Directory containing images
IMAGES_DIR="images"

# Create a directory for optimized images if it doesn't exist
mkdir -p "${IMAGES_DIR}/optimized"

echo "Starting image optimization..."

# Counter for processed images
processed=0

# Process all JPG and PNG images
for img in "${IMAGES_DIR}"/*.{jpg,jpeg,png,JPG,JPEG,PNG} 2>/dev/null; do
    if [ -f "$img" ]; then
        # Get filename without extension
        filename=$(basename "$img")
        name="${filename%.*}"
        
        # Create WebP version
        webp_file="${IMAGES_DIR}/optimized/${name}.webp"
        
        echo "Processing: $filename"
        
        # Convert to WebP with quality 85
        cwebp -q 85 "$img" -o "$webp_file" 2>/dev/null
        
        if [ $? -eq 0 ]; then
            # Check if WebP is smaller than original
            original_size=$(stat -f%z "$img" 2>/dev/null || stat -c%s "$img" 2>/dev/null)
            webp_size=$(stat -f%z "$webp_file" 2>/dev/null || stat -c%s "$webp_file" 2>/dev/null)
            
            if [ "$webp_size" -lt "$original_size" ]; then
                echo "  ✓ Created optimized WebP: Saved $((original_size - webp_size)) bytes"
            else
                rm "$webp_file"
                echo "  ⊗ Original is smaller, keeping original format"
            fi
            
            ((processed++))
        fi
    fi
done

echo ""
echo "Optimization complete! Processed $processed images."
echo "Optimized images are in ${IMAGES_DIR}/optimized/ directory"

# Optional: Create responsive image sizes
echo ""
echo "Would you like to create responsive image sizes? (y/n)"
read -r response

if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo "Creating responsive sizes..."
    mkdir -p "${IMAGES_DIR}/responsive"
    
    for img in "${IMAGES_DIR}"/*.{jpg,jpeg,png,JPG,JPEG,PNG} 2>/dev/null; do
        if [ -f "$img" ]; then
            filename=$(basename "$img")
            name="${filename%.*}"
            
            # Create different sizes
            convert "$img" -resize 400x400 "${IMAGES_DIR}/responsive/${name}-400.webp"
            convert "$img" -resize 800x800 "${IMAGES_DIR}/responsive/${name}-800.webp"
            echo "Created responsive sizes for: $filename"
        fi
    done
fi

echo "Done!"
