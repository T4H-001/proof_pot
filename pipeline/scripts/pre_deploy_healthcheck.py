#!/usr/bin/env python3
"""Pre-deploy gate. Verifies required env + health endpoint before any deploy.
Refuses (exit 1) rather than guessing when secrets are absent."""
import os, sys, urllib.request

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "staging"
    hc = os.environ.get(f"{target.upper()}_HEALTHCHECK_URL")
    if not hc:
        print(f"BLOCKED: {target.upper()}_HEALTHCHECK_URL not set", file=sys.stderr)
        sys.exit(1)
    try:
        with urllib.request.urlopen(hc, timeout=10) as r:
            ok = 200 <= r.status < 300
    except Exception as e:
        print(f"BLOCKED: healthcheck unreachable: {e}", file=sys.stderr)
        sys.exit(1)
    print("REAL: healthcheck 2xx" if ok else "BLOCKED: healthcheck non-2xx")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
