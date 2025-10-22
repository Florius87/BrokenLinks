# Broken Link Detector — README

Crawls your sitemap, finds **internal** links, checks them with HTTP **HEAD**, and appends results to a CSV so you can resume later.

## Requirements
- Python 3.8+
- Packages: `requests`, `beautifulsoup4`

## Configure
Edit the constants at the top of the script:

| Variable    | Default                               | Purpose                                                       |
|-------------|----------------------------------------|---------------------------------------------------------------|
| BASE_DOMAIN | florisera.com                          | Treat links ending with this domain as internal.              |
| SITEMAP_URL | https://florisera.com/post-sitemap.xml | Sitemap to crawl for page URLs.                               |
| MAX_URLS    | 110                                    | Max pages processed per run.                                  |
| REPORT_CSV  | broken_links_report.csv                | Append-only report (also used to skip checked pages).         |

Sitemaps spec: https://www.sitemaps.org/protocol.html

## How it works
1. Fetch sitemap and parse all `<loc>` URLs.  
2. Skip pages already present in `REPORT_CSV`.  
3. For each new page: fetch HTML → collect internal `<a href>` → send `HEAD`.  
4. Record links with status ≥ 400. If none, write a `checked` row.

## Run
From the script folder run: `python brokenlinkdetector.py`

## Output (CSV)
Columns: `page_url`, `broken_link`, `status`  
- `status` is an HTTP code or `checked` (no broken links on that page).  
- Delete `REPORT_CSV` to rescan everything.

## Notes
- Internal links only.  
- Some sites reject `HEAD`; consider adding a `GET` fallback.  
- Increase `MAX_URLS` to process more pages per run.
