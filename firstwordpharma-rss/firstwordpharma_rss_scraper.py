#!/usr/bin/env python3
"""
FirstWordPharma RSS Feed Generator
---------------------------------
This script scrapes press releases from FirstWordPharma and generates an RSS feed.
Dependencies:
- pyppeteer (Python port of Puppeteer)
- beautifulsoup4
- feedgen
- aiohttp
- asyncio
"""

import asyncio
import os
import re
from datetime import datetime
from urllib.parse import urljoin

import aiohttp
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from pyppeteer import launch

# URL configuration
BASE_URL = "https://firstwordpharma.com"
TARGET_URL = "https://firstwordpharma.com/river/type/Press%20Release"
OUTPUT_FILE = "firstwordpharma_press_releases.xml"

async def fetch_page_content():
    """
    Fetch the page content using Pyppeteer (Python port of Puppeteer)
    to handle dynamic JavaScript content loading.
    """
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto(TARGET_URL, {'waitUntil': 'networkidle0'})
    
    # Wait for content to load (adjust selector based on actual page structure)
    await page.waitForSelector('.article-item', {'timeout': 10000})
    
    # Get the page content after JavaScript has been executed
    content = await page.content()
    await browser.close()
    
    return content

def parse_articles(html_content):
    """
    Parse the HTML content using BeautifulSoup to extract article information.
    Adjust the selectors based on the actual structure of the website.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    articles = []
    
    # This is a placeholder selector - adjust based on actual page structure
    article_elements = soup.select('.article-item')
    
    if not article_elements:
        # Fallback selector if the first one doesn't match
        article_elements = soup.select('article') or soup.select('.news-item')
    
    for article in article_elements:
        try:
            # Adjust these selectors based on the actual page structure
            title_element = article.select_one('.article-title') or article.select_one('h2') or article.select_one('h3')
            link_element = article.select_one('a')
            date_element = article.select_one('.article-date') or article.select_one('.date')
            summary_element = article.select_one('.article-summary') or article.select_one('p')
            
            title = title_element.text.strip() if title_element else "No title"
            link = urljoin(BASE_URL, link_element['href']) if link_element and 'href' in link_element.attrs else "#"
            
            # Parse date (adjust format based on actual date format)
            date_str = date_element.text.strip() if date_element else ""
            try:
                # Try common date formats
                for fmt in ['%B %d, %Y', '%d %b %Y', '%Y-%m-%d', '%m/%d/%Y']:
                    try:
                        date = datetime.strptime(date_str, fmt)
                        break
                    except ValueError:
                        continue
                else:
                    # If no format matches, use current date
                    date = datetime.now()
            except Exception:
                date = datetime.now()
            
            summary = summary_element.text.strip() if summary_element else "No summary available"
            
            articles.append({
                'title': title,
                'link': link,
                'published': date,
                'summary': summary
            })
        except Exception as e:
            print(f"Error parsing article: {e}")
    
    return articles

def generate_rss_feed(articles):
    """
    Generate an RSS feed using the FeedGenerator library.
    """
    fg = FeedGenerator()
    fg.title('FirstWordPharma Press Releases')
    fg.link(href=TARGET_URL, rel='alternate')
    fg.description('Press releases from FirstWordPharma')
    fg.language('en')
    
    for article in articles:
        fe = fg.add_entry()
        fe.title(article['title'])
        fe.link(href=article['link'])
        fe.published(article['published'])
        fe.description(article['summary'])
    
    # Save the feed to a file
    fg.rss_file(OUTPUT_FILE)
    print(f"RSS feed generated and saved to {OUTPUT_FILE}")
    
    # Return the RSS XML as a string
    return fg.rss_str(pretty=True).decode('utf-8')

async def main():
    try:
        print("Fetching page content...")
        content = await fetch_page_content()
        
        print("Parsing articles...")
        articles = parse_articles(content)
        
        if not articles:
            print("No articles found. Check the selectors in the parse_articles function.")
            return
        
        print(f"Found {len(articles)} articles")
        
        print("Generating RSS feed...")
        generate_rss_feed(articles)
        
        print(f"Success! RSS feed is available at {OUTPUT_FILE}")
        print(f"To access this feed, you can serve it via HTTP or use it locally.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
