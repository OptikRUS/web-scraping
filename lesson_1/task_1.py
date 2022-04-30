import json

import requests


def get_repos_list(username: str, filename: str):
    response = requests.get(f'https://api.github.com/users/{username}/repos')
    if response.status_code == 200:
        with open(filename, 'w') as f:
            json.dump(response.json(), f, indent=4)
        return response.json()
    return response.status_code
