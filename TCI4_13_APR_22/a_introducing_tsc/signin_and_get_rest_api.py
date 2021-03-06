import requests
from pat import PAT_SECRET
import xml.etree.ElementTree as ET

SERVER_URL = 'https://10ax.online.tableau.com'
SITE_NAME = 'kjmdev797388'

PAT_NAME = 'Kyle'


def get_sign_in_xml():
    '''
    Return the XML body of the Tableau Server sign-in reaquest
    '''

    return f'''
        <tsRequest>
	        <credentials personalAccessTokenName="{PAT_NAME}" personalAccessTokenSecret="{PAT_SECRET}" >
  		        <site contentUrl="{SITE_NAME}" />
	        </credentials>
        </tsRequest>
    '''


def sign_in():
    '''
    Send POST request to Tableau Server to sign in
    '''
    resp = requests.post(
        f"{SERVER_URL}/api/3.14/auth/signin", data=get_sign_in_xml())

    return resp.content


def get_token_from_xml(resp_content):
    resp_xml = ET.fromstring(resp_content)

    return resp_xml.find('.//{*}credentials').attrib['token']


def get_site_luid_from_xml(resp_content):
    resp_xml = ET.fromstring(resp_content)

    return resp_xml.find('.//{*}site').attrib['id']


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
        f"{SERVER_URL}/api/3.14/sites/{site_luid}/workbooks", headers=headers)

    return resp.content


print(get_workbooks())
