"""Scrape arXiv papers using the API."""

import feedparser
from datetime import datetime, timedelta
from typing import List, Dict
import time
import requests
import warnings
from email.utils import parsedate_to_datetime


def fetch_papers_from_arxiv(
    categories: List[str] = None,
    days_back: int = 7,
    max_papers: int = 100
) -> List[Dict]:
    """Fetch papers from arXiv API.

    Args:
        categories: List of arXiv categories (e.g., ['cs.AI', 'cs.AR'])
        days_back: Number of days to look back
        max_papers: Maximum papers to fetch per category

    Returns:
        List of paper dictionaries with title, abstract, authors, url, published_date
    """
    if categories is None:
        categories = [
            "cs.AI",      # Artificial Intelligence
            "cs.LG",      # Machine Learning
            "cs.AR",      # Hardware Architecture
            "cs.DC",      # Distributed Computing
            "stat.ML",    # Statistical Machine Learning
            "q-bio.QM",   # Quantitative Methods (for scientific applications)
            "physics.cmp-gas",  # Computational physics
        ]

    papers = []
    cutoff_date = datetime.now() - timedelta(days=days_back)

    for category in categories:
        # arXiv API endpoint
        base_url = "http://export.arxiv.org/api/query?"
        search_query = f"cat:{category} AND submittedDate:[{cutoff_date.strftime('%Y%m%d0000')} TO {datetime.now().strftime('%Y%m%d2359')}]"

        params = {
            "search_query": search_query,
            "start": 0,
            "max_results": max_papers,
            "sortBy": "submittedDate",
            "sortOrder": "descending"
        }

        try:
            # Build query string manually to avoid issues
            query_string = f"{base_url}search_query={search_query}&start=0&max_results={max_papers}&sortBy=submittedDate&sortOrder=descending"
            response = feedparser.parse(query_string)

            if response.status == 200 or "entries" in response:
                for entry in response.entries:
                    paper = {
                        "title": entry.title,
                        "abstract": entry.summary,
                        "authors": [author.name for author in entry.authors],
                        "url": entry.id,
                        "published_date": entry.published,
                        "categories": entry.get("arxiv_primary_category", {}).get("term", category),
                        "arxiv_id": entry.id.split("/abs/")[-1]
                    }
                    papers.append(paper)

            # Rate limiting to avoid API throttling
            time.sleep(3)

        except Exception as e:
            print(f"Error fetching from category {category}: {e}")
            continue

    return papers


def parse_arxiv_xml_feed(days_back: int = 7) -> List[Dict]:
    """Fetch papers directly from arXiv feeds (alternative method)."""
    papers = []

    # arXiv category feeds updated daily
    feeds = {
        "ai": "http://export.arxiv.org/rss/cs.AI",
        "ml": "http://export.arxiv.org/rss/cs.LG",
        "architecture": "http://export.arxiv.org/rss/cs.AR",
        "dc": "http://export.arxiv.org/rss/cs.DC",
        "stat_ml": "http://export.arxiv.org/rss/stat.ML",
    }

    for feed_name, feed_url in feeds.items():
        try:
            # Suppress SSL warnings for development
            warnings.filterwarnings("ignore", message="Unverified HTTPS request")

            # Use requests to fetch the feed
            response = requests.get(feed_url, timeout=10, verify=False)
            response.raise_for_status()

            # Parse the XML content with feedparser
            parsed = feedparser.parse(response.content)

            for entry in parsed.entries[:50]:  # Get top 50 recent papers per feed
                try:
                    # Parse RFC 2822 format from arXiv RSS
                    published = parsedate_to_datetime(entry.published)
                    cutoff = datetime.now(published.tzinfo) - timedelta(days=days_back)

                    if published > cutoff:
                        paper = {
                            "title": entry.title,
                            "abstract": entry.summary,
                            "authors": [author.name for author in entry.get("authors", [])],
                            "url": entry.link,
                            "published_date": entry.published,
                            "categories": feed_name,
                            "arxiv_id": entry.id.split("/abs/")[-1]
                        }
                        papers.append(paper)
                except Exception as e:
                    print(f"Error parsing entry: {e}")
                    continue

            time.sleep(2)

        except Exception as e:
            print(f"Error fetching feed {feed_name}: {e}")
            continue

    # Remove duplicates based on arxiv_id
    seen = set()
    unique_papers = []
    for paper in papers:
        if paper["arxiv_id"] not in seen:
            seen.add(paper["arxiv_id"])
            unique_papers.append(paper)

    return unique_papers
