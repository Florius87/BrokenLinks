Broken Link Detector — README

Crawls your sitemap, extracts internal links, checks them with HTTP HEAD, and appends results to a CSV so you can resume later.

Requirements

Python 3.8+ · requests · beautifulsoup4

Configure

Edit the constants at the top of the script:

Variable	Default	Purpose
BASE_DOMAIN	florisera.com	Treat links ending with this domain as internal.
SITEMAP_URL	https://florisera.com/post-sitemap.xml
How it works (brief)

Fetch sitemap and parse all <loc> URLs.

Skip pages already present in REPORT_CSV.

For each new page: fetch HTML → collect internal <a href> → HEAD each link.

Record broken ones (status ≥ 400). If none, write a “checked” row.

Run

From your terminal in the script’s folder:
python brokenlinkdetector.py

Output (CSV)

Columns: page_url, broken_link, status

status is an HTTP code or “checked” (no broken links on that page).

Delete REPORT_CSV to rescan everything from scratch.

Notes

Internal only (external links are ignored).

Some sites don’t support HEAD; you may add a GET fallback if needed.

Increase MAX_URLS to process more pages per run.
