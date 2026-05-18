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

2. Create a `.env` file with Gmail credentials:
```bash
GMAIL_SENDER=your-email@gmail.com
GMAIL_PASSWORD=your-app-specific-password
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
   - Add `GMAIL_SENDER`: Your Gmail address
   - Add `GMAIL_PASSWORD`: Your [app-specific password](https://support.google.com/accounts/answer/185833)

3. The workflow runs automatically every Tuesday at 10 AM IST (04:30 UTC)
   - Can also be triggered manually via "Run workflow"

## Gmail Setup

1. Enable 2-Factor Authentication on your Google account
2. Generate an [app-specific password](https://support.google.com/accounts/answer/185833)
3. Use the app password as `GMAIL_PASSWORD` in GitHub Secrets

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
- Check GitHub Secrets are set correctly
- Verify Gmail app-specific password is current
- Check email isn't being marked as spam

### No papers found
- Verify arXiv feeds are accessible
- Check `paper_filter.py` scoring thresholds
- Adjust keywords in `INTERESTS` dictionary

### Running locally fails
- Install all dependencies: `pip install -r requirements.txt`
- Set environment variables: `export GMAIL_SENDER=...`
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
