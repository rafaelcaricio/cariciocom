#!/usr/bin/env python3
"""
WordPress to Zola Migration Script (XML-based)
Migrates posts, pages, categories, tags, and media from WordPress WXR export to Zola
"""

import os
import re
import html
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from lxml import etree
from html2text import HTML2Text

# Configuration
XML_FILE = Path("rafaelcaricio.WordPress.2026-01-11 (1).xml")
OUTPUT_DIR = Path("content")
STATIC_DIR = Path("static")
MEDIA_DIR = STATIC_DIR / "wp-content" / "uploads"

# Create directories
OUTPUT_DIR.mkdir(exist_ok=True)
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

# Create subdirectories
POSTS_DIR = OUTPUT_DIR / "blog"
PAGES_DIR = OUTPUT_DIR
POSTS_DIR.mkdir(exist_ok=True)

# WordPress XML namespaces
NS = {
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'wfw': 'http://wellformedweb.org/CommentAPI/',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'wp': 'http://wordpress.org/export/1.2/',
    'excerpt': 'http://wordpress.org/export/1.2/excerpt/',
}


def parse_xml():
    """Parse WordPress XML export file"""
    parser = etree.XMLParser(recover=True, remove_blank_text=True)
    tree = etree.parse(str(XML_FILE), parser)
    root = tree.getroot()
    return root


def get_xml_text(element, xpath, ns=None):
    """Get text from XML element"""
    if ns is None:
        ns = NS
    found = element.find(xpath, namespaces=ns)
    if found is not None and found.text:
        return found.text
    return None


def get_xml_cdata(element, xpath, ns=None):
    """Get CDATA content from XML element"""
    if ns is None:
        ns = NS
    found = element.find(xpath, namespaces=ns)
    if found is not None:
        return found.text or ''
    return ''


def html_to_markdown(html_content):
    """Convert HTML to Markdown using html2text"""
    if not html_content:
        return ""
    h = HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.ignore_emphasis = False
    h.body_width = 0  # No line wrapping
    h.unicode_snob = True
    h.mark_code = True
    markdown = h.handle(html_content)
    return markdown.strip()


def process_content_links(markdown_content):
    """Process and fix links in markdown content"""
    # Fix WordPress media links to point to static files
    markdown_content = re.sub(
        r'https://caricio\.com/wp-content/uploads/([^\s\)]+)',
        r'/wp-content/uploads/\1',
        markdown_content
    )
    # Fix WordPress post links
    markdown_content = re.sub(
        r'https://caricio\.com/([^/\s\)\]]+)',
        r'/\1',
        markdown_content
    )
    return markdown_content


