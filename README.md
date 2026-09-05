# redmine-test

Minimal sample repository used to verify the local AI Coding Agent workflow:

Redmine issue -> feature branch -> commit -> push -> Pull Request.

## Health check

Start the HTTP service:

```bash
python3 health_server.py
```

Check health:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{"status": "ok"}
```
