#!/usr/bin/env python3
"""
Screenshot Link Extractor

This script extracts URLs from screenshots using OCR, verifies they are working,
and aggregates them into a clickable document (Markdown or HTML).

Requirements:
    pip install pytesseract pillow requests

System requirements:
    - Tesseract OCR must be installed on your system
    - Ubuntu/Debian: sudo apt-get install tesseract-ocr
    - macOS: brew install tesseract
    - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
"""

import argparse
import re
import sys
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple, Optional
from dataclasses import dataclass
from urllib.parse import urlparse

try:
    import pytesseract
    from PIL import Image
    import requests
except ImportError as e:
    print(f"Missing required package: {e}")
    print("Please install requirements: pip install pytesseract pillow requests")
    sys.exit(1)


@dataclass
class LinkInfo:
    """Stores information about an extracted link."""
    url: str
    title: Optional[str]
    is_valid: bool
    status_code: Optional[int]
    error_message: Optional[str]


class ScreenshotLinkExtractor:
    """Extracts and validates links from screenshot images."""

    # Regex pattern for matching URLs
    URL_PATTERN = re.compile(
        r'https?://[^\s<>"\')\]]+',
        re.IGNORECASE
    )

    # Common image extensions
    SUPPORTED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp'}

    def __init__(self, timeout: int = 10, verify_ssl: bool = True):
        """
        Initialize the extractor.

        Args:
            timeout: HTTP request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def extract_text_from_image(self, image_path: str) -> str:
        """
        Extract text from an image using OCR.

        Args:
            image_path: Path to the image file

        Returns:
            Extracted text from the image
        """
        try:
            image = Image.open(image_path)
            # Use pytesseract to extract text
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            print(f"Error extracting text from {image_path}: {e}")
            return ""

    def extract_urls_from_text(self, text: str) -> List[str]:
        """
        Extract URLs from text using regex.

        Args:
            text: Text to search for URLs

        Returns:
            List of found URLs
        """
        urls = self.URL_PATTERN.findall(text)
        # Clean up URLs (remove trailing punctuation)
        cleaned_urls = []
        for url in urls:
            # Remove trailing punctuation that might have been captured
            url = url.rstrip('.,;:!?)\'"]')
            if url and self._is_valid_url_format(url):
                cleaned_urls.append(url)
        return list(dict.fromkeys(cleaned_urls))  # Remove duplicates while preserving order

    def _is_valid_url_format(self, url: str) -> bool:
        """Check if URL has valid format."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    def verify_link(self, url: str) -> LinkInfo:
        """
        Verify if a link is working.

        Args:
            url: URL to verify

        Returns:
            LinkInfo object with verification results
        """
        try:
            response = self.session.head(
                url,
                timeout=self.timeout,
                allow_redirects=True,
                verify=self.verify_ssl
            )
            # Some servers don't support HEAD, try GET if we get 405
            if response.status_code == 405:
                response = self.session.get(
                    url,
                    timeout=self.timeout,
                    allow_redirects=True,
                    verify=self.verify_ssl,
                    stream=True  # Don't download the full content
                )

            is_valid = response.status_code < 400
            return LinkInfo(
                url=url,
                title=self._extract_title_from_url(url),
                is_valid=is_valid,
                status_code=response.status_code,
                error_message=None if is_valid else f"HTTP {response.status_code}"
            )
        except requests.exceptions.SSLError:
            return LinkInfo(
                url=url,
                title=self._extract_title_from_url(url),
                is_valid=False,
                status_code=None,
                error_message="SSL certificate error"
            )
        except requests.exceptions.ConnectionError:
            return LinkInfo(
                url=url,
                title=self._extract_title_from_url(url),
                is_valid=False,
                status_code=None,
                error_message="Connection failed"
            )
        except requests.exceptions.Timeout:
            return LinkInfo(
                url=url,
                title=self._extract_title_from_url(url),
                is_valid=False,
                status_code=None,
                error_message="Request timed out"
            )
        except Exception as e:
            return LinkInfo(
                url=url,
                title=self._extract_title_from_url(url),
                is_valid=False,
                status_code=None,
                error_message=str(e)
            )

    def _extract_title_from_url(self, url: str) -> str:
        """Generate a title from the URL."""
        parsed = urlparse(url)
        # Try to create a readable title from the path
        path = parsed.path.strip('/')
        if path:
            # Get the last meaningful part of the path
            parts = [p for p in path.split('/') if p]
            if parts:
                title = parts[-1]
                # Remove file extensions
                title = re.sub(r'\.[^.]+$', '', title)
                # Replace separators with spaces
                title = re.sub(r'[-_]', ' ', title)
                return title.title()
        return parsed.netloc

    def verify_links_parallel(self, urls: List[str], max_workers: int = 5) -> List[LinkInfo]:
        """
        Verify multiple links in parallel.

        Args:
            urls: List of URLs to verify
            max_workers: Maximum number of parallel workers

        Returns:
            List of LinkInfo objects
        """
        results = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {executor.submit(self.verify_link, url): url for url in urls}
            for future in as_completed(future_to_url):
                result = future.result()
                results.append(result)
                status = "✓" if result.is_valid else "✗"
                print(f"  [{status}] {result.url}")

        # Sort results to maintain original order
        url_to_result = {r.url: r for r in results}
        return [url_to_result[url] for url in urls if url in url_to_result]

    def process_screenshots(self, image_paths: List[str], verify: bool = True) -> List[LinkInfo]:
        """
        Process multiple screenshots and extract/verify links.

        Args:
            image_paths: List of paths to screenshot images
            verify: Whether to verify links

        Returns:
            List of LinkInfo objects
        """
        all_urls = []

        for image_path in image_paths:
            print(f"\nProcessing: {image_path}")
            text = self.extract_text_from_image(image_path)
            urls = self.extract_urls_from_text(text)
            print(f"  Found {len(urls)} URLs")
            all_urls.extend(urls)

        # Remove duplicates across all images
        unique_urls = list(dict.fromkeys(all_urls))
        print(f"\nTotal unique URLs found: {len(unique_urls)}")

        if verify and unique_urls:
            print("\nVerifying links...")
            return self.verify_links_parallel(unique_urls)
        else:
            return [LinkInfo(url=url, title=self._extract_title_from_url(url),
                          is_valid=True, status_code=None, error_message=None)
                    for url in unique_urls]


