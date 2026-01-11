#!/usr/bin/env python3
"""
Convert legacy [code]...[/code] blocks to markdown triple backtick format
with automatic language detection and syntax highlighting support.
"""

import re
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Configuration
BLOG_DIR = Path("content/blog")

# Language detection patterns
PYTHON_PATTERNS = [
    r'^\s*import\s+',
    r'^\s*from\s+.+\s+import',
    r'^\s*def\s+\w+',
    r'^\s*class\s+\w+',
    r'^\s*async\s+def',
    r'^#!/usr/bin/env python',
    r'@app\.(get|post|put|delete)',
    r'^\s*async\s+with',
]

RUST_PATTERNS = [
    r'^\s*use\s+std::',
    r'^\s*fn\s+\w+',
    r'^\s*let\s+\w+',
    r'^\s*impl\s+',
    r'^\s*pub\s+(fn|struct|enum)',
    r'::\s*unwrap\(\)',
    r'\.\s*ok\(\)',
    r'\.\s*map\(',
]

BASH_PATTERNS = [
    r'\$\s+(brew|gst-launch|gst-inspect|http|uvicorn)',  # Commands starting with $
    r'^\s*brew\s+',
    r'^\s*gst-launch',
    r'^\s*gst-inspect',
    r'depends_on\s+"',  # Homebrew formula patterns
]

TEXT_PATTERNS = [
    r'^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}',  # Timestamps
    r'^\s*[├│└]',  # Tree structures
    r'WARNING:',
    r'<Response\s+\[',
    r'#\s+file\s+',  # File comments
]


def parse_frontmatter(content: str) -> Dict[str, any]:
    """Extract frontmatter metadata for context"""
    match = re.match(r'^\+\+\+\s*\n(.*?)\n\+\+\+', content, re.DOTALL)
    if not match:
        return {}

    frontmatter = {}
    for line in match.group(1).split('\n'):
        if '=' in line:
            key, value = line.split('=', 1)
            frontmatter[key.strip()] = value.strip().strip('"[]')

    return frontmatter


def detect_language_from_context(filepath: Path, frontmatter: Dict) -> Optional[str]:
    """Try to detect language from file context (filename, tags, categories)"""
    filename = filepath.name.lower()

    # Check file title/name
    if 'python' in filename or 'fastapi' in filename:
        return 'python'
    if 'rust' in filename:
        return 'rust'

    # Check frontmatter
    categories = frontmatter.get('categories', '').lower()
    tags = frontmatter.get('tags', '').lower()

    if 'python' in categories or 'python' in tags or 'fastapi' in tags:
        return 'python'
    if 'rust' in categories or 'rust' in tags:
        return 'rust'

    return None


def detect_language_from_content(code: str) -> Optional[str]:
    """Detect programming language from code content patterns"""
    # Clean up whitespace for analysis
    code_lines = [line for line in code.strip().split('\n') if line.strip()]

    if not code_lines:
        return None

    # Check for text/output patterns first (higher priority)
    for pattern in TEXT_PATTERNS:
        if any(re.search(pattern, line) for line in code_lines[:5]):
            return 'text'

    # Check Python patterns
    python_score = 0
    for pattern in PYTHON_PATTERNS:
        if any(re.search(pattern, line) for line in code_lines):
            python_score += 1

    # Check Rust patterns
    rust_score = 0
    for pattern in RUST_PATTERNS:
        if any(re.search(pattern, line) for line in code_lines):
            rust_score += 1

    # Check Bash patterns
    bash_score = 0
    for pattern in BASH_PATTERNS:
        if any(re.search(pattern, line) for line in code_lines):
            bash_score += 1

    # Return language with highest score
    scores = [
        ('python', python_score),
        ('rust', rust_score),
        ('bash', bash_score),
    ]

    max_lang, max_score = max(scores, key=lambda x: x[1])

    if max_score >= 2:  # Require at least 2 pattern matches
        return max_lang

    return None


