#!/usr/bin/env python3
"""
Script to organize Haji Ali images.
Renames and copies images to images/haji-ali/ directory.
"""

import os
import shutil
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Define the image names in order
image_names = [
    "2026-03-19-haji-ali-exterior.jpeg",
    "2026-03-19-haji-ali-fruit-display.jpeg",
    "2026-03-19-haji-ali-dahi-puri-plate.jpeg",
    "2026-03-19-haji-ali-dahi-puri-closeup-1.jpeg",
    "2026-03-19-haji-ali-dahi-puri-closeup-2.jpeg",
    "2026-03-19-haji-ali-dahi-puri-spoon.jpeg",
    "2026-03-19-haji-ali-kiwi-cream-spoon.jpeg",
    "2026-03-19-haji-ali-kiwi-cream-closeup.jpeg",
    "2026-03-19-haji-ali-kiwi-cream-full.jpeg",
]

# Destination directory
dest_dir = Path("/workspaces/fatindiangirl/images/haji-ali")

# Create destination directory if it doesn't exist
dest_dir.mkdir(parents=True, exist_ok=True)
print(f"✓ Created directory: {dest_dir}\n")

# Search locations for images (in order of priority)
search_locations = [
    Path.home() / "Downloads",
    Path.home() / ".cache",
    Path("/tmp"),
    Path.cwd(),
]

print("Searching for image files...")
image_extensions = ['.jpeg', '.jpg', '.png', '.webp']
source_files = []

for search_dir in search_locations:
    if not search_dir.exists():
        continue
    
    try:
        for ext in image_extensions:
            found = list(search_dir.glob(f'*{ext}')) + list(search_dir.glob(f'*{ext.upper()}'))
            source_files.extend(found)
    except PermissionError:
        continue

# Remove duplicates and sort by modification time (newest first)
source_files = list(set(source_files))
source_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

print(f"Found {len(source_files)} image files\n")

if source_files:
    print("Images found (most recent first):")
    for i, f in enumerate(source_files[:15], 1):
        print(f"  {i}. {f.name}")
    print()

# Ask user for source directory if not enough files found
if len(source_files) < len(image_names):
    print(f"⚠ Found only {len(source_files)} files, but need {len(image_names)}")
    source_input = input("\nEnter the full path to the folder containing the images (or press Enter to skip): ").strip()
    
    if source_input and Path(source_input).exists():
        source_dir = Path(source_input)
        source_files = []
        for ext in image_extensions:
            source_files.extend(source_dir.glob(f'*{ext}'))
            source_files.extend(source_dir.glob(f'*{ext.upper()}'))
        source_files = list(set(source_files))
        source_files.sort()
        print(f"\nFound {len(source_files)} images in {source_dir}\n")
    else:
        print("No valid path provided. Exiting.")
        sys.exit(1)

# Rename and copy files
if len(source_files) >= len(image_names):
    for i, new_name in enumerate(image_names):
        source_file = source_files[i]
        dest_file = dest_dir / new_name
        
        try:
            shutil.copy2(source_file, dest_file)
            print(f"✓ {source_file.name} → {new_name}")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    print(f"\n✓ All images organized successfully in {dest_dir}")
else:
    print(f"✗ Not enough images found. Found {len(source_files)}, need {len(image_names)}")
    sys.exit(1)
