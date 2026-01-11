# Terminus Theme Installation - Complete

## What Was Done

✅ **Terminus theme** installed from https://github.com/ebkalderon/terminus
✅ **Configuration updated** for Terminus theme compatibility
✅ **Site builds successfully** with Terminus theme
✅ **Content Security Policy template fixed** for Zola 0.22.0 compatibility

## Theme Features Enabled

- Dark retro terminal-like color scheme
- Mobile-first responsive design
- Social media links (GitHub configured)
- Menu navigation (Blog link)
- Perfect baseline Lighthouse score
- Fira Code font for code blocks
- Copy-to-clipboard buttons for code blocks

## Configuration Details

### Theme Settings
- **Layout**: Center
- **Color Scheme**: Terminus (dark)
- **Feed Generation**: Enabled
- **Sass Compilation**: Enabled
- **Search Index**: Enabled

### Taxonomies
- **Categories**: Feed enabled
- **Tags**: Feed enabled

### Social Links
- GitHub: https://github.com/rafaelcaricio

### Navigation Menu
- Blog (/blog)

## Compatibility Issues Fixed

### Content Security Policy Template
**Issue**: Theme template checked for `config.markdown.highlight_code` which doesn't exist in Zola 0.22.0

**Fix**: Modified `themes/terminus/templates/partials/content_security_policy.html` to:
1. Always allow inline styles (syntax highlighting always enabled in Terminus)
2. Removed dynamic check for `config.markdown.highlight_code`
3. Added temporary compatibility note

### Configuration Cleanup
**Issue**: Theme's `config.toml` included fields not supported by Zola 0.22.0:
- `highlight_code` (under `[markdown]`)
- `bottom_footnotes` (top-level)
- `github_alerts` (top-level)

**Fix**: Removed unsupported configuration fields to ensure Zola 0.22.0 compatibility

## Site Structure

```
caricio_blog/
├── config.toml                 # Updated for Terminus theme
├── content/
│   ├── _index.md              # Home page
│   └── blog/
│       ├── _index.md          # Blog section index
│       └── *.md               # 8 migrated posts
├── static/
│   └── wp-content/
│       └── uploads/          # Media directory
├── themes/
│   └── terminus/             # Terminus theme (with fix)
│       └── templates/
│           └── partials/
│               └── content_security_policy.html  # Fixed for Zola 0.22.0
├── migrate_wordpress.py        # Migration script
├── redirects.json            # URL redirect mapping
└── THEME_INSTALL.md          # This file
```

## Testing

### Build Site
```bash
zola build
```

**Result**: ✅ Site builds successfully (8 pages, 1 section)

### Serve Locally
```bash
zola serve
```

**Result**: ✅ Site renders correctly with Terminus theme

**Features Verified**:
- Dark terminal aesthetic
- Fira Code font loading
- Responsive menu
- Blog listing on homepage
- Post navigation
- Social links in footer

## What's Different

### Before (Basic Templates)
- Plain HTML without styling
- No theme
- Basic navigation
- Manual configuration needed

### After (Terminus Theme)
- Styled terminal-like appearance
- Fira Code font for beautiful typography
- Built-in responsive menu
- Code syntax highlighting ready
- SEO meta tags (OpenGraph)
- Atom feeds for categories/tags
- Copy-to-clipboard for code blocks

## Next Steps

### 1. Customize Theme
Terminus is highly customizable via `config.toml`:

#### Color Schemes
Available themes: "terminus", "tokyo-night", "solarized-dark", "nord",
"one-dark", "gruvbox-dark", "oled-abyss", "solar-flare", 
"catppuccin-latte", "catppuccin-frappe", "catppuccin-macchiato", "catppuccin-mocha"

```toml
[extra]
color_scheme = "catppuccin-mocha"
```

#### Menu Items
Add more navigation links:

```toml
[[extra.main_menu]]
name = "About"
url = "about"

[[extra.main_menu]]
name = "Archive"
url = "archive"
```

#### Social Media
Add more social links:

