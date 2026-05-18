# Quick Start Guide

Get your arXiv digest running in 5 minutes.

## 1. Gmail Setup (2 minutes)

1. Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (custom name)"
   - Enter "arXiv Digest"
   - Copy the 16-character password

## 2. GitHub Setup (2 minutes)

1. Push this code to GitHub
2. Go to your repo → Settings → Secrets and variables → Actions
3. Add two secrets:
   - `GMAIL_SENDER` = your-email@gmail.com
   - `GMAIL_PASSWORD` = the 16-char password from step 1

## 3. Test (30 seconds)

1. Go to Actions tab
2. Click "ArXiv Weekly Digest" → "Run workflow"
3. Check email for top 5 papers

## 4. Done! ✅

Your digest will automatically send every Tuesday at 10 AM IST.

---

## Testing Locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

export GMAIL_SENDER="your-email@gmail.com"
export GMAIL_PASSWORD="your-app-password"
export RECIPIENT_EMAIL="atharavnaik8@gmail.com"

python main.py
```

## Troubleshooting

**"Invalid credentials"** → Use app password, not Gmail password

**"No papers found"** → arXiv feeds sometimes slow, increase `days_back` in code

**Workflow won't run** → Enable Actions in repo settings, check schedule syntax

See `DEPLOYMENT.md` for detailed troubleshooting.