def detect_language(code: str, context: Dict) -> str:
    """Detect programming language using context and content analysis"""
    # Try context first
    context_lang = detect_language_from_context(
        context.get('filepath'),
        context.get('frontmatter', {})
    )

    # Try content analysis
    content_lang = detect_language_from_content(code)

    # Prefer content detection, but use context as fallback
    if content_lang:
        return content_lang
    elif context_lang:
        return context_lang
    else:
        # No clear detection - return empty string for plain code block
        return ''


def find_code_blocks(content: str) -> List[Dict]:
    """Find all [code]...[/code] blocks with positions"""
    blocks = []
    pattern = r'\[code\]\s*\n(.*?)\[/code\]'

    for match in re.finditer(pattern, content, re.DOTALL):
        blocks.append({
            'start': match.start(),
            'end': match.end(),
            'content': match.group(1).rstrip(),  # Remove trailing whitespace
            'full_match': match.group(0),
        })

    return blocks


def convert_code_block(code: str, language: str) -> str:
    """Convert code content to markdown format with language tag"""
    if language:
        return f"```{language}\n{code}\n```"
    else:
        return f"```\n{code}\n```"


def fix_syntax_errors_gstreamer_post(content: str) -> str:
    """Apply specific syntax fixes for 2025-11-17 GStreamer post"""
    # Fix 1: Line 1046 - broken link with embedded code fence
    # Pattern: Or [using the actual GStreamer bindings for Python](```python
    pattern1 = r'Or \[using the actual GStreamer bindings for Python\]\(```python'
    replacement1 = 'Or using the actual GStreamer bindings for Python:\n\n```python'
    content = re.sub(pattern1, replacement1, content)

    # Fix 2: Line 1137 - stray closing backticks after code block
    # Look for pattern where ``` is followed immediately by ).
    pattern2 = r'```\n\)\.'
    replacement2 = '```\n\n).'
    content = re.sub(pattern2, replacement2, content)

    return content


def validate_conversion(original: str, converted: str) -> List[str]:
    """Validate that conversion was successful and safe"""
    issues = []

    # Check all [code] tags removed
    if '[code]' in converted.lower():
        issues.append("Legacy [code] tags still present")

    if '[/code]' in converted.lower():
        issues.append("Legacy [/code] tags still present")

    # Check fence balance
    fence_count = converted.count('```')
    if fence_count % 2 != 0:
        issues.append(f"Unbalanced code fences: {fence_count} backticks")

    # Check content preservation (rough check)
    orig_lines = len(original.split('\n'))
    conv_lines = len(converted.split('\n'))
    line_diff = abs(orig_lines - conv_lines)

    if line_diff > 15:  # Allow some variance for reformatting
        issues.append(f"Line count changed significantly: {orig_lines} -> {conv_lines} (diff: {line_diff})")

    return issues


