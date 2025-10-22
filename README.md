# Broken Link Detector

Scan your site for **internal broken links** using your XML sitemap and save results to a CSV for easy fixing over time.

---

## Requirements

- Python 3.8+
- Libraries: [`requests`](https://pypi.org/project/requests/), [`beautifulsoup4`](https://pypi.org/project/beautifulsoup4/)

Install:
```bash
pip install requests beautifulsoup4

## Configure

Edit the constants at the top of `brokenlinkdetector.py`:

```python
BASE_DOMAIN = "florisera.com"
SITEMAP_URL = "https://florisera.com/post-sitemap.xml"
MAX_URLS = 110  # pages checked per run
REPORT_CSV = "broken_links_report.csv"
