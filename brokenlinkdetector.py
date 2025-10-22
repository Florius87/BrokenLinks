import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import csv
import xml.etree.ElementTree as ET
import os

BASE_DOMAIN = "florisera.com"
SITEMAP_URL = "https://florisera.com/post-sitemap.xml"
MAX_URLS = 110  # Number of pages to process per run
REPORT_CSV = "broken_links_report.csv"

def fetch_html(url):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return None

def extract_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        full_url = urljoin(base_url, href)
        if urlparse(full_url).netloc.endswith(BASE_DOMAIN):
            links.add(full_url)
    return links

def check_link(url):
    try:
        resp = requests.head(url, allow_redirects=True, timeout=10)
        if resp.status_code >= 400:
            return resp.status_code
        return None
    except Exception as e:
        return str(e)

def load_processed_pages():
    processed = set()
    if os.path.isfile(REPORT_CSV):
        with open(REPORT_CSV, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                processed.add(row["page_url"])
    return processed

def main():
    sitemap_xml = fetch_html(SITEMAP_URL)
    if not sitemap_xml:
        print("Failed to fetch sitemap. Exiting.")
        return

    root = ET.fromstring(sitemap_xml)
    ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    page_urls = [elem.text for elem in root.findall(".//ns:url/ns:loc", ns)]

    processed_pages = load_processed_pages()
    to_check = [url for url in page_urls if url not in processed_pages]
    to_check = to_check[:MAX_URLS]

    broken_links_report = []

    for page_url in to_check:
        print(f"Checking page: {page_url}")
        html = fetch_html(page_url)
        if not html:
            continue
        links = extract_links(html, page_url)
        for link in links:
            status = check_link(link)
            if status:
                print(f"Broken link found on {page_url}: {link} (Status: {status})")
                broken_links_report.append({
                    "page_url": page_url,
                    "broken_link": link,
                    "status": status,
                })
        # Mark page as processed by adding a row even if no broken links
        if not broken_links_report or all(bl["page_url"] != page_url for bl in broken_links_report):
            # Add an entry with no broken link if none found
            broken_links_report.append({
                "page_url": page_url,
                "broken_link": "",
                "status": "checked",
            })

    # Append new results to CSV
    file_exists = os.path.isfile(REPORT_CSV)
    with open(REPORT_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["page_url", "broken_link", "status"])
        if not file_exists:
            writer.writeheader()
        writer.writerows(broken_links_report)

    print(f"Broken links report updated in {REPORT_CSV}")

if __name__ == "__main__":
    main()
