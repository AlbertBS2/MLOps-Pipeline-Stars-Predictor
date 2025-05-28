import json
import requests
import pandas as pd


def make_request(endpoint, base_url, header, params={}, method=requests.get):
    response = method(base_url + endpoint,
                    headers=header,
                    params=params
    )
    return response


def json_response_to_content_dict(response):
    return json.loads(response.content.decode())


def get_repos_with_stars_in_range(min_stars, max_stars, amount, base_url, header, method=requests.get):
    params = {
        "q": f"stars:{min_stars}..{max_stars} fork:false",
        "per_page": f"{amount}"
    }
    
    response = make_request("/search/repositories", base_url, header, params, method)
    content_dict = json_response_to_content_dict(response)
    return response, content_dict["items"]


def get_repo(owner_name, repo_name, base_url, header, method=requests.get, params={}):
    response = make_request(f"/repos/{owner_name}/{repo_name}", base_url, header, params, method)
    content_dict = json_response_to_content_dict(response)
    return response, content_dict


#Takes star_ranges, an array of length 11 and then generates a dataset of
#1000 repo names, each sets of 100 on the range star_ranges[i]-star_ranges[i+1]
def establish_dataset(star_ranges, repos_per_interval, data_path, base_url, header, method=requests.get):
    content_dicts = []
    for i in range(len(star_ranges)):
        if i == 0:
            _, content_dict = get_repos_with_stars_in_range(star_ranges[i], star_ranges[i+1], repos_per_interval, base_url, header, method)
            content_dicts += content_dict
        elif i != 10:
             _, content_dict = get_repos_with_stars_in_range(star_ranges[i] + 1, star_ranges[i+1], repos_per_interval, base_url, header, method)
             content_dicts += content_dict
        else: #if i == 10
            json_string = json.dumps(content_dicts, indent=2)
            with open(data_path, 'w', encoding="utf-8") as f:
                f.write(json_string)


def extract_features_to_csv(features, data_path, features_path):
    with open(data_path, 'r', encoding="utf-8") as f:
        repo_dicts = json.loads(f.read())
    
    df = pd.DataFrame(repo_dicts)
    feature_df = df[features]
    feature_df.to_csv(features_path, index=False)
