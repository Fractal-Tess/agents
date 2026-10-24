#!/usr/bin/env python3
"""Forget Supermemory memories by ID, after saving a copy of each one.

usage: forget.py <containerTag> <memory id>... [--yes]

Without --yes it only prints what would be forgotten. With --yes it saves
the memories to ~/.local/state/supermemory-audit/ and then forgets them.
Forgetting hides a memory from recall; the server keeps its history, but
there is no API to bring it back, so the saved copy is the way to re-add one.
"""
import datetime
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API_URL = os.environ.get("SUPERMEMORY_API_URL", "http://127.0.0.1:6767").rstrip("/")
KEY = json.load(open(os.path.expanduser("~/.supermemory-claude/credentials.json")))["apiKey"]
BACKUP_DIR = os.path.expanduser("~/.local/state/supermemory-audit")


def api(method, path, body=None):
    req = urllib.request.Request(API_URL + path, method=method, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        raise SystemExit(f"{method} {path} failed: {e.code} {e.read()[:300].decode(errors='replace')}")


args = [a for a in sys.argv[1:] if a != "--yes"]
confirmed = "--yes" in sys.argv[1:]
if len(args) < 2:
    raise SystemExit(__doc__)
tag, ids = args[0], list(dict.fromkeys(args[1:]))
ns = urllib.parse.quote(tag, safe="")

memories = []
for memory_id in ids:
    m = api("GET", f"/ns/{ns}/memories/{urllib.parse.quote(memory_id, safe='')}?include=documents")
    memories.append(m)
    state = " (already forgotten)" if m.get("isForgotten") else ""
    print(f"- {m['id']} v{m['version']} {m['system']['createdAt'][:10]}{state}: {m['memory']}")

if not confirmed:
    print(f"\nDry run: {len(memories)} memories in {tag} would be forgotten. Re-run with --yes once the user has approved.")
    sys.exit(0)

os.makedirs(BACKUP_DIR, exist_ok=True)
stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
backup = os.path.join(BACKUP_DIR, f"{tag}-{stamp}.json")
json.dump({"containerTag": tag, "forgottenAt": stamp, "memories": memories}, open(backup, "w"), indent=1)

result = api("DELETE", f"/ns/{ns}/memories", {"ids": ids})
print(f"\nForgot {result.get('count', 0)} of {len(ids)} memories in {tag}. Copies saved to {backup}")
for error in result.get("errors") or []:
    print(f"  not forgotten: {json.dumps(error)}")
