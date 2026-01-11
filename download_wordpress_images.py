#!/usr/bin/env python3
"""
WordPress Image Downloader for Zola Migration
Downloads all images referenced in blog posts from the live WordPress site.
"""

import os
import re
import requests
from pathlib import Path
from typing import Set, Tuple

# Configuration
WORDPRESS_URL = "https://caricio.com"
CONTENT_DIR = Path("content/blog")
STATIC_DIR = Path("static")
IMAGE_PATTERN = re.compile(r'!\[.*?\]\((/wp-content/uploads/[^)]+)\)')


def extract_image_urls(content_dir: Path) -> Set[str]:
    """Extract all unique image URLs from blog post markdown files."""
    image_urls = set()

    print(f"Scanning blog posts for images in {content_dir}...")

    for md_file in content_dir.glob("*.md"):
        if md_file.name == "_index.md":
            continue

        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            matches = IMAGE_PATTERN.findall(content)
            image_urls.update(matches)

    return image_urls


def create_directories(image_urls: Set[str], static_dir: Path) -> None:
    """Create necessary directory structure for images."""
    directories = set()

    for url in image_urls:
        # Extract directory path (e.g., /wp-content/uploads/2022/10/)
        dir_path = os.path.dirname(url)
        full_path = static_dir / dir_path.lstrip('/')
        directories.add(full_path)

    print("\nCreating directories:")
    for directory in sorted(directories):
        directory.mkdir(parents=True, exist_ok=True)
        print(f"  {directory}")


def download_images(image_urls: Set[str], wordpress_url: str, static_dir: Path) -> Tuple[int, int, int]:
    """
    Download all images from WordPress site.
    Returns: (successful_downloads, failed_downloads, total_bytes)
    """
    successful = 0
    failed = 0
    total_bytes = 0

    image_list = sorted(image_urls)
    total_images = len(image_list)

    print(f"\nDownloading {total_images} images from {wordpress_url}...")

    for idx, image_url in enumerate(image_list, 1):
        # Construct full URL and local path
        full_url = f"{wordpress_url}{image_url}"
        local_path = static_dir / image_url.lstrip('/')

        # Skip if already exists
        if local_path.exists():
            file_size = local_path.stat().st_size
            print(f"  [{idx}/{total_images}] ⊙ {image_url} (already exists, {file_size:,} bytes)")
            successful += 1
            total_bytes += file_size
            continue

        try:
            # Download image
            response = requests.get(full_url, timeout=30)
            response.raise_for_status()

            # Save to file
            with open(local_path, 'wb') as f:
                f.write(response.content)

            file_size = len(response.content)
            total_bytes += file_size

            print(f"  [{idx}/{total_images}] ✓ {image_url} ({file_size:,} bytes)")
            successful += 1

        except requests.exceptions.RequestException as e:
            print(f"  [{idx}/{total_images}] ✗ {image_url} - Error: {e}")
            failed += 1

    return successful, failed, total_bytes


def verify_downloads(image_urls: Set[str], static_dir: Path) -> Tuple[int, int]:
    """
    Verify all images were downloaded successfully.
    Returns: (valid_files, invalid_files)
    """
    valid = 0
    invalid = 0

    for image_url in sorted(image_urls):
        local_path = static_dir / image_url.lstrip('/')

        if local_path.exists() and local_path.stat().st_size > 0:
            valid += 1
        else:
            invalid += 1
            print(f"  ✗ Missing or empty: {image_url}")

    return valid, invalid


def main():
    """Main execution function."""
    print("=" * 70)
    print("WordPress Image Migration Script")
    print("=" * 70)

    # Step 1: Extract image URLs
    image_urls = extract_image_urls(CONTENT_DIR)
    print(f"Found {len(image_urls)} unique images to download\n")

    if not image_urls:
        print("No images found in blog posts. Exiting.")
        return

    # Step 2: Create directory structure
    create_directories(image_urls, STATIC_DIR)

    # Step 3: Download images
    successful, failed, total_bytes = download_images(image_urls, WORDPRESS_URL, STATIC_DIR)

    # Step 4: Verify downloads
    print("\nVerifying downloads...")
    valid, invalid = verify_downloads(image_urls, STATIC_DIR)

    # Step 5: Summary report
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Total images:        {len(image_urls)}")
    print(f"  ✓ Downloaded:        {successful}")
    print(f"  ✗ Failed:            {failed}")
    print(f"  ✓ Verified valid:    {valid}")
    print(f"  ✗ Invalid/missing:   {invalid}")
    print(f"  Total size:          {total_bytes / 1024 / 1024:.2f} MB")
    print("=" * 70)

    if failed > 0 or invalid > 0:
        print("\n⚠ WARNING: Some images failed to download or are invalid!")
        return 1
    else:
        print("\n✓ SUCCESS: All images downloaded and verified!")
        return 0


if __name__ == "__main__":
    exit(main())
