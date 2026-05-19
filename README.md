# ArXiv Research Paper Digest

A GitHub Actions batch job that scrapes arXiv papers weekly and sends personalized research digests based on your interests.

## Features

- 📡 **Automatic ArXiv Scraping**: Fetches papers from CS.AI, CS.LG, CS.AR and related categories
- 🤖 **Intelligent Filtering**: Scores papers based on your research interests using keyword matching
- 📧 **Weekly Email Digest**: Sends top 5 relevant papers every Tuesday at 10 AM IST
- 🔍 **Interest-Based Filtering**: Customized to frontier AI research topics including:
  - Architectural alternatives to Transformers (Mamba, JEPA, world models)
  - Hardware/compute substrates (GPUs, TPUs, neuromorphic, quantum computing)
  - Scaling laws and frontier models
  - Reasoning, structure, and neuro-symbolic AI
  - AI for scientific discovery (biology, physics, mathematics)
  - Post-training and alignment techniques

## Setup

### Local Development

1. Clone and install dependencies:
```bash
git clone <repo-url>
cd arxiv-paper-batch-job
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Create a `.env` file with Resend credentials:
```bash
RESEND_API_KEY=re_xxxxxxxxxxxxxxxxxxxxxxxx
RESEND_FROM=onboarding@resend.dev   # or your verified domain sender
RECIPIENT_EMAIL=atharavnaik8@gmail.com
```

3. Run locally:
```bash
python main.py
```

### GitHub Actions Deployment

1. Push code to GitHub repository

2. Add GitHub Secrets:
   - Go to Settings → Secrets and variables → Actions
   - Add `RESEND_API_KEY`: Your Resend API key
   - Add `RESEND_FROM`: The verified sender address (or `onboarding@resend.dev` for testing)

3. The workflow runs automatically every Tuesday at 10 AM IST (04:30 UTC)
   - Can also be triggered manually via "Run workflow"

## Resend Setup

1. Create a free account at [resend.com](https://resend.com) (3,000 emails/month free)
2. Go to **API Keys** → **Create API Key**, copy the `re_...` value
3. (Optional but recommended) Add and verify a domain under **Domains** so you can send from your own address. For quick testing, the built-in `onboarding@resend.dev` sender works without verification — but it can only deliver to the email you signed up with.
4. Add `RESEND_API_KEY` (and `RESEND_FROM` if you verified a domain) as GitHub Secrets

## Project Structure

```
.
├── main.py              # Main entry point
├── arxiv_scraper.py     # Paper fetching from arXiv
├── paper_filter.py      # Relevance scoring and filtering
├── email_sender.py      # Email sending logic
├── requirements.txt     # Python dependencies
└── .github/workflows/
    └── arxiv-digest.yml # GitHub Actions workflow
```

## Customization

### Modify Research Interests

Edit `paper_filter.py` to change:
- Keywords in `INTERESTS` dictionary
- Weights for each category
- Negative keywords to filter out

### Change Schedule

Modify the cron expression in `.github/workflows/arxiv-digest.yml`:
- Currently: `30 4 * * 2` (Tuesday 10 AM IST / 04:30 UTC)
- [Cron format](https://crontab.guru/) is used (UTC timezone)

### Change Number of Papers

Edit `main.py`:
```python
top_papers = sorted(scored_papers, key=lambda x: x["score"], reverse=True)[:N]
```

Change `[:5]` to `[:N]` where N is desired number of papers.

## Troubleshooting

### Email not sending
- Check GitHub Secrets are set correctly (`RESEND_API_KEY`, optionally `RESEND_FROM`)
- Verify the API key is still active in the Resend dashboard
- If using `onboarding@resend.dev`, you can only send to the email you signed up with — verify a domain to send anywhere
- Check email isn't being marked as spam

### No papers found
- Verify arXiv feeds are accessible
- Check `paper_filter.py` scoring thresholds
- Adjust keywords in `INTERESTS` dictionary

### Running locally fails
- Install all dependencies: `pip install -r requirements.txt`
- Set environment variables: `export RESEND_API_KEY=...`
- Check internet connection for arXiv access

## How It Works

1. **Scraping**: Fetches recent papers from arXiv RSS feeds
2. **Filtering**: Scores each paper based on keyword matching against research interests
3. **Ranking**: Selects top 5 papers by relevance score
4. **Email**: Sends formatted HTML email with paper summaries and links
5. **Schedule**: Runs automatically via GitHub Actions every Tuesday

## License

MIT

## Contact

For issues or improvements, please open an issue on GitHub.
# arxiv-paper-batch-job
