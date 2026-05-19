"""Send email with top papers via Resend API."""

from typing import List, Dict
import os
import resend


def send_papers_email(
    recipient_email: str,
    papers: List[Dict],
    sender_email: str = None,
    api_key: str = None
) -> bool:
    """Send email with top papers using Resend.

    Args:
        recipient_email: Email address to send to
        papers: List of paper dictionaries
        sender_email: From address (uses RESEND_FROM env var if not provided).
            For testing without a verified domain, use "onboarding@resend.dev".
        api_key: Resend API key (uses RESEND_API_KEY env var if not provided)

    Returns:
        True if successful, False otherwise
    """
    if api_key is None:
        api_key = os.getenv("RESEND_API_KEY", "")
    if sender_email is None:
        sender_email = os.getenv("RESEND_FROM", "onboarding@resend.dev")

    if not api_key:
        print("Error: RESEND_API_KEY environment variable required")
        return False

    resend.api_key = api_key

    try:
        params: resend.Emails.SendParams = {
            "from": sender_email,
            "to": [recipient_email],
            "subject": "Top 5 arXiv Papers This Week - AI Research Digest",
            "html": create_html_email(papers),
            "text": create_plain_text_email(papers),
        }

        email = resend.Emails.send(params)
        print(f"Email sent successfully to {recipient_email} (id: {email.get('id')})")
        return True

    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def create_plain_text_email(papers: List[Dict]) -> str:
    """Create plain text version of email."""
    content = "Top 5 arXiv Papers This Week\n"
    content += "=" * 50 + "\n\n"

    for i, paper in enumerate(papers, 1):
        content += f"{i}. {paper['title']}\n"
        content += f"   Score: {paper.get('score', 0):.2f}\n"
        content += f"   Authors: {', '.join(paper['authors'][:3])}"
        if len(paper['authors']) > 3:
            content += f" (+ {len(paper['authors']) - 3} more)"
        content += "\n"
        content += f"   Link: {paper['url']}\n"
        content += f"   Abstract: {paper['abstract'][:200]}...\n\n"

    content += "=" * 50 + "\n"
    content += "Weekly AI Research Digest\n"
    content += "Tailored to your research interests\n"

    return content


def create_html_email(papers: List[Dict]) -> str:
    """Create HTML version of email."""
    html = """
    <html>
        <body style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto;">
            <div style="background-color: #1a1a1a; color: #ffffff; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                <h1 style="margin: 0; font-size: 28px;">🤖 Top 5 arXiv Papers This Week</h1>
                <p style="margin: 10px 0 0 0; color: #cccccc;">Your weekly AI research digest</p>
            </div>
    """

    for i, paper in enumerate(papers, 1):
        score = paper.get("score", 0)
        score_color = "#4CAF50" if score >= 0.7 else "#FFC107" if score >= 0.5 else "#FF9800"

        authors_str = ", ".join(paper["authors"][:3])
        if len(paper["authors"]) > 3:
            authors_str += f" <em>(+ {len(paper['authors']) - 3} more)</em>"

        abstract = paper["abstract"]
        if len(abstract) > 250:
            abstract = abstract[:250] + "..."

        html += f"""
            <div style="border-left: 4px solid {score_color}; padding: 15px; margin-bottom: 20px; background-color: #f9f9f9; border-radius: 4px;">
                <h3 style="margin: 0 0 10px 0; color: #1a1a1a;">
                    {i}. {paper['title']}
                </h3>
                <p style="margin: 5px 0; color: #666;">
                    <strong>Relevance Score:</strong> <span style="color: {score_color}; font-weight: bold;">{score:.2f}</span>
                </p>
                <p style="margin: 5px 0; color: #666;">
                    <strong>Authors:</strong> {authors_str}
                </p>
                <p style="margin: 5px 0; color: #666;">
                    <strong>Published:</strong> {paper.get('published_date', 'N/A')[:10]}
                </p>
                <p style="margin: 10px 0; line-height: 1.6; color: #333;">
                    {abstract}
                </p>
                <p style="margin: 10px 0;">
                    <a href="{paper['url']}" style="color: #0066cc; text-decoration: none; font-weight: bold;">
                        Read on arXiv →
                    </a>
                </p>
            </div>
        """

    html += """
            <div style="border-top: 1px solid #ddd; padding-top: 20px; margin-top: 30px; color: #666; font-size: 12px;">
                <p>This digest is tailored to your research interests:</p>
                <ul style="margin: 10px 0; padding-left: 20px;">
                    <li>Architectural alternatives to Transformers</li>
                    <li>Hardware and compute substrates for AI</li>
                    <li>Scaling laws and limits</li>
                    <li>Reasoning and structure in intelligence</li>
                    <li>AI for scientific acceleration</li>
                    <li>Post-training and alignment</li>
                </ul>
                <p style="margin-top: 20px;">
                    Generated automatically every Tuesday at 10 AM IST
                </p>
            </div>
        </body>
    </html>
    """

    return html
