########
# This is a living copy/paste collection of various REST API calls made through the sessions.
# Some code might need to be refactored out of context, be sure to replace URLS, tokens, site names, etc.
########

import csv
import requests
import json
import xml.etree.ElementTree as ET


def get_sign_in_xml():
    '''
    Return the XML body of the Tableau Server sign-in reaquest
    '''

    return f'''
        <tsRequest>
	        <credentials personalAccessTokenName="YOUR_PAT_NAME" personalAccessTokenSecret="YOUR_PAT_SECRET" >
  		        <site contentUrl="YOUR_SITE_NAME" />
	        </credentials>
        </tsRequest>
    '''


def sign_in():
    '''
    Send POST request to Tableau Server to sign in
    '''
    resp = requests.post(
        f"YOUR_SERVER_URL/api/3.14/auth/signin", data=get_sign_in_xml())

    return resp.content


def get_token_from_xml(resp_content):
    '''
    Parse Tableau Server sign-in response for 'token' (x-tableau-auth)
    '''

    resp_xml = ET.fromstring(resp_content)

    return resp_xml.find('.//{*}credentials').attrib['token']


def get_site_luid_from_xml(resp_content):
    '''
    Parse Tableau Server sign-in response for 'site_luid' (useful for subsequent calls)
    '''

    resp_xml = ET.fromstring(resp_content)

    return resp_xml.find('.//{*}site').attrib['id']


def get_sign_in_json():
    req_body = {
        "credentials": {
            "personalAccessTokenName": 'YOUR_PAT_NAME',
            "personalAccessTokenSecret": 'YOUR_PAT_SECRET',
            "site": {
                "contentUrl": "YOUR_SITE_NAME"
            }
        }
    }

    return json.dumps(req_body)


def json_headers():
    return {
        'content-type': 'application/json',
        'accept': 'application/json'
    }


def sign_in():
    resp = requests.post(url=f"YOUR_SERVER_URL/api/3.14/auth/signin",
                         data=get_sign_in_json(), headers=json_headers())

    return json.loads(resp.content)


def get_all_projects():
    '''
    Return all projects on site
    '''
    resp = sign_in()

    token = get_token_from_xml(resp)
    site_luid = get_site_luid_from_xml(resp)

    headers = {"X-Tableau-Auth": token}

    resp = requests.get(
        f"YOUR_SERVER_URL/sites/{site_luid}/projects", headers=headers)

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
        f"YOUR_SERVER_URL/sites/{site_luid}/projects?filter=name:eq:{proj_name}", headers=headers)

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
        f"YOUR_SERVER_URL/sites/{site_luid}/projects?filter=parentProjectId:eq:{parent_id}", headers=headers)

    return resp.content


def get_workbooks():
    '''
    Simple GET request to get all workbooks from site.

    Has no parameters, uses X-Tableau-Auth header
    '''

    auth = sign_in()
    token = get_token_from_xml(auth)
    site_luid = get_site_luid_from_xml(auth)

    headers = {
        'X-Tableau-Auth': token
    }

    resp = requests.get(
        f"YOUR_SERVER_URL/api/3.14/sites/{site_luid}/workbooks", headers=headers)

    return resp.content


def get_workbook_by_luid(wb_luid):
    '''
    GET: Retrieve a workbook via its luid.

    Has no parameters, uses X-Tableau-Auth header
    '''

    auth = sign_in()
    token = get_token_from_xml(auth)
    site_luid = get_site_luid_from_xml(auth)

    headers = {
        'X-Tableau-Auth': token
    }

    resp = requests.get(
        f"YOUR_SERVER_URL/api/3.14/sites/{site_luid}/workbooks/{wb_luid}", headers=headers)

    return resp.content


def filter_workbooks_by_name(wb_name):
    '''
    GET: Retrieve a filtered list of workbooks where name = wb_name
    '''

    auth = sign_in()
    token = get_token_from_xml(auth)
    site_luid = get_site_luid_from_xml(auth)

    headers = {
        'X-Tableau-Auth': token
    }

    resp = requests.get(
        f"YOUR_SERVER_URL/api/3.14/sites/{site_luid}/workbooks/?filter=name:eq:{wb_name}", headers=headers)

    return resp.content


