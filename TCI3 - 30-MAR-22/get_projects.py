import requests
import json
from tableau_sign_in_xml import sign_in, get_token_from_xml, get_site_luid_from_xml

# https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref.htm#query_projects

####
# There are multiple ways to query projects from Tableau Server
####

BASE_URL = 'https://10ax.online.tableau.com/api/3.14'


def get_all_projects():
    '''
    Return all projects on site
    '''
    resp = sign_in()

    token = get_token_from_xml(resp)
    site_luid = get_site_luid_from_xml(resp)

    headers = {"X-Tableau-Auth": token}

    resp = requests.get(
        f"{BASE_URL}/sites/{site_luid}/projects", headers=headers)

    return resp.content


def get_project_by_name(proj_name):
    '''
    Get a project by its name
    '''
    resp = sign_in()

    token = get_token_from_xml(resp)
    site_luid = get_site_luid_from_xml(resp)

    headers = {"X-Tableau-Auth": token}

    resp = requests.get(
        f"{BASE_URL}/sites/{site_luid}/projects?filter=name:eq:{proj_name}", headers=headers)

    return resp.content


def get_projects_by_parent_id(parent_id):
    '''
    Get sub projects by their parent project's luid
    '''
    resp = sign_in()

    token = get_token_from_xml(resp)
    site_luid = get_site_luid_from_xml(resp)

    headers = {"X-Tableau-Auth": token}

    resp = requests.get(
        f"{BASE_URL}/sites/{site_luid}/projects?filter=parentProjectId:eq:{parent_id}", headers=headers)

    return resp.content


print(get_projects_by_parent_id('830ab4f5-638a-4473-98ac-cbadb9c35f64'))
