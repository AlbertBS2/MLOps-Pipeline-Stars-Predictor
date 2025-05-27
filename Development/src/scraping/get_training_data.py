import requests
from dotenv import load_dotenv
import os
import json
import sys
import csv
import pandas as pd

#requests config
load_dotenv(".env") 

HTTP_REQUEST_HEADERS = {
        "Authorization": f"Bearer {os.environ["GITHUB_TOKEN"]}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "de2-project-group-13",
        "X-GitHub-Api-Version": "2022-11-28"
}
BASE_URL = "https://api.github.com"


#star range distribution for dataset config
STAR_RANGES = [50, 75, 100, 150, 200, 400, 600, 800, 1000, 5000, 10000]
AMOUNT_PER_INTERVAL = 100
REPO_DATA_FILENAME = "./repo_data.json"
REPO_DATA_FEATURES_FILENAME = "./repo_data.csv"
#feature extraction config
FEATURES = ["full_name", "stargazers_count", "description", "created_at", "updated_at", "forks_count", "watchers_count", "size", "language", "has_issues", "has_projects", "has_downloads", "has_wiki", "has_pages", "has_discussions", "archived", "open_issues_count"]



def make_request(endpoint, params={}, base_url=BASE_URL, header=HTTP_REQUEST_HEADERS, method=requests.get):
    response = method(base_url + endpoint,
                    headers=HTTP_REQUEST_HEADERS,
                    params=params
    )
    return response


def json_response_to_content_dict(response):
    return json.loads(response.content.decode())

def get_repos_with_stars_in_range(min_stars, max_stars, amount):
    params = {
        "q": f"stars:{min_stars}..{max_stars} fork:false",
        "per_page": f"{amount}"
    }
    
    response = make_request("/search/repositories", params)
    content_dict = json_response_to_content_dict(response)
    return response, content_dict["items"]

def get_repo(owner_name, repo_name):
    response = make_request(f"/repos/{owner_name}/{repo_name}")
    content_dict = json_response_to_content_dict(response)
    return response, content_dict



#Takes star_ranges, an array of length 11 and then generates a dataset of
#1000 repo names, each sets of 100 on the range star_ranges[i]-star_ranges[i+1]
def establish_dataset(star_ranges, repos_per_interval):
    if os.path.isfile(REPO_DATA_FILENAME):
        cli_response = input("The repo data json file already exists in your directory. Are you sure that you want to create a new one?\nType YES to create a new file: ")
        if cli_response != "YES":
            print("aborting...")
    assert len(star_ranges) == 11 #should be 10 intervals for the ranges
    content_dicts = []
    for i in range(len(star_ranges)):
        if i == 0:
            _, content_dict = get_repos_with_stars_in_range(star_ranges[i], star_ranges[i+1], repos_per_interval)
            content_dicts += content_dict
        elif i != 10:
             _, content_dict = get_repos_with_stars_in_range(star_ranges[i] + 1, star_ranges[i+1], repos_per_interval)
             content_dicts += content_dict
        else: #if i == 10
            json_string = json.dumps(content_dicts, indent=2)
            with open(REPO_DATA_FILENAME, 'w', encoding="utf-8") as f:
                f.write(json_string)

def extract_features_to_csv(features):
    with open(REPO_DATA_FILENAME, 'r', encoding="utf-8") as f:
        repo_dicts = json.loads(f.read())
    
    df = pd.DataFrame(repo_dicts)
    feature_df = df[features]
    feature_df.to_csv(REPO_DATA_FEATURES_FILENAME, index=False)
    
if __name__ == "__main__":

    passed_argument = sys.argv[1]
    
    if passed_argument == "establish_dataset":
        establish_dataset(STAR_RANGES, AMOUNT_PER_INTERVAL)
    elif passed_argument == "feature_extraction":
        extract_features_to_csv(FEATURES)
    else:
        print(f"No accepted argument passed. Write 'python {sys.argv[0]} *ARGUMENT*', see bottom of file for arguments)")