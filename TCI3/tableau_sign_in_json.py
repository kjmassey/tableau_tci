import requests
from pat_secret import PAT_SECRET
import json

SERVER_URL = 'https://10ax.online.tableau.com/'
SITE_NAME = 'kjmdev797388'

PAT_NAME = 'Kyle'

def get_sign_in_json():
    return json.dumps({
    "credentials" : {
        "personalAccessTokenName":"Kyle",
        "personalAccessTokenSecret":"SJmSPpgzRvWcMI5M+VhxKA==:uHV6Ht7XdOYn43Bj3bA90CJgogjMrKe1",
        "site": {
            "contentUrl":"kjmdev797388"
        }
    }
})

def json_headers():
    return {
        'content-type': 'application/json',
        'accept':'application/json'
    }

def sign_in():
    resp = requests.post(url=f"{SERVER_URL}/api/3.14/auth/signin",data=get_sign_in_json(),headers=json_headers())

    return resp.content

print(sign_in())