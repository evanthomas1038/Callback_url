# Meta Graph API Callback Backend

Very small FastAPI backend for Meta webhook verification and callback delivery.

## Endpoints

- `GET /webhook` - Meta webhook verification endpoint
- `POST /webhook` - receives Meta webhook events
- `GET /oauth/callback` - optional OAuth redirect callback that returns the `code`
- `GET /` - health check

## Local setup

```bash
python -m venv .venv
pip install -r requirements.txt
set META_VERIFY_TOKEN=your_random_secret_here
uvicorn app.main:app --reload
```

PowerShell:

```powershell
$env:META_VERIFY_TOKEN="your_random_secret_here"
uvicorn app.main:app --reload
```

## What to enter in Meta

After deploying this backend to HTTPS:

```text
Callback URL: https://your-domain.com/webhook
Verify token: the same value as META_VERIFY_TOKEN
```

Example:

```text
Callback URL: https://my-api.example.com/webhook
Verify token: ig_webhook_verify_9x7k2p
```

Use your own random verify token. Do not paste the example token.

## OAuth callback URL

If Meta asks for an OAuth redirect URL instead of the webhook callback URL, use:

```text
https://your-domain.com/oauth/callback
```

Webhook callback URL and OAuth redirect URL are different.
