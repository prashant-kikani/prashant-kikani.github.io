"""
Script to parse all .markdown files in _posts/ and generate a JSON file
with title, URL, permalink, keywords, and description for each post.

Usage: python generate_posts_json.py
"""

import os
import json
import re
import glob

POSTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_posts")
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "posts_data.json")
BASE_URL = "https://prashantkikani.com"


def parse_frontmatter(filepath):
    """Parse YAML frontmatter from a markdown file."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract frontmatter between --- delimiters
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None

    frontmatter_text = match.group(1)
    data = {}

    # Parse title (handles quotes)
    title_match = re.search(r'title:\s*"(.+?)"', frontmatter_text)
    if title_match:
        data["title"] = title_match.group(1)

    # Parse date
    date_match = re.search(r"date:\s*(\S+)", frontmatter_text)
    if date_match:
        data["date"] = date_match.group(1)

    # Parse permalink (handles quotes)
    permalink_match = re.search(r'permalink:\s*"(.+?)"', frontmatter_text)
    if permalink_match:
        data["permalink"] = permalink_match.group(1)
        data["url"] = BASE_URL + permalink_match.group(1)

    # Parse keywords (comma-separated)
    keyword_match = re.search(r"keyword:\s*(.+)", frontmatter_text)
    if keyword_match:
        raw_keywords = keyword_match.group(1).strip()
        data["keywords"] = [k.strip() for k in raw_keywords.split(",") if k.strip()]

    # Parse description (handles escaped quotes like \")
    desc_match = re.search(r'description:\s*"((?:[^"\\]|\\.)*)"', frontmatter_text)
    if desc_match:
        data["description"] = desc_match.group(1).replace('\\"', '"')

    return data


def main():
    markdown_files = sorted(glob.glob(os.path.join(POSTS_DIR, "*.markdown")))
    posts = []

    for filepath in markdown_files:
        filename = os.path.basename(filepath)
        data = parse_frontmatter(filepath)
        if data:
            data["filename"] = filename
            posts.append(data)
        else:
            print(f"Warning: Could not parse frontmatter from {filename}")

    # Sort by date descending (newest first)
    posts.sort(key=lambda x: x.get("date", ""), reverse=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)

    print(f"Generated {OUTPUT_FILE} with {len(posts)} posts.")


if __name__ == "__main__":
    main()
