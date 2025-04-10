# FirstWordPharma RSS Feed Generator

This repository hosts an automated RSS feed generator for FirstWordPharma press releases.

## RSS Feed URL

The generated RSS feed is available at:

**[https://fermaagents.github.io/Sandeep/firstwordpharma_press_releases.xml](https://fermaagents.github.io/Sandeep/firstwordpharma_press_releases.xml)**

## How It Works

1. A GitHub Action runs daily to scrape the latest press releases from FirstWordPharma
2. The script generates an RSS feed in XML format
3. The feed is automatically committed to this repository
4. GitHub Pages serves the XML file at the URL above

## Local Development

To run the RSS generator locally:

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the script: `python firstwordpharma_rss_scraper.py`

## Feed Content

The RSS feed includes:
- Press release titles
- Publication dates
- Summary text
- Links to the original articles