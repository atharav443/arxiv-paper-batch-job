"""Main entry point for arxiv paper batch job."""

import os
import sys
from datetime import datetime
from arxiv_scraper import parse_arxiv_xml_feed
from paper_filter import is_relevant, score_paper
from email_sender import send_papers_email


def main():
    """Main workflow: scrape papers, filter, and send email."""
    recipient_email = os.getenv("RECIPIENT_EMAIL", "atharavnaik8@gmail.com")

    print(f"[{datetime.now()}] Starting arXiv paper digest job...")

    # Fetch papers from arXiv
    print("Fetching papers from arXiv...")
    papers = parse_arxiv_xml_feed(days_back=7)
    print(f"Found {len(papers)} papers from the past week")

    if not papers:
        print("No papers found. Exiting.")
        return False

    # Score and filter papers
    print("Scoring and filtering papers...")
    scored_papers = []

    for paper in papers:
        score = score_paper(
            paper["title"],
            paper["abstract"],
            paper.get("categories", "")
        )

        if is_relevant(paper["title"], paper["abstract"], paper.get("categories", "")):
            paper["score"] = score
            scored_papers.append(paper)

    print(f"Found {len(scored_papers)} relevant papers")

    if not scored_papers:
        print("No relevant papers found. Exiting.")
        return False

    # Get top 5 papers
    top_papers = sorted(scored_papers, key=lambda x: x["score"], reverse=True)[:5]

    print(f"Top 5 papers:")
    for i, paper in enumerate(top_papers, 1):
        print(f"  {i}. [{paper['score']:.2f}] {paper['title'][:60]}...")

    # Send email
    print(f"Sending email to {recipient_email}...")
    success = send_papers_email(recipient_email, top_papers)

    if success:
        print(f"[{datetime.now()}] Job completed successfully!")
        return True
    else:
        print(f"[{datetime.now()}] Job failed - email not sent")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
