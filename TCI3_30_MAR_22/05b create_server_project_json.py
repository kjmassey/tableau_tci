import requests
import xml.etree.ElementTree as ET
from tableau_sign_in_json import sign_in, json_headers
import json

#https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref.htm#create_project

####
# We'll create a project in the specified site!
####

BASE_URL = 'https://10ax.online.tableau.com/api/3.14'


def get_req_body(proj_name,proj_descr='Default description'):
    return json.dumps({'project' : {
            'name': f"{proj_name}",
            'description' :f"{proj_descr}"
            }
        })

def create_server_project():
    resp = sign_in()

    token = resp['credentials']['token']
    site_luid = resp['credentials']['site']['id']

    headers = json_headers()
    headers['X-Tableau-Auth'] = token

    proj_name = input("Enter new project name: ")

    req = requests.post(url=f"{BASE_URL}/sites/{site_luid}/projects",data=get_req_body(proj_name),headers=headers)

    return req.content

print(create_server_project())



