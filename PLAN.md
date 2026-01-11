# Migration and Enhancement Plan

## ✅ Completed Tasks

### Phase 1: WordPress to Zola Migration
- [x] Parse WordPress XML export file
- [x] Extract posts, categories, tags
- [x] Convert HTML content to Markdown
- [x] Create Zola frontmatter for all posts
- [x] Migrate 8 published blog posts
- [x] Skip 3 draft posts
- [x] Create taxonomies (categories, tags)
- [x] Generate redirect mapping (redirects.json)
- [x] Create basic templates

### Phase 2: Terminus Theme Installation
- [x] Clone Terminus theme from GitHub
- [x] Configure theme in config.toml
- [x] Fix theme compatibility with Zola 0.22.0
- [x] Fix Content Security Policy template
- [x] Remove unsupported configuration fields
- [x] Configure menu and social links
- [x] Set up taxonomies with feeds
- [x] Enable Sass compilation
- [x] Test site build
- [x] Verify theme renders correctly

## ✅ Completed Tasks

### Phase 3: Gist Code Inlining
- [x] Create inline_gists.py script
- [x] Scan all blog posts for gist links
- [x] Fetch 12 gist contents from GitHub API
- [x] Replace gist links with inline code blocks
- [x] Preserve language information for syntax highlighting
- [x] Format code blocks using Zola syntax (```)
- [x] Test inline code renders with syntax highlighting

**Result**: 12 Python code blocks from GStreamer post successfully inlined

**Benefits**:
- ✅ Faster page loads (no external gist requests)
- ✅ Better SEO (code is crawlable)
- ✅ Syntax highlighting works offline
- ✅ Code is self-contained in blog
- ✅ No external dependencies for code snippets

### Phase 3.5: Legacy Code Block Conversion
- [x] Create convert_legacy_code_blocks.py script
- [x] Implement intelligent language detection (Python, Rust, Bash, Text)
- [x] Convert 29 legacy [code] blocks to markdown triple backtick format
- [x] Fix critical syntax errors in 2025-11-17 GStreamer post
- [x] Apply appropriate language tags for syntax highlighting
- [x] Validate all conversions (no legacy tags, balanced fences)
- [x] Test build with zola build

**Result**: 29 legacy code blocks converted across 7 blog posts

**Files Updated**:
- 2021-07-08-why-not-just-use-async-python-for-this-api.md (11 blocks: Python, text)
- 2022-06-27-install-gstreamer-srt-plugin-on-macos.md (7 blocks: bash/shell)
- 2022-10-29-a-brief-introduction-to-gstreamer.md (2 blocks: Rust)
- 2023-01-26-decompress-content-using-rust-and-flate2-without-headaches.md (2 blocks: Rust)
- 2023-03-18-readable-rust-combinators-vs-match-clauses.md (3 blocks: Rust)
- 2025-01-11-building-a-cultural-bridge-my-late-night-hack-with-ios-shortcuts-and-ai.md (1 block: text)
- 2025-11-17-learn-by-example-making-it-easier-to-understand-gstreamer.md (3 blocks: Python + syntax fixes)

**Benefits**:
- ✅ All code blocks now use proper markdown format
- ✅ Syntax highlighting enabled on all code snippets
- ✅ Consistent formatting across all blog posts
- ✅ Better readability and maintainability
- ✅ Modern markdown standard compliance

### Phase 3.6: Terminus Shortcode Enhancements
- [x] Research available Terminus theme shortcodes
- [x] Add alert shortcodes for critical warnings and tips (4 alerts)
- [x] Add wide_container shortcodes for complex code examples (2 examples)
- [x] Test shortcodes render correctly

**Shortcodes Applied**:

**Alert Shortcodes** (4 total):
1. **flate2 bug solution** (2023-01-26 post) - Tip alert highlighting MultiGzDecoder solution
2. **iOS prerequisites** (2025-01-11 post) - Note alert for required apps
3. **GStreamer state transitions** (2025-11-17 post) - Important alert about critical concept
4. **Async Python warning** (2021-07-08 post) - Warning alert about blocking calls

**Wide Container Shortcodes** (2 total):
1. **Rust GStreamer example** (2022-10-29 post) - Complete pipeline code
2. **HLS Pipeline example** (2025-11-17 post) - Complex multi-element pipeline

**Benefits**:
- ✅ Critical information stands out with visual alerts
- ✅ Warnings prevent common mistakes and save debugging time
- ✅ Wide containers improve readability of complex code examples
- ✅ Better learning experience with highlighted concepts
- ✅ Professional presentation matching theme design

### Phase 3.7: KaTeX Mathematical Typesetting
- [x] Enable KaTeX in config.toml
- [x] Convert key timing formula to KaTeX block display
- [x] Add inline KaTeX formulas for rate explanations
- [x] Test mathematical rendering

**KaTeX Formulas Added**:
1. **Running time formula** (GStreamer post) - Block display with fraction notation
   - $$running\_time = \frac{position - start}{rate} + base$$
2. **Rate explanations** (GStreamer post) - Inline formulas for playback rates
   - $rate = 1.0$ (normal speed), $rate > 1.0$ (faster), $rate < 1.0$ (slower)
3. **Inline variables** - Enhanced technical terms ($position$, $start$, $rate$, $base$)

**Benefits**:
- ✅ Professional mathematical notation using LaTeX
- ✅ Clear visual presentation of formulas
- ✅ Improved readability of technical content
- ✅ Consistent mathematical typography
- ✅ Better educational value for timing concepts

### Phase 4: Media Management
- [x] Create automated download script
- [x] Download WordPress media files from live site
- [x] Organize images in `static/wp-content/uploads/`
- [x] Verify all images load correctly
- [x] Test site build with images

**Result**: 19 images successfully downloaded and migrated

**Implementation**:
- Created `download_wordpress_images.py` script
- Downloaded all images from https://caricio.com
- Preserved exact directory structure (year/month)
- All image references in blog posts work without modification

**Images Downloaded**:
- **2022/10/**: 12 images (GStreamer diagrams, screenshots)
- **2025/01/**: 1 image (iOS Shortcuts screenshot)
- **2025/11/**: 6 images (GStreamer tutorial diagrams)
- **Total size**: 1.66 MB

**Benefits**:
- ✅ All blog images now self-hosted
- ✅ No dependency on WordPress site
- ✅ Faster page loads (local images)
- ✅ Complete control over media assets
- ✅ Images display correctly in all 5 posts with images

### Phase 4.5: Standalone Pages Migration
- [x] Fetch content from WordPress pages
- [x] Download profile image for About Me page
- [x] Create About Me page structure
- [x] Create Blogroll page structure
- [x] Add pages to navigation menu
- [x] Test pages build and display correctly

**Result**: 2 standalone pages successfully migrated

**Pages Migrated**:
- **About Me** (`/about-me/`) - Personal introduction and topics covered
- **Blogroll** (`/recommended-content/`) - Curated list of blogs and podcasts

**Implementation**:
- Created page directories with `index.md` files
- Preserved WordPress URL structure with trailing slashes
- Downloaded profile image (385 KB) to `static/images/`
- Added pages to main menu in `config.toml`
- Converted content from WordPress to clean Markdown

**Benefits**:
- ✅ Complete site structure with all essential pages
- ✅ Navigation menu includes Blog, About, and Blogroll
- ✅ URLs match WordPress structure for redirects
- ✅ Profile image self-hosted
- ✅ Clean, readable Markdown content

## 📋 Planned Tasks

### Phase 5: Content Enhancement
- [ ] Review migrated posts for formatting issues
- [ ] Fix broken links (4 found during build check)
- [ ] Add table of contents to long posts
- [ ] Update post excerpts
- [ ] Add "read more" markers where appropriate

### Phase 6: Testing & QA
- [ ] Test all blog posts render correctly
- [ ] Verify category pages work
- [ ] Verify tag pages work
- [ ] Test navigation menu
- [ ] Check social links
- [ ] Test mobile responsiveness
- [ ] Run Lighthouse audit
- [ ] Verify atom feeds generate

### Phase 7: Deployment Preparation
- [ ] Set up deployment configuration
- [ ] Configure domain/DNS
- [ ] Set up SSL certificate
- [ ] Configure web server redirects (use redirects.json)
- [ ] Test production build
- [ ] Deploy to production
- [ ] Verify all URLs work

## 📊 Statistics

### Content Migration
- **Total posts found**: 11 (8 published, 3 drafts)
- **Posts migrated**: 8
- **Standalone pages migrated**: 2 (About Me, Blogroll)
- **Categories found**: 8
- **Tags found**: 22
- **Gists linked**: 12 across 1 post
- **Gists inlined**: 12 code blocks successfully inlined
- **Legacy code blocks**: 29 blocks converted across 7 posts
- **Code block languages**: Python (17), Rust (9), Bash (7), Text (7)
- **Images migrated**: 19 images (1.66 MB total)
- **Posts with images**: 5 posts
- **Profile images**: 1 image (385 KB)
- **Total pages**: 10 (8 blog posts + 2 standalone pages)
- **Redirect mappings**: 10 URLs (8 blog posts + 2 pages)

### Site Configuration
- **Theme**: Terminus (dark terminal theme)
- **Zola version**: 0.22.0
- **Syntax highlighting**: Dracula theme (no white space artifacts)
- **Font**: Fira Code
- **CSS framework**: Custom (Terminus)
- **Layout**: Center
- **Feeds**: Atom feeds enabled
- **Search**: Index enabled

### Theme Features
- **Color schemes**: 12 available (Terminus, Tokyo Night, Solarized, etc.)
- **Layout options**: Center, Left, Full-width
- **Social icons**: GitHub, Mastodon, LinkedIn, Email, etc.
- **Navigation**: Responsive hamburger menu
- **Accessibility**: WCAG 2.2 Level AA compliant
- **Lighthouse**: Perfect baseline score

## 🔧 Technical Details

### Zola Configuration
```toml
# Key settings in config.toml
theme = "terminus"
taxonomies = [
    {name = "categories", feed = true},
    {name = "tags", feed = true},
]
compile_sass = true
build_search_index = true
```

### Directory Structure
```
caricio_blog/
├── config.toml              # Site configuration
├── content/
│   ├── _index.md           # Homepage
│   └── blog/
│       ├── _index.md       # Blog section
│       └── *.md           # Blog posts (8 files)
├── static/
│   ├── fonts/              # Theme fonts
│   ├── js/                 # Theme JavaScript
│   ├── css/                # Compiled Sass
│   └── wp-content/
│       └── uploads/      # WordPress media (empty)
├── themes/
│   └── terminus/           # Theme (with CSP fix)
│       └── templates/
│           └── partials/
│               └── content_security_policy.html  # Fixed for Zola 0.22.0
├── templates/
│   └── (old templates)     # Removed, using theme
├── venv/                   # Python virtual environment
├── migrate_wordpress.py     # Migration script
├── inline_gists.py         # Gist inlining script
├── redirects.json           # URL mappings
├── MIGRATION.md            # Migration documentation
└── THEME_INSTALL.md         # Theme installation docs
```

### Migration Script Details
- **Parser**: lxml (robust XML parsing)
- **HTML to Markdown**: html2text library
- **Request handling**: python-requests
- **Date parsing**: Python datetime
- **Taxonomy handling**: Custom logic for categories/tags

## 🎯 Success Criteria

### Phase 3: Gist Inlining
**Complete when**:
- [x] All 12 gist links replaced with inline code
- [x] Code blocks use proper Zola syntax highlighting
- [x] Language information preserved
- [x] No broken links after replacement
- [x] All posts build successfully
- [x] Code renders with syntax highlighting

### Overall Project
**Complete when**:
- [ ] All blog posts reviewed and corrected
- [ ] All media files downloaded and referenced
- [ ] All pages tested (home, blog, categories, tags)
- [ ] Mobile responsiveness verified
- [ ] Lighthouse score > 90 in all categories
- [ ] Redirects configured on server
- [ ] Site deployed to production
- [ ] All URLs from WordPress work correctly

## 📝 Notes

### Theme Compatibility
- Terminus theme requires Zola 0.20.0+
- Using Zola 0.22.0 requires minimal fixes
- Content Security Policy needed modification for `config.markdown.highlight_code` check
- Markdown configuration fields changed in Zola 0.22.0

### Gist Inlining
- GitHub API rate limit: 60 requests/hour (unauthenticated)
- For 12 gists, this is within limits
- Script fetches each gist once and caches in memory
- Gist content is extracted from API response
- Inline code uses markdown code block syntax (```) for Zola

