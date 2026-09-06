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

## Version check

```bash
curl http://127.0.0.1:8000/version
```

Expected response:

```json
{"service": "redmine-test", "version": "0.1.0"}
```

## Merge gate

`main` 分支受保护：

- 禁止直接 push `main`
- 必须通过 Pull Request 合并
- 至少需要 1 个 Approve，且批准人不能是最近一次推送者
- Pull Request 会话评论需全部 resolved
