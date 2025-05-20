import requests


def extract_features(repo_full_name):
    """
    Extracts commits, forks, and watchers from a GitHub repo.
    repo_full_name: e.g. 'pallets/flask'
    Returns: dict or raises Exception
    """

    GITHUB_TOKEN = ""
    headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}"
    }
    base_url = f"https://api.github.com/repos/{repo_full_name}"

    # Fetch repo info
    repo_resp = requests.get(base_url, headers=headers)
    if repo_resp.status_code != 200:
        raise Exception(f"Repo '{repo_full_name}' not found")

    repo_data = repo_resp.json()

    # Fetch commits count
    commits_resp = requests.get(f"{base_url}/commits", headers=headers, params={"per_page": 1})
    if 'Link' in commits_resp.headers:
        last_page = [link for link in commits_resp.headers['Link'].split(",") if 'rel="last"' in link]
        if last_page:
            commit_count = int(last_page[0].split("page=")[-1].split(">")[0])
        else:
            commit_count = 1
    else:
        commit_count = len(commits_resp.json())

    return {
        "commits": commit_count,
        "forks": repo_data.get("forks_count", 0),
        "watchers": repo_data.get("watchers_count", 0)
    }
