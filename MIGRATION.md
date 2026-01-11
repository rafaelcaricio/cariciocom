# WordPress to Zola Migration - Complete

## What Was Migrated

✅ **8 blog posts** successfully migrated from WordPress to Zola
✅ **Taxonomies configured** - Categories and Tags
✅ **Templates created** - Basic site structure
✅ **Redirect map generated** - `redirects.json` for URL preservation

## Directory Structure

```
caricio_blog/
├── config.toml                 # Updated with taxonomies
├── content/
│   ├── blog/
│   │   ├── _index.md          # Blog section index
│   │   ├── 2021-07-08-why-not-just-use-async-python-for-this-api.md
│   │   ├── 2022-06-27-install-gstreamer-srt-plugin-on-macos.md
│   │   ├── 2022-10-29-a-brief-introduction-to-gstreamer.md
│   │   ├── 2022-12-13-i-deleted-my-twitter-account.md
│   │   ├── 2023-01-26-decompress-content-using-rust-and-flate2-without-headaches.md
│   │   ├── 2023-03-18-readable-rust-combinators-vs-match-clauses.md
│   │   ├── 2025-01-11-building-a-cultural-bridge-my-late-night-hack-with-ios-shortcuts-and-ai.md
│   │   └── 2025-11-17-learn-by-example-making-it-easier-to-understand-gstreamer.md
├── templates/
│   ├── base.html              # Base template
│   ├── index.html             # Home page
│   ├── page.html              # Blog post template
│   ├── section.html           # Blog listing
│   ├── taxonomy_list.html      # Category/tag listing
│   └── taxonomy_single.html   # Single category/tag page
├── static/
│   └── wp-content/
│       └── uploads/          # Media directory (empty - needs manual download)
├── migrate_wordpress.py        # Migration script
├── redirects.json            # URL redirect mapping
└── MIGRATION.md             # This file
```

## URL Mapping

WordPress URLs have been mapped to Zola URLs:

| WordPress URL | Zola URL |
|---------------|------------|
| `/why-not-just-use-async-python-for-this-api/` | `/blog/2021-07-08-why-not-just-use-async-python-for-this-api/` |
| `/a-brief-introduction-to-gstreamer/` | `/blog/2022-10-29-a-brief-introduction-to-gstreamer/` |
| etc. | `/blog/DATE-slug/` |

The mapping is saved in `redirects.json` for implementing redirects on your server.

## Posts Migrated

1. Why not just use async Python for this API? (2021-07-08)
2. A brief introduction to GStreamer (2022-10-29)
3. Install GStreamer SRT plugin on macOS (2022-06-27)
4. I deleted my Twitter account (2022-12-13)
5. Decompress content using Rust and flate2 without headaches (2023-01-26)
6. Readable Rust: Combinators vs Match Clauses (2023-03-18)
7. Building a cultural bridge - My late-night hack with iOS Shortcuts and AI (2025-01-11)
8. Learn by example: Making it easier to understand GStreamer (2025-11-17)

## Skipped (Draft/Private Posts)

These posts were not migrated as they were not published:
- Writing GStreamer applications in Rust (draft)
- Rust bindings and external memory management models (draft)
- MPEG-TS over SRT Synchronization Example (draft)

## Taxonomies

### Categories Found:
- AI
- Automation Tool
- GStreamer
- Programming
- Python
- Rust
- Social Media
- Prompt Engineering

### Tags Found:
- ai
- async
- automation-tool
- cartoon
- fascism
- fastapi
- gst
- gstreamer
- ios
- late-night
- multimedia
- prompt-engineering
- python
- rust
- shortcuts

## Next Steps

### 1. Review Migrated Content
Check the migrated posts in `content/blog/` and verify:
- Content is formatted correctly
- Categories and tags are accurate
- Links work as expected

### 2. Download Media Files
Images are not automatically downloaded. You have two options:

**Option A: Manual Download**
```bash
# Download from WordPress and place in static/wp-content/uploads/
# The script has already created the directory structure
```

**Option B: Use wp-cli on WordPress server**
```bash
# On your WordPress server
wp media export --dir=wp-exported-media
# Then copy to static/wp-content/uploads/
```

### 3. Customize Templates
The current templates are minimal. You can:
- Add CSS styling in `sass/` directory
- Customize the layout in `templates/`
- Install a Zola theme from https://www.getzola.org/themes/

### 4. Test Locally
```bash
./venv/bin/zola serve
# Visit http://localhost:1111
```

### 5. Deploy
Once satisfied with the site, deploy using your preferred method. See:
https://www.getzola.org/documentation/deployment/overview/

### 6. Implement Redirects
Set up redirects using `redirects.json` on your web server. The format shows:
```json
{
  "https://caricio.com/old-url/": "/blog/new-url/"
}
```

For Nginx, you can create a redirect map. For Netlify, add a `_redirects` file.

### 7. Fix Broken Links
Zola reported 4 broken external links (all to GitHub):
- Link anchors that have changed on GitHub
- One Mastodon link that returned an error

You can manually fix these in the markdown files if desired.

## Migration Script

The migration script is saved as `migrate_wordpress.py` and can be re-run:
```bash
./venv/bin/python migrate_wordpress.py
```

It will:
- Parse the WordPress XML export
- Convert HTML to Markdown
- Create proper Zola front-matter
- Map categories and tags
- Generate redirect mappings

## Notes

- **Virtual Environment**: Dependencies are installed in `./venv/`
- **Python Version**: The script uses Python 3.13
- **Dependencies**: `html2text`, `requests`, `lxml`
- **Taxonomies**: Categories and tags are configured in `config.toml`
- **RSS Feeds**: Atom feeds are automatically generated for categories and tags

## Issues Found

1. **Taxonomy Configuration**: Initially placed under `[markdown.highlighting]` instead of top-level. Fixed.
2. **Template Errors**: Missing taxonomy templates and variable name errors. Fixed.
3. **Broken Links**: 4 external links to GitHub/Mastodon that may need updating.

## Support

For Zola documentation:
- https://www.getzola.org/documentation/

For the migration script:
- Run `./venv/bin/python migrate_wordpress.py --help` (if added)
- Edit the script to customize behavior

For testing:
```bash
./venv/bin/zola serve --port 8080
# Then visit http://localhost:8080
```
