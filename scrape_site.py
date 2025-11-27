#!/usr/bin/env python3
"""
Script to scrape skullspace.ca WordPress site and convert to Hugo format.
Downloads all images and converts content to Markdown.
"""

import os
import re
import sys
import time
import urllib.parse
from pathlib import Path
from urllib.parse import urljoin, urlparse

import html2text
import requests
from bs4 import BeautifulSoup

# Configuration
BASE_URL = "https://skullspace.ca"
OUTPUT_DIR = Path(__file__).parent
CONTENT_DIR = OUTPUT_DIR / "content"
STATIC_DIR = OUTPUT_DIR / "static"
IMAGES_DIR = STATIC_DIR / "img"

# Create directories
CONTENT_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)
IMAGES_DIR.mkdir(exist_ok=True, parents=True)

# Session for connection pooling
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
})

# Track downloaded images to avoid duplicates
downloaded_images = {}
downloaded_urls = set()


def sanitize_filename(filename):
    """Sanitize filename for filesystem."""
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '-', filename)
    filename = filename.strip('. ')
    return filename[:200]  # Limit length


def download_image(img_url, page_slug=""):
    """Download an image and return the local path."""
    if img_url in downloaded_images:
        return downloaded_images[img_url]
    
    try:
        # Make absolute URL
        if not img_url.startswith('http'):
            img_url = urljoin(BASE_URL, img_url)
        
        # Parse URL to get filename
        parsed = urlparse(img_url)
        filename = os.path.basename(parsed.path)
        
        # If no filename, generate one
        if not filename or '.' not in filename:
            ext = 'jpg'  # default
            if 'png' in img_url.lower():
                ext = 'png'
            elif 'gif' in img_url.lower():
                ext = 'gif'
            elif 'svg' in img_url.lower():
                ext = 'svg'
            filename = f"image_{hash(img_url) % 10000}.{ext}"
        
        filename = sanitize_filename(filename)
        
        # Create subdirectory based on page if provided
        if page_slug:
            page_img_dir = IMAGES_DIR / page_slug
            page_img_dir.mkdir(exist_ok=True, parents=True)
            local_path = page_img_dir / filename
            hugo_path = f"/img/{page_slug}/{filename}"
        else:
            local_path = IMAGES_DIR / filename
            hugo_path = f"/img/{filename}"
        
        # Skip if already downloaded
        if local_path.exists():
            downloaded_images[img_url] = hugo_path
            return hugo_path
        
        # Download image
        print(f"  Downloading image: {img_url}")
        response = session.get(img_url, timeout=30, stream=True)
        response.raise_for_status()
        
        # Save image
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        downloaded_images[img_url] = hugo_path
        time.sleep(0.5)  # Be polite
        return hugo_path
        
    except Exception as e:
        print(f"  Error downloading image {img_url}: {e}")
        return img_url  # Return original URL if download fails


def html_to_markdown(html_content, page_slug=""):
    """Convert HTML to Markdown, handling images."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Download and replace images
    for img in soup.find_all('img'):
        src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
        if src:
            local_path = download_image(src, page_slug)
            img['src'] = local_path
    
    # Use html2text for better conversion
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.body_width = 0  # Don't wrap lines
    h.unicode_snob = True
    
    # Convert to markdown
    markdown = h.handle(str(soup))
    
    # Clean up
    markdown = re.sub(r'\n{3,}', r'\n\n', markdown)
    markdown = markdown.strip()
    
    return markdown


def get_page_content(url):
    """Fetch and parse a page."""
    if url in downloaded_urls:
        return None
    
    try:
        print(f"Fetching: {url}")
        response = session.get(url, timeout=30)
        response.raise_for_status()
        downloaded_urls.add(url)
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def extract_links(html):
    """Extract all internal links from HTML."""
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('/') or BASE_URL in href:
            if BASE_URL in href:
                links.add(href)
            else:
                links.add(urljoin(BASE_URL, href))
    
    return links


def create_hugo_content(title, content, url, content_type="page", date=None):
    """Create a Hugo content file."""
    # Generate slug from URL
    parsed = urlparse(url)
    slug = parsed.path.strip('/').replace('/', '-') or 'index'
    slug = sanitize_filename(slug)
    
    # Determine file path
    if content_type == "post":
        file_path = CONTENT_DIR / "posts" / f"{slug}.md"
        (CONTENT_DIR / "posts").mkdir(exist_ok=True)
    else:
        file_path = CONTENT_DIR / f"{slug}.md"
    
    # Front matter
    front_matter = f"""+++
title = "{title.replace('"', '\\"')}"
date = "{date or '2025-01-01'}"
draft = false
+++

"""
    
    # Write file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(front_matter)
        f.write(content)
    
    print(f"Created: {file_path}")
    return slug


def scrape_site():
    """Main scraping function."""
    print("Starting scrape of skullspace.ca...")
    
    # Start with homepage and common blog/post URLs
    to_visit = {
        BASE_URL,
        f"{BASE_URL}/blog/",
        f"{BASE_URL}/posts/",
        f"{BASE_URL}/category/",
        f"{BASE_URL}/tag/",
    }
    visited = set()
    
    while to_visit:
        url = to_visit.pop()
        
        if url in visited:
            continue
        
        visited.add(url)
        
        # Skip non-HTML content
        if any(url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.zip']):
            continue
        
        html = get_page_content(url)
        if not html:
            continue
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract title
        title_tag = soup.find('title')
        title = title_tag.get_text().strip() if title_tag else "Untitled"
        title = title.replace(' | SkullSpace', '').replace('SkullSpace - ', '').strip()
        
        # Extract main content
        # Try common WordPress content selectors
        content_selectors = [
            'article',
            '.entry-content',
            '.post-content',
            '.content',
            'main',
            '#content',
            '.main-content'
        ]
        
        content_html = None
        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                content_html = str(content_elem)
                break
        
        if not content_html:
            # Fallback to body
            body = soup.find('body')
            if body:
                # Remove nav, header, footer
                for tag in body.find_all(['nav', 'header', 'footer', 'script', 'style']):
                    tag.decompose()
                content_html = str(body)
        
        # Convert to markdown
        slug = urlparse(url).path.strip('/').replace('/', '-') or 'index'
        slug = sanitize_filename(slug)
        content_md = html_to_markdown(content_html, slug)
        
        # Determine if it's a post or page (simple heuristic)
        is_post = any(word in url.lower() for word in ['/blog/', '/post/', '/news/', '/article/'])
        content_type = "post" if is_post else "page"
        
        # Extract date if available
        date = None
        date_elem = soup.find('time') or soup.find(class_=re.compile('date|published'))
        if date_elem:
            datetime_attr = date_elem.get('datetime') or date_elem.get_text()
            if datetime_attr:
                date = datetime_attr[:10]  # YYYY-MM-DD
        
        # Create Hugo content file
        create_hugo_content(title, content_md, url, content_type, date)
        
        # Extract links to visit
        new_links = extract_links(html)
        for link in new_links:
            if BASE_URL in link and link not in visited:
                to_visit.add(link)
        
        time.sleep(1)  # Be polite to the server
    
    print(f"\nScraping complete!")
    print(f"Visited {len(visited)} pages")
    print(f"Downloaded {len(downloaded_images)} images")


if __name__ == "__main__":
    try:
        scrape_site()
    except KeyboardInterrupt:
        print("\nScraping interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

