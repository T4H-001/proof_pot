#!/usr/bin/env python3
"""Trigger a deployment webhook for a pinned artifact version.
Production requires an explicit pinned version argument (rollback safety)."""
import os, sys, json, urllib.request

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "staging"
    version = sys.argv[2] if len(sys.argv) > 2 else "latest"
    if target == "production" and version == "latest":
        print("BLOCKED: production deploy requires a pinned artifact version",
              file=sys.stderr)
        sys.exit(1)
    hook = os.environ.get(f"{target.upper()}_DEPLOY_WEBHOOK_URL")
    tok  = os.environ.get(f"{target.upper()}_DEPLOY_WEBHOOK_TOKEN")
    if not (hook and tok):
        print(f"BLOCKED: {target} deploy webhook/token absent", file=sys.stderr)
        sys.exit(1)
    body = json.dumps({"target": target, "version": version}).encode()
    req = urllib.request.Request(
        hook, data=body,
        headers={"Authorization": f"Bearer {tok}",
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        print(f"REAL: deploy triggered target={target} version={version} "
              f"status={r.status}")

if __name__ == "__main__":
    main()
