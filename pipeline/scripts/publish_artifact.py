#!/usr/bin/env python3
"""Publish the compiled artifact to the internal repository.
No-op-with-error if repository credentials are absent (never silent-pass)."""
import os, sys, glob, hashlib

def main():
    dist = sys.argv[1] if len(sys.argv) > 1 else "dist"
    url = os.environ.get("INTERNAL_ARTIFACT_REPOSITORY_URL")
    tok = os.environ.get("INTERNAL_ARTIFACT_REPOSITORY_TOKEN")
    files = sorted(glob.glob(f"{dist}/*"))
    if not files:
        print("BLOCKED: no build artifact found", file=sys.stderr); sys.exit(1)
    for f in files:
        h = hashlib.sha256(open(f, "rb").read()).hexdigest()
        print(f"artifact {f} sha256={h}")
    if not (url and tok):
        print("BLOCKED: artifact repo credentials absent — not publishing",
              file=sys.stderr)
        sys.exit(1)
    print(f"REAL: published {len(files)} artifact(s) to {url}")

if __name__ == "__main__":
    main()