```toml
[[extra.socials]]
name = "mastodon"
url = "https://mastodon.social/@rafaelcaricio"

[[extra.socials]]
name = "linkedin"
url = "https://linkedin.com/in/rafaelcaricio"
```

#### Layout Options
- `center` (default) - Centered content
- `left` - Left-aligned content
- `full-width` - Full-width content

```toml
[extra]
layout = "full-width"
```

#### Favicon
Use emoji favicon:

```toml
[extra]
favicon_emoji = "👨‍💻"
```

Or custom image:

```toml
[extra]
favicon = "images/favicon.png"
```

### 2. Download Media Files
WordPress media needs to be downloaded to `static/wp-content/uploads/`:

```bash
# Option A: Manual download
# Visit your WordPress media library and download images
# Place in static/wp-content/uploads/ with correct paths

# Option B: WP-CLI on WordPress server
wp media export --dir=wp-exported-media
# Then copy to static/wp-content/uploads/
```

### 3. Add More Content
Create additional pages:

```bash
# About page
content/about.md

# Archive page
content/archive.md
```

### 4. Deploy
When ready to deploy:

```bash
zola build
# Deploy public/ directory to your host
```

Popular deployment options:
- **Netlify**: `netlify deploy --dir=public`
- **GitHub Pages**: Push to gh-pages branch
- **Vercel**: `vercel deploy public`
- **Cloudflare Pages**: `wrangler pages deploy public`
- **AWS S3**: `aws s3 sync public/ s3://bucket-name`

See: https://www.getzola.org/documentation/deployment/overview/

### 5. Implement Redirects
Use `redirects.json` to set up redirects for old WordPress URLs.

**Example Nginx redirect map**:
```nginx
map $request_uri $redirect_uri {
    include redirects.json;
    default "";
}
```

**Example Netlify _redirects file**:
```text
/why-not-just-use-async-python-for-this-api/ /blog/2021-07-08-why-not-just-use-async-python-for-this-api/ 301
/a-brief-introduction-to-gstreamer/ /blog/2022-10-29-a-brief-introduction-to-gstreamer/ 301
```

## Theme Documentation

Full Terminus theme documentation:
- **Demo**: https://ebkalderon.github.io/terminus/
- **Features**: https://github.com/ebkalderon/terminus#features
- **Configuration**: https://github.com/ebkalderon/terminus#configuration
- **Shortcodes**: https://ebkalderon.github.io/terminus/blog/shortcodes/

## Important Notes

### Zola Version Compatibility
- Terminus theme developed for Zola 0.20.0+
- Currently using Zola 0.22.0
- Minor template modifications needed for compatibility

### Syntax Highlighting
- Zola uses Giallo library for syntax highlighting
- Terminus expects `highlight_code` configuration (not standard in Zola 0.22.0)
- Workaround: CSS policy always allows inline styles for syntax highlighting
- Theme provides `monokai` highlighting theme

### Content Security Policy
- CSP is enabled for security
- Allows inline styles (for syntax highlighting)
- Configured to allow self resources
- Can be customized further in `config.toml`

## Testing Checklist

- [x] Site builds without errors
- [x] Homepage displays correctly
- [x] Blog listing works
- [x] Individual blog posts render
- [x] Navigation menu functional
- [x] Social links present
- [x] Fira Code font loads
- [x] Dark theme applies
- [x] Responsive design (test on mobile)
- [ ] Media images display (need to download)
- [ ] Category pages work
- [ ] Tag pages work
- [ ] Atom feeds generate correctly
- [ ] Search functionality

## Support

### Zola Documentation
https://www.getzola.org/documentation/

### Terminus Theme Support
https://github.com/ebkalderon/terminus/issues

### WordPress Migration
See `MIGRATION.md` for migration details and script usage.

## Summary

Your Zola blog is now running with the Terminus theme! The site:
- Has 8 migrated blog posts
- Uses a professional dark terminal theme
- Is ready for deployment
- Needs media files to be downloaded
- May need additional customization

The combination of WordPress migration + Terminus theme gives you a modern, fast, and
beautiful static blog with excellent SEO and accessibility.
