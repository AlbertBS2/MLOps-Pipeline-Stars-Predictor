import requests
from dotenv import load_dotenv
import os
import json

load_dotenv(".env")
HTTP_REQUEST_HEADERS = {
        "Authorization": f"Bearer {os.environ["GITHUB_TOKEN"]}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "de2-project-group-13",
        "X-GitHub-Api-Version": "2022-11-28"
}

def get_repos_with_stars_in_range(min_stars, max_stars, amount):
    params = {
        "q": f"stars:{min_stars}..{max_stars} fork:false",
        "per_page": f"{amount}"
    }
    response = requests.get("https://api.github.com/search/repositories",
                 headers=HTTP_REQUEST_HEADERS,
                 params=params
    )
    
    return response

def response_to_content_dict(response):
    return json.loads(response.content.decode())