def filter_datasources_updated_before(date):
    '''
    GET: Retrieve a filtered list of datasources where 'last updated' <= date
    '''

    auth = sign_in()
    token = get_token_from_xml(auth)
    site_luid = get_site_luid_from_xml(auth)

    headers = {
        'X-Tableau-Auth': token
    }

    resp = requests.get(
        f"YOUR_SERVER_URL/api/3.14/sites/{site_luid}/workbooks/?filter=updatedAt:lte:{date}", headers=headers)

    return resp.content


def get_items_from_csv(csv_path):
    '''
    Read a csv file into a list of dictionaries
    '''

    with open(csv_path, 'r', newline='', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        return list(csv_reader)


def get_request_body():
    '''
    Build the request body for refreshing a workbook/datasource -- which is empty!
    '''

    return '<tsRequest></tsRequest>'


def refrest_a_list_of_extracts_from_csv(csv_path):
    '''
    Read a CSV file to a list of dictionaries and send a refresh request for each
    '''

    extract_list = get_items_from_csv(csv_path)

    response_list = []

    for item in extract_list:

        auth = sign_in()
        token = get_token_from_xml(auth)

        headers = {
            'X-Tableau-Auth': token
        }

        item_type_endpoint = 'workbooks'

        if item['object_type'] == 'datasource':
            item_type_endpoint = 'datasources'

        resp = requests.post(
            f"YOUR_SERVER_URL/api/3.14/sites/{item['site_luid']}/{item_type_endpoint}/{item['object_luid']}/refresh", data=get_request_body(), headers=headers)

        response_list.append(resp.content)

    return response_list


def query_job(job_id):
    '''
    Query the status of a job (e.g. extract refresh)
    '''

    auth = sign_in()
    token = get_token_from_xml(auth)
    site_luid = get_site_luid_from_xml(auth)

    headers = {
        'X-Tableau-Auth': token
    }

    resp = requests.get(
        f"YOUR_SERVER_URL/api/3.14/sites/{site_luid}/jobs/{job_id}", headers=headers)

    return resp.content


def make_multipart_req(source):
    '''
    Used to create the complex request format needed when publishing workbooks/datasources via the REST API

    Adapted from
    https://stackoverflow.com/questions/26299889/how-to-post-multipart-list-of-json-xml-files-using-python-requests
    '''

    from urllib3.filepost import encode_multipart_formdata
    from urllib3.fields import RequestField

    multipart_parts = []

    for name, (filename, contents, content_type) in source.items():
        part = RequestField(name=name, data=contents, filename=filename)
        part.make_multipart(content_type=content_type)

        multipart_parts.append(part)

    payload, content_type = encode_multipart_formdata(multipart_parts)

    content_type = ''.join(('multipart/mixed',) +
                           content_type.partition(';')[1:])

    return payload, content_type


def get_publish_req_body(wb_name, show_tabs, proj_luid):
    '''
    Returns the base XML request body for a very basic workbook publish
    '''

    return f'''
    <tsRequest>
    <workbook name="{wb_name}" showTabs="{show_tabs}">
        <project id="{proj_luid}"/>
    </workbook>
    </tsRequest>
    '''


def publish_workbook(wb_path, show_tabs, proj_luid):
    '''
    Publish a very simple workbook using the REST API -- the only good use case, IMO ;)
    '''

    auth = sign_in()
    token = get_token_from_xml(auth)
    site_luid = get_site_luid_from_xml(auth)

    wb_filename = wb_path.split('\\')[-1]
    wb_name = wb_filename.split('.')[0]

    # Read the content of the file as 'bytes'
    wb_contents = open(wb_path, 'rb').read()

    req_body = get_publish_req_body(wb_name, show_tabs, proj_luid)

    req_parts = {
        'request_payload': ('', req_body, 'text/xml'),
        'tableau_workbook': (wb_path, wb_contents, 'application/xml')
    }

    payload, content_type = make_multipart_req(req_parts)

    resp = requests.post(f"YOUR_SERVER_URL/api/3.14/sites/{site_luid}/workbooks?overwrite=true",
                         data=payload, headers={'x-tableau-auth': token, 'content-type': content_type})

    return resp.content