def convert_date(wp_date):
    """Convert WordPress date to Zola format"""
    try:
        # WordPress format: 2021-07-08 08:56:00
        dt = datetime.strptime(wp_date, '%Y-%m-%d %H:%M:%S')
        return dt.strftime('%Y-%m-%d')
    except:
        try:
            # Try ISO format
            dt = datetime.fromisoformat(wp_date.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d')
        except:
            return ''


def sanitize_filename(name):
    """Sanitize filename"""
    name = re.sub(r'[^\w\-_.]', '_', name)
    return name


def migrate_post(item):
    """Migrate a single post to Zola"""
    title = get_xml_cdata(item, 'title')
    link = get_xml_text(item, 'link')
    slug = get_xml_text(item, 'wp:post_name')
    pub_date = get_xml_text(item, 'pubDate')
    post_date = get_xml_text(item, 'wp:post_date')
    content_html = get_xml_cdata(item, 'content:encoded')
    excerpt_html = get_xml_cdata(item, 'excerpt:encoded')
    status = get_xml_text(item, 'wp:status')
    
    # Skip non-published posts
    if status != 'publish':
        print(f"  Skipping draft/private post: {title}")
        return None
    
    # Convert to markdown
    content_md = html_to_markdown(content_html)
    content_md = process_content_links(content_md)
    
    # Parse categories
    categories = []
    for cat in item.findall('category', namespaces=NS):
        domain = cat.get('domain')
        if domain == 'category':
            cat_name = cat.text
            if cat_name and cat_name != 'Uncategorized':
                # Use slug from nicename attribute if available
                cat_slug = sanitize_filename(cat_name.lower().replace(' ', '-'))
                categories.append(cat_slug)
    
    # Parse tags
    tags = []
    for cat in item.findall('category', namespaces=NS):
        domain = cat.get('domain')
        if domain == 'post_tag':
            tag_name = cat.text
            if tag_name:
                tag_slug = sanitize_filename(tag_name.lower().replace(' ', '-'))
                tags.append(tag_slug)
    
    # Create date
    date = convert_date(post_date)
    
    # Create filename with date prefix
    if date:
        filename = f"{date}-{slug}.md"
    else:
        filename = f"{slug}.md"
    filepath = POSTS_DIR / filename
    
    # Create frontmatter
    frontmatter = f"""+++
title = "{html.unescape(title)}"
date = {date}
slug = "{slug}"
"""
    
    if excerpt_html:
        excerpt_md = html_to_markdown(excerpt_html)
        frontmatter += f'description = """{html.unescape(excerpt_md).strip()}"""\n'
    
    # Add taxonomies
    if categories or tags:
        frontmatter += '\n[taxonomies]\n'
        if categories:
            frontmatter += f'categories = {categories}\n'
        if tags:
            frontmatter += f'tags = {tags}\n'
    
    frontmatter += '+++\n'
    
    # Write file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(frontmatter + '\n' + content_md)
    
    print(f"  Created: {filename}")
    return {
        'title': title,
        'slug': slug,
        'link': link,
        'date': date,
        'file': str(filepath)
    }


def create_redirect_map(migrated_posts):
    """Create a redirect map for URL preservation"""
    redirects = {}
    
    for post in migrated_posts:
        wp_url = post.get('link', '')
        slug = post.get('slug', '')
        date = post.get('date', '')
        
        if wp_url and slug:
            # WordPress: https://caricio.com/slug/
            # Zola: https://caricio.com/blog/date-slug/
            zola_slug = f"{date}-{slug}" if date else slug
            redirects[wp_url.rstrip('/')] = f"/blog/{zola_slug}/"
    
    with open('redirects.json', 'w') as f:
        import json
        json.dump(redirects, f, indent=2)
    
    print(f"\nCreated redirects.json with {len(redirects)} redirects")


def create_index_page():
    """Create index page for blog section"""
    index_path = POSTS_DIR / "_index.md"
    with open(index_path, 'w') as f:
        f.write("""+++
title = "Blog"
sort_by = "date"
paginate_by = 10
template = "section.html"
+++
""")
    print(f"Created blog index: {index_path}")


def update_config():
    """Update config.toml to add taxonomies"""
    config_path = Path("config.toml")
    
    # Read existing config
    with open(config_path, 'r') as f:
        config = f.read()
    
    # Check if taxonomies already exist
    if '[taxonomies]' in config or 'taxonomies =' in config:
        print("Taxonomies already in config.toml")
        return
    
    # Add taxonomies
    taxonomy_config = """

taxonomies = [
    {name = "categories", feed = true},
    {name = "tags", feed = true},
]
"""
    
    # Append to config
    with open(config_path, 'a') as f:
        f.write(taxonomy_config)
    
    print("Added taxonomies to config.toml")


def main():
    print("=" * 60)
    print("WordPress to Zola Migration (XML-based)")
    print("=" * 60)
    
    # Parse XML
    print(f"\nParsing XML file: {XML_FILE}")
    root = parse_xml()
    
    # Find all items
    items = root.findall('.//item')
    print(f"Found {len(items)} items in XML")
    
    # Separate posts by type
    posts = []
    attachments = []
    
    for item in items:
        post_type = get_xml_text(item, 'wp:post_type')
        if post_type == 'post':
            posts.append(item)
        elif post_type == 'attachment':
            attachments.append(item)
    
    print(f"  Posts: {len(posts)}")
    print(f"  Attachments: {len(attachments)}")
    
    # Migrate posts
    print(f"\nMigrating posts to {POSTS_DIR}...")
    migrated_posts = []
    
    for post in posts:
        result = migrate_post(post)
        if result:
            migrated_posts.append(result)
    
    # Create blog index
    print(f"\nCreating blog index page...")
    create_index_page()
    
    # Create redirect map
    print(f"\nCreating redirect map...")
    create_redirect_map(migrated_posts)
    
    # Update config
    print(f"\nUpdating config.toml...")
    update_config()
    
    print("\n" + "=" * 60)
    print("Migration complete!")
    print("=" * 60)
    print(f"\nMigrated {len(migrated_posts)} posts")
    print(f"\nNext steps:")
    print("1. Review migrated content in content/blog/")
    print("2. Download media files manually or add media download feature")
    print("3. Test site with: ./venv/bin/zola serve")
    print("4. Review redirects.json for URL mapping")


if __name__ == "__main__":
    main()