def process_file(filepath: Path, dry_run: bool = False, verbose: bool = False) -> Tuple[bool, int, List[str]]:
    """Process a single blog post file"""
    print(f"\nProcessing: {filepath.name}")

    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()

    # Parse frontmatter for context
    frontmatter = parse_frontmatter(original)
    context = {
        'filepath': filepath,
        'frontmatter': frontmatter,
    }

    # Find legacy code blocks
    blocks = find_code_blocks(original)

    if not blocks:
        print("  No legacy code blocks found")
        return False, 0, []

    print(f"  Found {len(blocks)} legacy code block(s)")

    # Convert content
    converted = original

    # Process blocks in reverse order to preserve positions
    for block in reversed(blocks):
        code = block['content']
        language = detect_language(code, context)
        new_block = convert_code_block(code, language)

        if verbose:
            lang_display = language if language else '(none)'
            print(f"    Block at pos {block['start']}: detected as '{lang_display}'")

        # Replace the entire [code]...[/code] block
        converted = (
            converted[:block['start']] +
            new_block +
            converted[block['end']:]
        )

    # Apply file-specific syntax fixes
    if '2025-11-17' in filepath.name:
        print("  Applying syntax fixes for GStreamer post")
        converted = fix_syntax_errors_gstreamer_post(converted)

    # Validate conversion
    issues = validate_conversion(original, converted)

    if issues:
        print(f"  ✗ Validation issues:")
        for issue in issues:
            print(f"    - {issue}")
        return False, 0, issues

    # Write or preview
    if dry_run:
        print("  [DRY RUN] Would convert blocks:")
        for block in blocks:
            lang = detect_language(block['content'], context)
            lang_display = lang if lang else '(none)'
            preview = block['content'][:50].replace('\n', ' ')
            print(f"    - Language: {lang_display} | Preview: {preview}...")
    else:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(converted)
        print(f"  ✓ Converted {len(blocks)} block(s) successfully")

    return True, len(blocks), []


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Convert legacy [code] blocks to markdown format with language tags'
    )
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be converted without modifying files')
    parser.add_argument('--file', type=str,
                        help='Process only the specified file (filename only, not path)')
    parser.add_argument('--all', action='store_true',
                        help='Process all markdown files in blog directory')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Show detailed language detection information')

    args = parser.parse_args()

    print("=" * 70)
    print("Legacy Code Block Converter")
    print("=" * 70)

    if args.dry_run:
        print("\n** DRY RUN MODE - No files will be modified **\n")

    # Determine files to process
    if args.file:
        # Single file mode
        filepath = BLOG_DIR / args.file
        if not filepath.exists():
            print(f"Error: File not found: {filepath}")
            return
        files = [filepath]
    elif args.all:
        # All files mode
        files = sorted(BLOG_DIR.glob("*.md"))
    else:
        # Default: known files with legacy blocks (from exploration)
        known_files = [
            "2021-07-08-why-not-just-use-async-python-for-this-api.md",
            "2022-10-29-a-brief-introduction-to-gstreamer.md",
            "2022-06-27-install-gstreamer-srt-plugin-on-macos.md",
            "2023-01-26-decompress-content-using-rust-and-flate2-without-headaches.md",
            "2023-03-18-readable-rust-combinators-vs-match-clauses.md",
            "2025-01-11-building-a-cultural-bridge-my-late-night-hack-with-ios-shortcuts-and-ai.md",
            "2025-11-17-learn-by-example-making-it-easier-to-understand-gstreamer.md",
        ]
        files = [BLOG_DIR / f for f in known_files if (BLOG_DIR / f).exists()]

    if not files:
        print(f"No markdown files found to process")
        return

    print(f"Found {len(files)} file(s) to process\n")

    # Process each file
    total_files = 0
    total_blocks = 0
    failed_files = []

    for filepath in files:
        success, block_count, issues = process_file(filepath, args.dry_run, args.verbose)
        if success:
            total_files += 1
            total_blocks += block_count
        elif issues:
            failed_files.append((filepath.name, issues))

    # Summary
    print("\n" + "=" * 70)
    if args.dry_run:
        print("DRY RUN COMPLETE - No files were modified")
    else:
        print("CONVERSION COMPLETE")
    print("=" * 70)
    print(f"Files processed: {total_files}")
    print(f"Total blocks converted: {total_blocks}")

    if failed_files:
        print(f"\nFailed files: {len(failed_files)}")
        for filename, issues in failed_files:
            print(f"  - {filename}: {', '.join(issues)}")

    if not args.dry_run and total_blocks > 0:
        print("\nNext steps:")
        print("  1. Review changes: git diff content/blog/")
        print("  2. Verify no legacy tags: grep -r '\\[code\\]' content/blog/")
        print("  3. Test build: zola build")
        print("  4. Preview site: zola serve")


if __name__ == "__main__":
    main()
