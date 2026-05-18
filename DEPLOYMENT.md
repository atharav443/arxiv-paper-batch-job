# Deployment Guide

## Prerequisites

- GitHub account with a repository
- Gmail account with 2FA enabled
- Python 3.11+ (for local testing)

## Step 1: Gmail Setup

1. **Enable 2-Factor Authentication**
   - Go to https://myaccount.google.com/security
   - Enable "2-Step Verification"

2. **Create App Password**
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (custom name)"
   - Enter "arXiv Digest Job"
   - Google will generate a 16-character password
   - **Save this password securely** - you'll need it for GitHub Secrets

## Step 2: GitHub Repository Setup

1. **Create Repository**
   ```bash
   git remote add origin https://github.com/your-username/arxiv-paper-batch-job.git
   git branch -M main
   git push -u origin main
   ```

2. **Add GitHub Secrets**
   - Go to your repository on GitHub
   - Navigate to Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Add two secrets:
     - **GMAIL_SENDER**: Your Gmail address (e.g., your-email@gmail.com)
     - **GMAIL_PASSWORD**: The 16-character app-specific password from Step 1

   These secrets will be automatically injected into the workflow as environment variables.

## Step 3: Verify Workflow

1. **Manual Trigger (Test)**
   - Go to Actions tab in your repository
   - Click "ArXiv Weekly Digest" workflow
   - Click "Run workflow" button
   - Watch the logs to ensure it runs successfully

2. **Automatic Scheduling**
   - The workflow is configured to run every Tuesday at 10 AM IST (04:30 UTC)
   - No further setup needed - it will automatically trigger on schedule

## Step 4: Monitor Execution

1. **Check Workflow Runs**
   - Go to Actions tab
   - Click "ArXiv Weekly Digest"
   - See all past runs and their status

2. **Troubleshoot Failures**
   - Click on failed run
   - Click "arxiv-digest" job
   - Expand "Run arXiv digest job" to see logs
   - Check for error messages

## Local Testing

1. **Install Dependencies**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Create .env File**
   ```bash
   cat > .env << EOF
   GMAIL_SENDER=your-email@gmail.com
   GMAIL_PASSWORD=your-app-specific-password
   RECIPIENT_EMAIL=atharavnaik8@gmail.com
   EOF
   ```

3. **Run Test**
   ```bash
   source venv/bin/activate
   export $(cat .env | xargs)
   python main.py
   ```

## Troubleshooting

### Email Not Sending

**Problem**: "Error: GMAIL_SENDER and GMAIL_PASSWORD environment variables required"

**Solution**:
- Verify GitHub Secrets are set correctly
- Check secret names exactly match: `GMAIL_SENDER` and `GMAIL_PASSWORD`
- Re-create secrets if needed

**Problem**: "SMTPAuthenticationError: Invalid credentials"

**Solution**:
- Verify you used the app-specific password (16 characters), not your regular password
- Confirm 2FA is enabled on Gmail account
- Generate a new app password and update GitHub Secret

**Problem**: "SMTPRejectRecipient: 550 5.7.1 Unauthenticated email"

**Solution**:
- Ensure `GMAIL_SENDER` matches the email you're authenticated with
- Check the `RECIPIENT_EMAIL` is valid

### No Papers Found

**Problem**: Email sent but with 0 papers

**Solution**:
- arXiv feeds may be temporarily unavailable
- Check arXiv status at https://status.arxiv.org/
- Increase `days_back` parameter in `arxiv_scraper.py` to look further back
- Adjust filter thresholds in `paper_filter.py`

### Workflow Not Running

**Problem**: Scheduled workflow doesn't execute

**Solution**:
- GitHub Actions must be enabled in repository settings
- Check workflow file syntax with `git diff .github/workflows/arxiv-digest.yml`
- Verify the schedule time: Tuesday 04:30 UTC (10 AM IST)
- GitHub may have workflow limits for private repos

## Customization

### Change Email Recipient

Edit `.github/workflows/arxiv-digest.yml`:
```yaml
env:
  RECIPIENT_EMAIL: newemail@example.com
```

### Change Schedule

Edit `.github/workflows/arxiv-digest.yml`:
```yaml
- cron: '0 10 * * 2'  # Every Tuesday at 10 AM UTC
```

[Cron format help](https://crontab.guru/)

### Change Paper Count

Edit `main.py`:
```python
top_papers = sorted(scored_papers, key=lambda x: x["score"], reverse=True)[:10]
```
Change `[:5]` to `[:N]` for N papers.

### Update Research Interests

Edit `paper_filter.py` to modify keywords and weights in the `INTERESTS` dictionary.

## Security Notes

- App-specific passwords are tied to your Gmail account but can't access all Google services
- GitHub Secrets are encrypted and only visible to authorized users
- The script doesn't store emails or paper data - it only sends via SMTP
- arXiv feeds are public and don't require authentication

## Support

For issues:
1. Check GitHub Actions logs
2. Review error messages in workflow output
3. Test locally with `.env` file
4. Verify Gmail app password is current
