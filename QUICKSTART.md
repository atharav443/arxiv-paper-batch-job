# Quick Start Guide

Get your arXiv digest running in 5 minutes.

## 1. Resend Setup (2 minutes)

1. Sign up at https://resend.com (free tier: 3,000 emails/month)
2. Go to **API Keys** → **Create API Key**, name it "arXiv Digest"
3. Copy the `re_...` key — you'll only see it once
4. (Optional) Verify a domain under **Domains** to send from your own address.
   Skip this for testing; you can use `onboarding@resend.dev` instead, but it will only deliver to the email you signed up with.

## 2. GitHub Setup (2 minutes)

1. Push this code to GitHub
2. Go to your repo → Settings → Secrets and variables → Actions
3. Add these secrets:
   - `RESEND_API_KEY` = the `re_...` key from step 1
   - `RESEND_FROM` = your verified sender (or `onboarding@resend.dev` for testing)

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

export RESEND_API_KEY="re_xxxxxxxxxxxxxxxxxxxxxxxx"
export RESEND_FROM="onboarding@resend.dev"
export RECIPIENT_EMAIL="atharavnaik8@gmail.com"

python main.py
```

## Troubleshooting

**"RESEND_API_KEY environment variable required"** → Secret not set, or env var missing locally

**"You can only send testing emails to your own email address"** → You're using `onboarding@resend.dev` but sending to someone other than your signup email. Verify a domain in Resend to send anywhere.

**"No papers found"** → arXiv feeds sometimes slow, increase `days_back` in code

**Workflow won't run** → Enable Actions in repo settings, check schedule syntax

See `DEPLOYMENT.md` for detailed troubleshooting.
