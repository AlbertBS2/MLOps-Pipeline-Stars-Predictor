from dotenv import load_dotenv
import os
import sys
from utils_scraping import establish_dataset, extract_features_to_csv

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
base_dir = os.path.dirname(__file__)
REPO_DATA_FILENAME = os.path.abspath(os.path.join(base_dir, '..', '..', 'data', 'repo_data.json'))
REPO_DATA_FEATURES_FILENAME = os.path.abspath(os.path.join(base_dir, '..', '..', 'data', 'repo_data.csv'))
#feature extraction config
FEATURES = [
    "full_name", 
    "stargazers_count", 
    "description", 
    "created_at", 
    "updated_at", 
    "forks_count", 
    "watchers_count", 
    "size", 
    "language", 
    "has_issues", 
    "has_projects", 
    "has_downloads", 
    "has_wiki", 
    "has_pages", 
    "has_discussions", 
    "archived", 
    "open_issues_count"
]

passed_argument = sys.argv[1]
    
if passed_argument == "establish_dataset":
    establish_dataset(STAR_RANGES, AMOUNT_PER_INTERVAL, REPO_DATA_FILENAME, BASE_URL, HTTP_REQUEST_HEADERS)
elif passed_argument == "feature_extraction":
    extract_features_to_csv(FEATURES, REPO_DATA_FILENAME, REPO_DATA_FEATURES_FILENAME)
else:
    print(f"No accepted argument passed. Write 'python {sys.argv[0]} *ARGUMENT*', see bottom of file for arguments)")
