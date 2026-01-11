#!/usr/bin/env python3
"""
Fetch code from GitHub gists and inline them into blog posts
"""

import re
import requests
from pathlib import Path
import json

# Configuration
BLOG_DIR = Path("content/blog")
GIST_API_BASE = "https://api.github.com/gists/"


def extract_gist_urls(content):
    """Extract gist URLs from markdown content"""
    pattern = r'https://gist\.github\.com/rafaelcaricio/([a-f0-9]+)'
    matches = re.findall(pattern, content)
    return matches


def fetch_gist(gist_id):
    """Fetch gist content from GitHub API"""
    url = f"{GIST_API_BASE}{gist_id}"
    print(f"Fetching gist: {gist_id}")
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"  Failed to fetch gist {gist_id}: {response.status_code}")
            return None
    except Exception as e:
        print(f"  Error fetching gist {gist_id}: {e}")
        return None


def extract_code_from_gist(gist_data):
    """Extract code files from gist data"""
    if not gist_data:
        return None
    
    code_blocks = []
    files = gist_data.get('files', {})
    
    for filename, file_info in files.items():
        raw_url = file_info.get('raw_url')
        language = file_info.get('language', '')
        content = file_info.get('content', '')
        
        if content:
            code_blocks.append({
                'filename': filename,
                'language': language.lower() if language else '',
                'content': content,
                'raw_url': raw_url
            })
    
    return code_blocks


def process_post(post_path):
    """Process a single blog post"""
    print(f"\nProcessing: {post_path.name}")
    
    with open(post_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Extract gist IDs
    gist_ids = extract_gist_urls(content)
    
    if not gist_ids:
        print("  No gist links found")
        return False
    
    print(f"  Found {len(gist_ids)} gist link(s)")
    
    # Process each gist
    for gist_id in gist_ids:
        gist_data = fetch_gist(gist_id)
        
        if not gist_data:
            continue
        
        code_blocks = extract_code_from_gist(gist_data)
        
        if not code_blocks:
            print(f"  No code found in gist {gist_id}")
            continue
        
        # Replace gist link with inline code blocks
        for code_block in code_blocks:
            gist_url = f"https://gist.github.com/rafaelcaricio/{gist_id}"
            
            # Create code block in Zola format
            language = code_block['language']
            if language:
                code_block_md = f"```{language}\n{code_block['content']}\n```\n"
            else:
                code_block_md = f"```\n{code_block['content']}\n```\n"
            
            # Replace the gist link with code block
            # Handle multiple occurrences of the same gist
            content = content.replace(gist_url, code_block_md)
            
            print(f"  Inlined: {code_block['filename']} ({language})")
    
    # Write updated content if changed
    if content != original_content:
        with open(post_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("  Updated post")
        return True
    else:
        print("  No changes needed")
        return False


def main():
    """Main function"""
    print("=" * 60)
    print("Gist to Inline Code - Migration Tool")
    print("=" * 60)
    
    # Find all markdown files in blog directory
    post_files = list(BLOG_DIR.glob("*.md"))
    
    if not post_files:
        print(f"No markdown files found in {BLOG_DIR}")
        return
    
    print(f"\nFound {len(post_files)} blog post(s)\n")
    
    # Process each post
    updated_count = 0
    total_gists = 0
    
    for post_path in sorted(post_files):
        result = process_post(post_path)
        if result:
            updated_count += 1
    
    print("\n" + "=" * 60)
    print("Migration Complete!")
    print("=" * 60)
    print(f"Posts updated: {updated_count}")
    print(f"Total gist links found and processed: {total_gists}")
    print("\nAll gist code has been inlined using Zola syntax highlighting")


if __name__ == "__main__":
    main()