### Performance Considerations
- **Before**: External gist links cause additional HTTP requests
- **After**: Inline code eliminates network requests
- **Estimated improvement**: ~200-500ms faster page loads
- **SEO benefit**: Code is crawlable by search engines

### Maintenance
- **Updating gists**: If gist is updated, need to re-run script
- **New posts**: Add gist links, then run inline_gists.py
- **Rollback**: Git history allows reverting changes

## 🚀 Next Actions

### Immediate (Phase 3)
1. Run `./venv/bin/python inline_gists.py`
2. Review inlined code blocks
3. Test syntax highlighting
4. Commit changes

### Short Term (Phases 4-5)
1. Download and organize media files
2. Review and fix content formatting
3. Test all pages and features
4. Run Lighthouse audit

### Long Term (Phases 6-7)
1. Set up deployment infrastructure
2. Configure redirects
3. Deploy to production
4. Monitor and optimize

## 📚 Documentation

**Migration Details**: `MIGRATION.md`
**Theme Installation**: `THEME_INSTALL.md`
**Theme Customization**: https://github.com/ebkalderon/terminus
**Zola Documentation**: https://www.getzola.org/documentation/

## 🔗 Useful Links

- Terminus Theme: https://github.com/ebkalderon/terminus
- Terminus Demo: https://ebkalderon.github.io/terminus/
- Zola: https://www.getzola.org/
- GitHub Gists: https://gist.github.com/rafaelcaricio/
- Giallo (syntax highlighting): https://github.com/getzola/giallo