class DocumentGenerator:
    """Generates clickable documents from link information."""

    @staticmethod
    def generate_markdown(links: List[LinkInfo], include_invalid: bool = False) -> str:
        """
        Generate a Markdown document with clickable links.

        Args:
            links: List of LinkInfo objects
            include_invalid: Whether to include invalid links

        Returns:
            Markdown formatted string
        """
        lines = [
            "# Extracted Links",
            "",
            f"Total links found: {len(links)}",
            ""
        ]

        valid_links = [l for l in links if l.is_valid]
        invalid_links = [l for l in links if not l.is_valid]

        if valid_links:
            lines.extend([
                "## Working Links",
                "",
            ])
            for link in valid_links:
                status = f" (HTTP {link.status_code})" if link.status_code else ""
                lines.append(f"- [{link.title or link.url}]({link.url}){status}")
            lines.append("")

        if include_invalid and invalid_links:
            lines.extend([
                "## Invalid/Broken Links",
                "",
            ])
            for link in invalid_links:
                error = f" - {link.error_message}" if link.error_message else ""
                lines.append(f"- ~~[{link.title or link.url}]({link.url})~~{error}")
            lines.append("")

        return "\n".join(lines)

    @staticmethod
    def generate_html(links: List[LinkInfo], include_invalid: bool = False) -> str:
        """
        Generate an HTML document with clickable links.

        Args:
            links: List of LinkInfo objects
            include_invalid: Whether to include invalid links

        Returns:
            HTML formatted string
        """
        valid_links = [l for l in links if l.is_valid]
        invalid_links = [l for l in links if not l.is_valid]

        html_parts = [
            "<!DOCTYPE html>",
            "<html lang='en'>",
            "<head>",
            "    <meta charset='UTF-8'>",
            "    <meta name='viewport' content='width=device-width, initial-scale=1.0'>",
            "    <title>Extracted Links</title>",
            "    <style>",
            "        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }",
            "        h1 { color: #333; }",
            "        h2 { color: #666; margin-top: 30px; }",
            "        ul { list-style-type: none; padding: 0; }",
            "        li { margin: 10px 0; padding: 10px; background: #f5f5f5; border-radius: 5px; }",
            "        a { color: #0066cc; text-decoration: none; }",
            "        a:hover { text-decoration: underline; }",
            "        .invalid { background: #ffebee; }",
            "        .invalid a { color: #c62828; text-decoration: line-through; }",
            "        .status { color: #888; font-size: 0.9em; }",
            "        .error { color: #c62828; font-size: 0.9em; }",
            "    </style>",
            "</head>",
            "<body>",
            f"    <h1>Extracted Links</h1>",
            f"    <p>Total links found: {len(links)}</p>",
        ]

        if valid_links:
            html_parts.extend([
                "    <h2>Working Links</h2>",
                "    <ul>",
            ])
            for link in valid_links:
                title = link.title or link.url
                status = f' <span class="status">(HTTP {link.status_code})</span>' if link.status_code else ""
                html_parts.append(f'        <li><a href="{link.url}" target="_blank">{title}</a>{status}</li>')
            html_parts.append("    </ul>")

        if include_invalid and invalid_links:
            html_parts.extend([
                "    <h2>Invalid/Broken Links</h2>",
                "    <ul>",
            ])
            for link in invalid_links:
                title = link.title or link.url
                error = f' <span class="error">- {link.error_message}</span>' if link.error_message else ""
                html_parts.append(f'        <li class="invalid"><a href="{link.url}" target="_blank">{title}</a>{error}</li>')
            html_parts.append("    </ul>")

        html_parts.extend([
            "</body>",
            "</html>",
        ])

        return "\n".join(html_parts)


