from lib2to3.pgen2 import token
import requests
from tableau_sign_in_xml import sign_in, get_token_from_xml, get_site_luid_from_xml
import xml.etree.ElementTree as ET

#https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref.htm#create_project

####
# We'll create a project in the specified site!
####

BASE_URL = 'https://10ax.online.tableau.com/api/3.14'


def get_req_body(proj_name,proj_descr='Default description'):
    return f'''
    <tsRequest>
        <project 
            name="{proj_name}"
            description="{proj_descr}"/>
    
    </tsRequest>
    '''

def create_server_project():
    resp = sign_in()

    token = get_token_from_xml(resp)
    site_luid = get_site_luid_from_xml(resp)

    headers = {'X-Tableau-Auth': token}

    proj_name = input("Enter new project name: ")

    req = requests.post(url=f"{BASE_URL}/sites/{site_luid}/projects",data=get_req_body(proj_name),headers=headers)

    return req.content

print(create_server_project())



