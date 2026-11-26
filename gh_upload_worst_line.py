"""Upload this entry's files to its public GitHub repository.

Usage:
    python3 gh_upload_worst_line.py [--repo NAME] [--owner OWNER] [--branch BRANCH]

The repository must already exist (created separately with create_repo.py).
This script only uploads files through the GitHub Contents API, creating
each file or updating it when it is already there. It authenticates with
the stored GitHub credential through the dynamic-credentials surrogate, so
no token is ever pasted into this file.

Uploads main.py and README.md from this folder.
"""

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request

OWNER = "rezimtirani"
REPO = "u-steady-ibis-48-6610-the-worst-line-an-ai-could-say-2ae5e90f-entry"
BRANCH = "main"
FILES = ["main.py", "README.md"]

API = "https://api.github.com"


def api_request(method, url, payload=None):
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Accept", "application/vnd.github+json")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    add_surrogate_to_request(req, "custom.github", allowed_hosts=["api.github.com"])
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def existing_sha(path):
    url = f"{API}/repos/{OWNER}/{REPO}/contents/{path}?ref={BRANCH}"
    try:
        return api_request("GET", url)["sha"]
    except urllib.error.HTTPError as err:
        if err.code == 404:
            return None
        raise


def upload_one(local_path, repo_path):
    with open(local_path, "rb") as handle:
        content = base64.b64encode(handle.read()).decode("ascii")
    payload = {
        "message": f"Add {repo_path} for The Worst Line an AI Could Say entry",
        "content": content,
        "branch": BRANCH,
    }
    sha = existing_sha(repo_path)
    if sha:
        payload["sha"] = sha
    url = f"{API}/repos/{OWNER}/{REPO}/contents/{repo_path}"
    result = api_request("PUT", url, payload)
    print(f"uploaded {repo_path} -> {result['content']['sha']}")
    return result


def main():
    global OWNER, REPO, BRANCH
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=REPO)
    parser.add_argument("--owner", default=OWNER)
    parser.add_argument("--branch", default=BRANCH)
    args = parser.parse_args()
    OWNER, REPO, BRANCH = args.owner, args.repo, args.branch
    here = os.path.dirname(os.path.abspath(__file__))
    for name in FILES:
        upload_one(os.path.join(here, name), name)
    print(f"done: https://github.com/{OWNER}/{REPO}")


if __name__ == "__main__":
    main()