def find_images_in_directory(directory: str) -> List[str]:
    """Find all supported image files in a directory."""
    images = []
    dir_path = Path(directory)
    for ext in ScreenshotLinkExtractor.SUPPORTED_EXTENSIONS:
        images.extend(str(p) for p in dir_path.glob(f"*{ext}"))
        images.extend(str(p) for p in dir_path.glob(f"*{ext.upper()}"))
    return sorted(images)


def main():
    parser = argparse.ArgumentParser(
        description="Extract links from screenshots and create a clickable document",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s screenshot.png
  %(prog)s image1.png image2.png -o links.md
  %(prog)s --dir ./screenshots -o links.html --format html
  %(prog)s screenshot.png --no-verify -o links.md
        """
    )

    parser.add_argument(
        "images",
        nargs="*",
        help="Path(s) to screenshot image(s)"
    )
    parser.add_argument(
        "-d", "--dir",
        help="Directory containing screenshots to process"
    )
    parser.add_argument(
        "-o", "--output",
        default="extracted_links.md",
        help="Output file path (default: extracted_links.md)"
    )
    parser.add_argument(
        "-f", "--format",
        choices=["markdown", "html"],
        default="markdown",
        help="Output format (default: markdown)"
    )
    parser.add_argument(
        "--no-verify",
        action="store_true",
        help="Skip link verification"
    )
    parser.add_argument(
        "--include-invalid",
        action="store_true",
        help="Include invalid/broken links in output"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="HTTP request timeout in seconds (default: 10)"
    )
    parser.add_argument(
        "--no-ssl-verify",
        action="store_true",
        help="Disable SSL certificate verification"
    )

    args = parser.parse_args()

    # Collect image paths
    image_paths = list(args.images) if args.images else []

    if args.dir:
        dir_images = find_images_in_directory(args.dir)
        if not dir_images:
            print(f"No images found in directory: {args.dir}")
        else:
            print(f"Found {len(dir_images)} images in {args.dir}")
            image_paths.extend(dir_images)

    if not image_paths:
        parser.error("No images specified. Provide image paths or use --dir to specify a directory.")

    # Verify all files exist
    for path in image_paths:
        if not os.path.exists(path):
            print(f"Error: File not found: {path}")
            sys.exit(1)

    # Process screenshots
    extractor = ScreenshotLinkExtractor(
        timeout=args.timeout,
        verify_ssl=not args.no_ssl_verify
    )

    links = extractor.process_screenshots(
        image_paths,
        verify=not args.no_verify
    )

    if not links:
        print("\nNo links found in the provided screenshots.")
        sys.exit(0)

    # Generate document
    if args.format == "html":
        content = DocumentGenerator.generate_html(links, args.include_invalid)
    else:
        content = DocumentGenerator.generate_markdown(links, args.include_invalid)

    # Write output
    output_path = args.output
    if not output_path.endswith(('.md', '.html')):
        output_path += '.html' if args.format == 'html' else '.md'

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    valid_count = sum(1 for l in links if l.is_valid)
    print(f"\nResults:")
    print(f"  Valid links: {valid_count}/{len(links)}")
    print(f"  Output saved to: {output_path}")


if __name__ == "__main__":
    main()
